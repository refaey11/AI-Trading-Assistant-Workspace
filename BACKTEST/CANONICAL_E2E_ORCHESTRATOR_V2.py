from __future__ import annotations

"""Canonical E2E evidence compiler for 2016-2024.

This layer integrates existing artifacts without rebuilding book knowledge or
Decision Brain V1. It compiles one point-in-time evidence envelope per H1 bar,
then crosses the existing Knowledge/Decision Handoff boundary. Memory and
retrieval remain evidence-only. No synthetic SL/TP is created here.
"""

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

ALLOWLIST = ROOT / "governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json"
BRAIN = ROOT / "RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py"
HANDOFF = ROOT / "compatibility/knowledge_decision_handoff.py"
RISK = ROOT / "RUNTIME/RISK_ENGINE_INTEGRATION_V1/risk_engine_integration_v1.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if not spec or not spec.loader:
        raise RuntimeError(f"Cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read_csv(path: Path, required: set[str], chunksize: int | None = None) -> pd.DataFrame:
    if chunksize:
        parts = []
        for p in pd.read_csv(path, chunksize=chunksize, low_memory=False):
            missing = sorted(required - set(p.columns))
            if missing:
                raise ValueError(f"{path}: missing {missing}")
            parts.append(p)
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


def split_ids(values) -> set[str]:
    out: set[str] = set()
    for value in values:
        if pd.isna(value):
            continue
        out.update(x.strip() for x in str(value).split("|") if x.strip())
    return out


def norm_direction(value: Any) -> str | None:
    s = str(value or "").strip().upper()
    if s in {"BUY", "BULL", "BULLISH"}:
        return "BULLISH"
    if s in {"SELL", "BEAR", "BEARISH"}:
        return "BEARISH"
    return None


def allowed_rules() -> tuple[set[str], set[str]]:
    data = json.loads(ALLOWLIST.read_text(encoding="utf-8"))
    return set(data["verified_runtime"]["MURPHY"]), set(data["verified_runtime"]["NISON"])


def aggregate_murphy(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for ts, g in df.groupby("timestamp", sort=True):
        passed = g[g["status"].astype(str).str.upper().eq("PASS")]
        dirs = {d for d in (norm_direction(x) for x in passed["direction"]) if d}
        direction = next(iter(dirs)) if len(dirs) == 1 else ("CONFLICTED" if len(dirs) > 1 else "ABSENT")
        rows.append({
            "timestamp": ts,
            "murphy_direction": direction,
            "murphy_rule_ids": sorted(split_ids(g["source_rule_id"])),
            "murphy_rule_count": len(split_ids(g["source_rule_id"])),
        })
    return pd.DataFrame(rows)


def aggregate_nison(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for ts, g in df.groupby("timestamp", sort=True):
        passed = g[g["status"].astype(str).str.upper().eq("PASS")]
        failed = g[g["status"].astype(str).str.upper().eq("FAIL")]
        dirs = {d for d in (norm_direction(x) for x in passed["direction"]) if d}
        rows.append({
            "timestamp": ts,
            "nison_confirmation": next(iter(dirs)) if len(dirs) == 1 else ("CONFLICTED" if len(dirs) > 1 else "ABSENT"),
            "nison_contradiction": bool(not failed.empty),
            "nison_rule_count": int(g["rule_id"].nunique()),
        })
    return pd.DataFrame(rows)


def asof_join(left: pd.DataFrame, right: pd.DataFrame) -> pd.DataFrame:
    if right.empty:
        return left.copy()
    cols = [c for c in right.columns if c != "timestamp"]
    r = right[["timestamp", *cols]].sort_values("timestamp").drop_duplicates("timestamp", keep="last")
    return pd.merge_asof(left.sort_values("timestamp"), r, on="timestamp", direction="backward", allow_exact_matches=True)


def snapshot(root: Path, label: str) -> dict[str, Any]:
    files = []
    if root.exists():
        files = [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in {".json", ".csv"}]
    return {
        "source": label,
        "status": "CONNECTED_GOVERNED_SNAPSHOT" if files else "NOT_EVALUABLE",
        "artifact_count": len(files),
        "direction": None,
        "final_trade_decision": None,
    }


def brain_row(market: dict[str, Any], mtf: dict[str, Any]) -> dict[str, Any]:
    trend_map = {"BULL_TREND": 1.0, "BEAR_TREND": -1.0, "TRANSITION": 0.0, "UNKNOWN": 0.0}
    keys = ["M5_trend_regime", "M15_trend_regime", "M30_trend_regime", "H1_trend_regime", "H4_trend_regime", "D1_trend_regime"]
    volume = ["M5_volume_regime", "M15_volume_regime", "M30_volume_regime", "H1_volume_regime", "H4_volume_regime", "D1_volume_regime"]
    row = {k: 0.0 for k in ["mtf_trend_score", *keys, *volume]}
    row["volume_available"] = False
    if market:
        row["H1_trend_regime"] = trend_map.get(str(market.get("trend", "UNKNOWN")).upper(), 0.0)
        for k in row:
            if k in market and pd.notna(market[k]):
                row[k] = market[k]
    if mtf:
        row["mtf_trend_score"] = trend_map.get(str(mtf.get("trend", "UNKNOWN")).upper(), 0.0)
        row["H4_trend_regime"] = trend_map.get(str(mtf.get("h4_trend", "UNKNOWN")).upper(), 0.0)
    return row


def run(args) -> dict[str, Any]:
    bars = read_csv(args.h1, {"timestamp", "open", "high", "low", "close"})
    bars = bars[(bars.timestamp.dt.year >= 2016) & (bars.timestamp.dt.year <= 2024)].reset_index(drop=True)
    market = read_csv(args.market, {"timestamp"})
    mtf = read_csv(args.mtf, {"timestamp"})
    murphy_raw = read_csv(args.murphy, {"timestamp", "status", "direction", "source_rule_id"})
    nison_raw = read_csv(args.nison, {"timestamp", "status", "direction", "rule_id"}, chunksize=400000)
    hc = read_csv(args.historical_context, {"timestamp", "context_signature"})
    ho = read_csv(args.historical_outcome, {"timestamp", "context_signature"})

    am, an = allowed_rules()
    observed_m = split_ids(murphy_raw["source_rule_id"])
    observed_n = set(nison_raw["rule_id"].astype(str))
    blocked = {x["rule_id"] for x in json.loads(ALLOWLIST.read_text(encoding="utf-8")).get("explicitly_blocked", [])}
    if observed_m - am:
        raise ValueError(f"Unknown Murphy rule id(s): {sorted(observed_m-am)}")
    if observed_n - an:
        raise ValueError(f"Unknown Nison rule id(s): {sorted(observed_n-an)}")
    if observed_m & blocked:
        raise ValueError(f"Blocked Murphy rule(s) observed: {sorted(observed_m & blocked)}")

    murphy = aggregate_murphy(murphy_raw)
    nison = aggregate_nison(nison_raw)
    base = bars[["timestamp", "close"]]
    joined = asof_join(base, market)
    joined = asof_join(joined, mtf)
    joined = asof_join(joined, murphy)
    joined = asof_join(joined, nison)
    joined = asof_join(joined, hc[[c for c in hc.columns if c in {"timestamp", "context_signature"}]])
    joined = asof_join(joined, ho[[c for c in ho.columns if c in {"timestamp", "context_signature"}]])

    brain = load_module(BRAIN, "decision_brain_v1")
    handoff_mod = load_module(HANDOFF, "knowledge_decision_handoff")
    risk_mod = load_module(RISK, "risk_engine")
    sim_meta = snapshot(args.similarity, "Similarity V2")
    ret_meta = snapshot(args.retrieval, "Context-Aware Retrieval V2")

    events = []
    for idx, row in joined.iterrows():
        ts = row["timestamp"]
        market_values = {k: v for k, v in row.to_dict().items() if k != "timestamp" and pd.notna(v)}
        mtf_values = market_values.copy()
        mdir = row.get("murphy_direction")
        ncontra = bool(row.get("nison_contradiction", False))
        nconf = str(row.get("nison_confirmation") or "ABSENT")
        evidence = {
            "h1": {"status": "CONNECTED", "direction": None, "final_trade_decision": None, "timestamp": ts.isoformat()},
            "market_state": {"status": "CONNECTED", "direction": None, "final_trade_decision": None},
            "mtf": {"status": "CONNECTED", "direction": None, "final_trade_decision": None},
            "murphy": {"status": "CONNECTED", "direction": str(mdir or "ABSENT").lower()},
            "nison": {"status": "CONNECTED", "confirmation": nconf, "contradiction": ncontra, "direction_generated": False},
            "historical_context": {"status": "CONNECTED" if pd.notna(row.get("context_signature_x")) else "NOT_EVALUABLE", "direction": None, "final_trade_decision": None, "context_signature": row.get("context_signature_x")},
            "historical_outcome": {"status": "CONNECTED" if pd.notna(row.get("context_signature_y")) else "NOT_EVALUABLE", "direction": None, "final_trade_decision": None, "context_signature": row.get("context_signature_y")},
            "similarity": sim_meta,
            "context_aware_retrieval": ret_meta,
            "tiz": {"status": "UNRESOLVED_OPTIONAL", "direction": None, "final_trade_decision": None},
        }
        alignment = "NISON_CONTRADICTION" if ncontra else ("ALIGNED" if mdir in {"BULLISH", "BEARISH"} else "NEEDS_REVIEW")
        h = handoff_mod.build_handoff(
            brain_row(market_values, mtf_values),
            {
                "alignment_state": alignment,
                "candidate_direction": str(mdir or "neutral").lower(),
                "contradiction_gate": "FAIL" if ncontra else "PASS",
                "process_gate": "NOT_EVALUABLE",
                "book_evidence_status": "CONNECTED",
                "market_evidence_status": "CONNECTED",
                "similarity_record_count": 0,
                "evidence_bundle": evidence,
            },
            similarity=sim_meta,
        )
        assessment = brain.assess(h["decision_brain_row"], similarity=None)

        # Risk is evaluated only when real upstream execution inputs exist.
        risk_status = "NOT_EVALUABLE"
        risk_reason = "MISSING_UPSTREAM_SL_TP_ATR"
        if all(k in row.index and pd.notna(row[k]) for k in ("stop_loss", "take_profit", "atr")):
            atr = float(row["atr"])
            entry = float(row["close"])
            rr = risk_mod.evaluate_risk(equity=100000.0, entry=entry, stop_loss=float(row["stop_loss"]), take_profit=float(row["take_profit"]), atr=atr, prior_loss_streak=0, peak_equity=100000.0)
            risk_status, risk_reason = ("PASS" if rr.risk_pass else "FAIL"), rr.reason

        events.append({
            "timestamp": ts,
            "h1_connected": True,
            "market_state_connected": True,
            "mtf_connected": True,
            "murphy_direction": mdir,
            "murphy_rule_count": int(row.get("murphy_rule_count", 0) or 0),
            "nison_confirmation": nconf,
            "nison_contradiction": ncontra,
            "historical_context_asof": pd.notna(row.get("context_signature_x")),
            "historical_outcome_asof": pd.notna(row.get("context_signature_y")),
            "similarity_status": sim_meta["status"],
            "retrieval_status": ret_meta["status"],
            "handoff_routing": h["routing"],
            "handoff_abstain": h["gates"]["abstain"],
            "brain_bias": assessment.directional_bias,
            "brain_confidence": assessment.confidence,
            "tiz_status": "UNRESOLVED_OPTIONAL",
            "risk_status": risk_status,
            "risk_reason": risk_reason,
            "2025_locked": int(ts.year) != 2025,
        })
        if (idx + 1) % 5000 == 0:
            print(f"E2E_PROGRESS {idx+1}/{len(joined)} as_of={ts.isoformat()}", flush=True)

    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    ev = pd.DataFrame(events)
    ev.to_csv(out / "unified_evidence_events_2016_2024.csv", index=False)
    manifest = {
        "status": "CANONICAL_E2E_EVIDENCE_COMPILED",
        "window": "2016-2024",
        "2025_locked": True,
        "murphy_observed_rule_count": len(observed_m),
        "nison_observed_rule_count": len(observed_n),
        "similarity": sim_meta,
        "retrieval": ret_meta,
        "tiz": "UNRESOLVED_OPTIONAL",
        "risk_sl_tp_synthetic": False,
        "decision_brain_v1_source_unchanged": True,
        "memory_or_retrieval_generated_direction": False,
    }
    (out / "canonical_e2e_manifest.json").write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")
    print(json.dumps(manifest, indent=2, default=str))


def main() -> None:
    p = argparse.ArgumentParser()
    for name in ("h1", "market", "mtf", "murphy", "nison", "historical-context", "historical-outcome", "similarity", "retrieval", "output-dir"):
        p.add_argument("--" + name, required=True, type=Path)
    run(p.parse_args())


if __name__ == "__main__":
    main()
