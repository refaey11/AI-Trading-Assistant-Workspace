from __future__ import annotations

"""Governed canonical runtime entry for 2016-2024.

Reuses existing Decision Brain V1, handoff and Risk boundaries. It does not
rebuild Murphy/Nison knowledge and never manufactures TIZ PASS or SL/TP.
All historical joins are point-in-time/as-of. 2025 is excluded at ingestion.
"""

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
BRAIN = ROOT / "RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py"
HANDOFF = ROOT / "compatibility/knowledge_decision_handoff.py"
RISK = ROOT / "RUNTIME/RISK_ENGINE_INTEGRATION_V1/risk_engine_integration_v1.py"
ALLOWLIST = ROOT / "governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json"
TIZ_BOUNDARY = ROOT / "03_TIZ/TIZ_RUNTIME_BOUNDARY_RESOLUTION_V2.json"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if not spec or not spec.loader:
        raise RuntimeError(f"Unable to load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read_csv(path: Path, required: set[str], chunksize: int | None = None) -> pd.DataFrame:
    if chunksize:
        parts = []
        for part in pd.read_csv(path, chunksize=chunksize, low_memory=False):
            missing = sorted(required - set(part.columns))
            if missing:
                raise ValueError(f"{path}: missing {missing}")
            parts.append(part)
        df = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame(columns=sorted(required))
    else:
        df = pd.read_csv(path, low_memory=False)
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"{path}: missing {missing}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce", format="mixed")
    if df["timestamp"].isna().any():
        raise ValueError(f"{path}: invalid timestamp")
    return df.sort_values("timestamp").drop_duplicates("timestamp", keep="last").reset_index(drop=True)


def asof_join(left: pd.DataFrame, right: pd.DataFrame, suffix: str) -> pd.DataFrame:
    if right.empty:
        return left.copy()
    cols = [c for c in right.columns if c != "timestamp"]
    r = right[["timestamp", *cols]].sort_values("timestamp").drop_duplicates("timestamp", keep="last")
    return pd.merge_asof(left.sort_values("timestamp"), r, on="timestamp", direction="backward", allow_exact_matches=True, suffixes=("", suffix))


def norm_direction(value: Any) -> str | None:
    s = str(value or "").strip().upper()
    return {"BUY": "BULLISH", "BULL": "BULLISH", "BULLISH": "BULLISH", "SELL": "BEARISH", "BEAR": "BEARISH", "BEARISH": "BEARISH"}.get(s)


def aggregate_rule_frame(df: pd.DataFrame, rule_col: str, status_col: str = "status", direction_col: str = "direction") -> pd.DataFrame:
    rows = []
    for ts, g in df.groupby("timestamp", sort=True):
        passed = g[g[status_col].astype(str).str.upper().eq("PASS")]
        dirs = {d for d in (norm_direction(x) for x in passed[direction_col]) if d}
        direction = next(iter(dirs)) if len(dirs) == 1 else ("CONFLICTED" if len(dirs) > 1 else "ABSENT")
        rows.append({"timestamp": ts, "direction": direction, "rule_ids": "|".join(sorted(set(str(x) for x in g[rule_col].dropna()))), "rule_count": int(g[rule_col].nunique())})
    return pd.DataFrame(rows)


def source_snapshot(path: Path, label: str) -> dict[str, Any]:
    files = [p for p in path.rglob("*") if p.is_file()] if path.exists() else []
    data_files = [p for p in files if p.suffix.lower() in {".csv", ".json", ".parquet", ".txt"}]
    return {"source": label, "status": "CONNECTED_GOVERNED_SNAPSHOT" if data_files else "NOT_EVALUABLE", "artifact_count": len(data_files), "direction": None, "final_trade_decision": None}


def first_value(row: pd.Series, aliases: list[str]):
    for key in aliases:
        if key in row.index and pd.notna(row[key]):
            return row[key]
    return None


def brain_row(row: pd.Series) -> dict[str, Any]:
    trend_map = {"BULL_TREND": 1.0, "BEAR_TREND": -1.0, "TRANSITION": 0.0, "UNKNOWN": 0.0}
    out = {"mtf_trend_score": 0.0, "volume_available": False}
    for tf in ("M5", "M15", "M30", "H1", "H4", "D1"):
        out[f"{tf}_trend_regime"] = 0.0
        out[f"{tf}_volume_regime"] = 0.0
    for tf in ("M5", "M15", "M30", "H1", "H4", "D1"):
        raw = first_value(row, [f"{tf}_trend_regime", f"{tf}_trend", f"{tf.lower()}_trend"])
        if raw is not None:
            out[f"{tf}_trend_regime"] = trend_map.get(str(raw).upper(), float(raw) if isinstance(raw, (int, float)) else 0.0)
    raw = first_value(row, ["mtf_trend_score", "mtf_score"])
    if raw is not None:
        out["mtf_trend_score"] = float(raw)
    return out


