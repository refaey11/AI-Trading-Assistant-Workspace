from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
BRAIN_PATH = ROOT / "RECOVERED_SOURCES" / "DECISION_BRAIN_V1" / "decision_brain.py"
GATE_PATH = ROOT / "compatibility" / "murphy_governed_decision_gate_v1.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if not spec or not spec.loader:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_csv(path: Path, required: set[str], duplicates: bool = False) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"{path}: missing columns {missing}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if df["timestamp"].isna().any():
        raise ValueError(f"{path}: invalid timestamps")
    if not duplicates and df["timestamp"].duplicated().any():
        raise ValueError(f"{path}: duplicate timestamps")
    return df.sort_values("timestamp").reset_index(drop=True)


def norm_direction(value: Any) -> str | None:
    text = str(value or "").strip().upper()
    if text in {"BUY", "BULL", "BULLISH"}:
        return "BULLISH"
    if text in {"SELL", "BEAR", "BEARISH"}:
        return "BEARISH"
    return None


def aggregate_murphy(df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for ts, group in df.groupby("timestamp", sort=True):
        passed = group[group["status"].astype(str).str.upper().eq("PASS")]
        directions = sorted({d for d in (norm_direction(x) for x in passed["direction"]) if d})
        if len(directions) == 1:
            status, direction = "PASS", directions[0]
        elif len(directions) > 1:
            status, direction = "PASS", None
        else:
            status, direction = "NOT_EVALUABLE", None
        rule_ids = []
        if "source_rule_id" in group.columns:
            for value in group["source_rule_id"].dropna():
                rule_ids.extend(str(value).split("|"))
        rows.append({
            "timestamp": ts,
            "status": status,
            "direction": direction,
            "source_rule_ids": sorted({x.strip() for x in rule_ids if x.strip()}),
        })
    return pd.DataFrame(rows)


def aggregate_nison(df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for ts, group in df.groupby("timestamp", sort=True):
        passed = group[group["status"].astype(str).str.upper().eq("PASS")]
        dirs = sorted({d for d in (norm_direction(x) for x in passed["direction"]) if d})
        confirmation = dirs[0] if len(dirs) == 1 else ("CONFLICTED" if len(dirs) > 1 else "ABSENT")
        rows.append({
            "timestamp": ts,
            "confirmation": confirmation,
            "contradiction": bool((group["status"].astype(str).str.upper() == "FAIL").any()),
        })
    return pd.DataFrame(rows)


def brain_row(row: pd.Series) -> dict[str, Any]:
    keys = [
        "mtf_trend_score", "M5_trend_regime", "M15_trend_regime", "M30_trend_regime",
        "H1_trend_regime", "H4_trend_regime", "D1_trend_regime", "volume_available",
        "M5_volume_regime", "M15_volume_regime", "M30_volume_regime",
        "H1_volume_regime", "H4_volume_regime", "D1_volume_regime",
    ]
    out: dict[str, Any] = {}
    for key in keys:
        if key in row.index and pd.notna(row[key]):
            out[key] = row[key]
    return out


def run(*, h1: Path, murphy: Path, context: Path, nison: Path | None, output_dir: Path, tiz_mode: str = "optional") -> dict[str, Any]:
    if tiz_mode not in {"optional", "strict"}:
        raise ValueError("tiz_mode must be optional or strict")
    bars = load_csv(h1, {"timestamp", "open", "high", "low", "close"})
    m = load_csv(murphy, {"timestamp", "status", "direction"}, duplicates=True)
    ctx = load_csv(context, {"timestamp"})
    if "entry_price" not in ctx.columns and "close" in ctx.columns:
        ctx["entry_price"] = ctx["close"]
    if "atr" not in ctx.columns and "atr20" in ctx.columns:
        ctx["atr"] = ctx["atr20"]
    if nison is not None:
        n = load_csv(nison, {"timestamp", "status", "direction", "rule_id"}, duplicates=True)
        n_agg = aggregate_nison(n)
    else:
        n_agg = pd.DataFrame(columns=["timestamp", "confirmation", "contradiction"])

    merged = ctx.merge(aggregate_murphy(m), on="timestamp", how="left").merge(n_agg, on="timestamp", how="left")
    merged = merged[(merged["timestamp"].dt.year >= 2016) & (merged["timestamp"].dt.year <= 2024)].copy()

    brain = load_module(BRAIN_PATH, "recovered_decision_brain")
    gate = load_module(GATE_PATH, "murphy_governed_decision_gate_v1")

    events: list[dict[str, Any]] = []
    for _, row in merged.iterrows():
        query_as_of = row["timestamp"].isoformat()
        tiz_value = str(row.get("tiz_process_gate") or "").strip().upper()
        tiz_unverified = not tiz_value
        if tiz_unverified:
            tiz_value = "NOT_EVALUABLE"
        if tiz_mode == "strict" and tiz_value == "NOT_EVALUABLE":
            tiz_value = "FAIL"
        tiz = {"process_gate": tiz_value, "unverified": tiz_unverified, "mode": tiz_mode}
        risk = {"risk_status": row.get("risk_status", "NOT_EVALUABLE")}
        nison_evidence = {
            "confirmation": row.get("confirmation", "ABSENT"),
            "contradiction": bool(row.get("contradiction", False)),
        }
        murphy_evidence = {
            "status": row.get("status", "NOT_EVALUABLE"),
            "direction": row.get("direction"),
            "source_rule_ids": row.get("source_rule_ids", []),
        }
        result = gate.assess_with_murphy_gate(
            brain,
            row=brain_row(row),
            query_as_of=query_as_of,
            mode="development",
            murphy_evidence=murphy_evidence,
            nison_evidence=nison_evidence,
            tiz_evidence=tiz,
            risk_evidence=risk,
            provenance={"runner": "DEV_BACKTEST_RUNNER_GOVERNED_V2", "tiz_mode": tiz_mode},
            tiz_mode=tiz_mode,
        )
        execution = result.get("execution", {})
        events.append({
            "timestamp": query_as_of,
            "brain_bias": result.get("assessment", {}).get("directional_bias"),
            "brain_confidence": result.get("assessment", {}).get("confidence"),
            "murphy_status": row.get("status", "NOT_EVALUABLE"),
            "murphy_direction": row.get("direction"),
            "murphy_direction_source": result.get("murphy_direction_source"),
            "nison_confirmation": row.get("confirmation", "ABSENT"),
            "nison_contradiction": bool(row.get("contradiction", False)),
            "tiz_gate": tiz["process_gate"],
            "tiz_unverified": tiz_unverified,
            "tiz_mode": tiz_mode,
            "risk_gate": risk["risk_status"],
            "alignment": execution.get("alignment"),
            "final_trade_decision": execution.get("final_trade_decision"),
            "execution_eligible": bool(execution.get("execution_eligible", False)),
            "hard_blocks": json.dumps(execution.get("hard_blocks", [])),
            "needs_review": json.dumps(execution.get("needs_review", [])),
            "source_rule_ids": json.dumps(row.get("source_rule_ids", [])),
        })

    out = pd.DataFrame(events)
    output_dir.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_dir / "unified_78_events_2016_2024.csv", index=False)
    out.to_csv(output_dir / "decision_events_2016_2024.csv", index=False)
    executed = out[out["final_trade_decision"].isin(["EXECUTE", "EXECUTE_TIZ_UNVERIFIED"])].copy()
    executed.to_csv(output_dir / "executed_trades_2016_2024.csv", index=False)

    def count(mask):
        return int(mask.sum())

    funnel = {
        "input_events": int(len(out)),
        "murphy_directional": count(out["murphy_direction"].isin(["BULLISH", "BEARISH"])),
        "brain_aligned": count(out["alignment"].eq("ALIGNED")),
        "tiz_pass": count(out["tiz_gate"].eq("PASS")),
        "tiz_unverified": count(out["tiz_unverified"]),
        "risk_pass": count(out["risk_gate"].eq("PASS")),
        "needs_review": count(out["final_trade_decision"].eq("NEEDS_REVIEW")),
        "blocked": count(out["final_trade_decision"].eq("BLOCKED")),
        "executed": count(out["final_trade_decision"].isin(["EXECUTE", "EXECUTE_TIZ_UNVERIFIED"])),
    }
    manifest = {
        "runner": "DEV_BACKTEST_RUNNER_GOVERNED_V2",
        "window": "2016-2024",
        "tiz_mode": tiz_mode,
        "tiz_optional_default": True,
        "tiz_missing_action_optional": "EXECUTE_TIZ_UNVERIFIED when all other gates pass",
        "tiz_missing_action_strict": "BLOCKED",
        "2025_locked": True,
        "brain_modified": False,
        "direction_inference": False,
        "missing_direction_fail_closed": True,
        "risk_overridable": False,
        "official_profitability_claim_allowed": False,
        "note": "Optional TIZ does not claim psychological/process evaluation; it records TIZ_UNVERIFIED.",
    }
    (output_dir / "execution_funnel_2016_2024.json").write_text(json.dumps(funnel, indent=2), encoding="utf-8")
    (output_dir / "validation_manifest_2016_2024.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return {"funnel": funnel, "manifest": manifest}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--h1", required=True, type=Path)
    p.add_argument("--murphy", required=True, type=Path)
    p.add_argument("--context", required=True, type=Path)
    p.add_argument("--nison", type=Path)
    p.add_argument("--output-dir", required=True, type=Path)
    p.add_argument("--tiz-mode", choices=["optional", "strict"], default="optional")
    a = p.parse_args()
    print(json.dumps(run(h1=a.h1, murphy=a.murphy, context=a.context, nison=a.nison, output_dir=a.output_dir, tiz_mode=a.tiz_mode), indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())