def run(args) -> dict[str, Any]:
    bars = read_csv(args.h1, {"timestamp", "open", "high", "low", "close"})
    bars = bars[(bars.timestamp.dt.year >= 2016) & (bars.timestamp.dt.year <= 2024)].copy()
    if bars.empty:
        raise ValueError("No 2016-2024 H1 bars available")

    market = read_csv(args.market, {"timestamp"})
    mtf = read_csv(args.mtf, {"timestamp"})
    murphy = read_csv(args.murphy, {"timestamp", "status", "direction", "source_rule_id"})
    nison = read_csv(args.nison, {"timestamp", "status", "direction", "rule_id"}, chunksize=400000)
    hc = read_csv(args.historical_context, {"timestamp", "context_signature"})
    ho = read_csv(args.historical_outcome, {"timestamp", "context_signature"})

    allow = json.loads(ALLOWLIST.read_text(encoding="utf-8"))
    murphy_allowed = set(allow["verified_runtime"]["MURPHY"])
    nison_allowed = set(allow["verified_runtime"]["NISON"])
    murphy_ids = {x for v in murphy.source_rule_id.dropna() for x in str(v).split("|") if x}
    nison_ids = set(nison.rule_id.dropna().astype(str))
    blocked = {x["rule_id"] for x in allow.get("explicitly_blocked", [])}
    unknown_m = sorted(murphy_ids - murphy_allowed)
    unknown_n = sorted(nison_ids - nison_allowed)
    blocked_m = sorted(murphy_ids & blocked)
    if unknown_m or unknown_n or blocked_m:
        raise ValueError(json.dumps({"unknown_murphy": unknown_m, "unknown_nison": unknown_n, "blocked_murphy": blocked_m}))

    m = aggregate_rule_frame(murphy, "source_rule_id")
    n = aggregate_rule_frame(nison, "rule_id")
    joined = bars[["timestamp", "open", "high", "low", "close"]].copy()
    joined = asof_join(joined, market, "_market")
    joined = asof_join(joined, mtf, "_mtf")
    joined = asof_join(joined, m.rename(columns={"direction": "murphy_direction", "rule_ids": "murphy_rule_ids", "rule_count": "murphy_rule_count"}), "_murphy")
    joined = asof_join(joined, n.rename(columns={"direction": "nison_confirmation", "rule_ids": "nison_rule_ids", "rule_count": "nison_rule_count"}), "_nison")
    joined = asof_join(joined, hc[["timestamp", "context_signature"]].rename(columns={"context_signature": "historical_context_signature"}), "_hc")
    joined = asof_join(joined, ho[["timestamp", "context_signature"]].rename(columns={"context_signature": "historical_outcome_signature"}), "_ho")

    brain = load_module(BRAIN, "decision_brain_v1")
    handoff = load_module(HANDOFF, "knowledge_decision_handoff")
    risk = load_module(RISK, "risk_engine")
    tiz_boundary = json.loads(TIZ_BOUNDARY.read_text(encoding="utf-8"))
    sim_meta = source_snapshot(args.similarity, "Similarity V2")
    ret_meta = source_snapshot(args.retrieval, "Context-Aware Retrieval V2")

    events = []
    for _, row in joined.iterrows():
        ts = row.timestamp
        murphy_dir = row.get("murphy_direction")
        nison_dir = row.get("nison_confirmation")
        nison_contradiction = nison_dir == "CONFLICTED"
        alignment = "NISON_CONTRADICTION" if nison_contradiction else ("ALIGNED" if murphy_dir in {"BULLISH", "BEARISH"} else "NEEDS_REVIEW")
        evidence_bundle = {
            "h1": {"status": "CONNECTED", "timestamp": ts.isoformat()},
            "market_state": {"status": "CONNECTED"},
            "market_structure": {"status": "CONNECTED_OR_UNRESOLVED", "direction": None},
            "dynamic_mtf": {"status": "CONNECTED"},
            "murphy": {"status": "CONNECTED", "direction": murphy_dir, "rule_ids": row.get("murphy_rule_ids")},
            "nison": {"status": "CONNECTED", "confirmation": nison_dir, "contradiction": nison_contradiction, "direction_generated": False},
            "historical_context": {"status": "CONNECTED" if pd.notna(row.get("historical_context_signature")) else "NOT_EVALUABLE", "context_signature": row.get("historical_context_signature")},
            "historical_outcome": {"status": "CONNECTED" if pd.notna(row.get("historical_outcome_signature")) else "NOT_EVALUABLE", "context_signature": row.get("historical_outcome_signature")},
            "similarity": sim_meta,
            "context_aware_retrieval": ret_meta,
            "tiz": {"status": "NOT_EVALUABLE", "direction": None, "final_trade_decision": None, "boundary": tiz_boundary["status"]},
        }
        h = handoff.build_handoff(
            brain_row(row),
            {
                "alignment_state": alignment,
                "candidate_direction": str(murphy_dir or "neutral").lower(),
                "contradiction_gate": "FAIL" if nison_contradiction else "PASS",
                "process_gate": "NOT_EVALUABLE",
                "book_evidence_status": "CONNECTED",
                "market_evidence_status": "CONNECTED",
                "similarity_record_count": sim_meta["artifact_count"],
                "evidence_bundle": evidence_bundle,
            },
            similarity=sim_meta,
        )
        assessment = brain.assess(h["decision_brain_row"], similarity=sim_meta)

        entry = float(row["close"])
        stop = first_value(row, ["stop_loss", "sl", "execution_stop_loss"])
        target = first_value(row, ["take_profit", "tp", "execution_take_profit"])
        atr = first_value(row, ["atr", "ATR", "execution_atr"])
        equity = first_value(row, ["equity", "account_equity", "execution_equity"])
        peak = first_value(row, ["peak_equity", "account_peak_equity", "execution_peak_equity"])
        streak = first_value(row, ["prior_loss_streak", "loss_streak", "execution_loss_streak"])
        risk_status = "NOT_EVALUABLE"
        risk_reason = "MISSING_UPSTREAM_EXECUTION_INPUT"
        risk_size = None
        if all(x is not None for x in (equity, peak, streak, stop, target, atr)):
            rr = risk.evaluate_risk(equity=float(equity), entry=entry, stop_loss=float(stop), take_profit=float(target), atr=float(atr), prior_loss_streak=int(streak), peak_equity=float(peak))
            risk_status = "PASS" if rr.risk_pass else "FAIL"
            risk_reason = rr.reason
            risk_size = rr.position_size

        trade_allowed = bool(risk_status == "PASS" and not h["gates"]["abstain"])
        events.append({
            "timestamp": ts,
            "murphy_direction": murphy_dir,
            "nison_confirmation": nison_dir,
            "nison_contradiction": nison_contradiction,
            "historical_context_asof": pd.notna(row.get("historical_context_signature")),
            "historical_outcome_asof": pd.notna(row.get("historical_outcome_signature")),
            "similarity_status": sim_meta["status"],
            "retrieval_status": ret_meta["status"],
            "handoff_routing": h["routing"],
            "handoff_abstain": h["gates"]["abstain"],
            "brain_bias": assessment.directional_bias,
            "brain_confidence": assessment.confidence,
            "tiz_status": "NOT_EVALUABLE",
            "risk_status": risk_status,
            "risk_reason": risk_reason,
            "position_size": risk_size,
            "trade_allowed": trade_allowed,
            "2025_locked": True,
        })

    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    ev = pd.DataFrame(events)
    ev.to_csv(out / "decision_events_2016_2024.csv", index=False)
    manifest = {
        "status": "CANONICAL_GOVERNED_RUNNER_V3_COMPILED",
        "window": "2016-2024",
        "2025_locked": True,
        "murphy_observed_rule_count": len(murphy_ids),
        "nison_observed_rule_count": len(nison_ids),
        "similarity": sim_meta,
        "retrieval": ret_meta,
        "tiz": {"status": "NOT_EVALUABLE", "hardcoded_pass": False, "boundary": tiz_boundary["status"]},
        "risk": {"hardcoded_pass": False, "synthetic_sl_tp": False, "real_upstream_inputs_required": True},
        "decision_brain_v1_source_unchanged": True,
        "memory_or_retrieval_generated_direction": False,
        "events": int(len(ev)),
        "trade_allowed_events": int(ev["trade_allowed"].sum()) if not ev.empty else 0,
    }
    (out / "canonical_e2e_manifest_v3.json").write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")
    print(json.dumps(manifest, indent=2, default=str))


def main() -> None:
    p = argparse.ArgumentParser()
    for name in ("h1", "market", "mtf", "murphy", "nison", "historical-context", "historical-outcome", "similarity", "retrieval", "output-dir"):
        p.add_argument("--" + name, required=True, type=Path)
    run(p.parse_args())


if __name__ == "__main__":
    main()
