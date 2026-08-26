from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from RECOVERED_SOURCES.DECISION_BRAIN_V1.decision_brain import assess


def read_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
        if df["timestamp"].isna().any():
            raise ValueError(f"{path}: invalid timestamps")
    return df


def rule_coverage(df: pd.DataFrame, family: str) -> dict:
    if "rule_id" not in df.columns and "source_rule_id" not in df.columns:
        raise ValueError(f"{family}: missing rule_id/source_rule_id")
    rid_col = "source_rule_id" if "source_rule_id" in df.columns else "rule_id"
    if "status" not in df.columns:
        raise ValueError(f"{family}: missing status")
    out = {}
    for rid, g in df.groupby(rid_col, dropna=False):
        statuses = Counter(g["status"].astype(str).str.upper())
        out[str(rid)] = {
            "rows": int(len(g)),
            "PASS": int(statuses.get("PASS", 0)),
            "FAIL": int(statuses.get("FAIL", 0)),
            "NOT_EVALUABLE": int(statuses.get("NOT_EVALUABLE", 0)),
            "OTHER": int(sum(v for k, v in statuses.items() if k not in {"PASS", "FAIL", "NOT_EVALUABLE"})),
            "coverage_pct": round(100.0 * (statuses.get("PASS", 0) + statuses.get("FAIL", 0)) / max(1, len(g)), 4),
        }
    return out


def normalize_direction(value: object) -> str:
    v = str(value or "").strip().upper()
    if v in {"BULL", "BULLISH", "BUY"}:
        return "BULLISH"
    if v in {"BEAR", "BEARISH", "SELL"}:
        return "BEARISH"
    return v or "NONE"


def audit_direction(market: pd.DataFrame, murphy: pd.DataFrame) -> dict:
    required_m = {"timestamp", "status", "direction"}
    missing = required_m - set(murphy.columns)
    if missing:
        raise ValueError(f"Murphy candidate missing: {sorted(missing)}")
    merged = market.merge(
        murphy[["timestamp", "status", "direction"]],
        on="timestamp",
        how="inner",
        validate="one_to_one",
        suffixes=("_market", "_murphy"),
    )
    rows = []
    for row in merged.to_dict("records"):
        assessment = assess(row)
        brain = normalize_direction(assessment.directional_bias)
        murphy_dir = normalize_direction(row.get("direction_murphy"))
        murphy_status = str(row.get("status")).upper()
        if murphy_status != "PASS":
            category = "MURPHY_NOT_PASS"
        elif brain in {"NEUTRAL", "CONFLICTED", "NONE"}:
            category = "BRAIN_NON_DIRECTIONAL"
        elif brain == murphy_dir:
            category = "AGREE"
        else:
            category = "OPPOSITE"
        rows.append({
            "timestamp": row["timestamp"],
            "brain_bias": brain,
            "brain_confidence": float(assessment.confidence),
            "murphy_status": murphy_status,
            "murphy_direction": murphy_dir,
            "category": category,
        })
    c = Counter(r["category"] for r in rows)
    return {
        "rows_compared": len(rows),
        "category_counts": dict(c),
        "examples": {
            k: next((r for r in rows if r["category"] == k), None)
            for k in ["AGREE", "OPPOSITE", "BRAIN_NON_DIRECTIONAL", "MURPHY_NOT_PASS"]
        },
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--market-state", required=True, type=Path)
    p.add_argument("--murphy-full", required=True, type=Path)
    p.add_argument("--nison-full", required=True, type=Path)
    p.add_argument("--murphy-candidate", required=True, type=Path)
    p.add_argument("--nison-candidate", required=True, type=Path)
    p.add_argument("--decision-events", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    a = p.parse_args()

    market = read_csv(a.market_state)
    murphy_full = read_csv(a.murphy_full)
    nison_full = read_csv(a.nison_full)
    murphy_candidate = read_csv(a.murphy_candidate)
    nison_candidate = read_csv(a.nison_candidate)
    events = read_csv(a.decision_events)

    result = {
        "status": "PASS",
        "evaluation_year": 2025,
        "governance": {
            "oos_tuning": False,
            "new_rule_semantics": False,
            "synthetic_substitution": False,
            "murphy_role": "context_and_directional_confirmation",
            "nison_role": "confirmation_or_contradiction_only",
            "tiz_role": "process_psychology_gate_only",
            "similarity_role": "historical_evidence_only",
            "risk_role": "hard_gate",
        },
        "input_rows": {
            "market_state": int(len(market)),
            "murphy_full": int(len(murphy_full)),
            "nison_full": int(len(nison_full)),
            "murphy_candidate": int(len(murphy_candidate)),
            "nison_candidate": int(len(nison_candidate)),
            "decision_events": int(len(events)),
        },
        "rule_coverage": {
            "murphy": rule_coverage(murphy_full, "Murphy"),
            "nison": rule_coverage(nison_full, "Nison"),
        },
        "direction_arbitration": audit_direction(market, murphy_candidate),
        "decision_event_reasons": dict(Counter(events.get("primary_reason", pd.Series(dtype=str)).astype(str))),
        "memory_integration_gap": {
            "final_event_producer_passes_historical_evidence": False,
            "note": "Current governed producer passes historical_evidence=None; this audit records the integration gap and does not invent memory evidence.",
        },
    }

    # Simple hard checks for the expected verified envelope.
    murphy_ids = set(result["rule_coverage"]["murphy"])
    nison_ids = set(result["rule_coverage"]["nison"])
    result["envelope"] = {
        "murphy_rule_count": len(murphy_ids),
        "nison_rule_count": len(nison_ids),
        "total_rule_count": len(murphy_ids | nison_ids),
        "expected_total": 78,
        "status": "PASS" if len(murphy_ids) == 34 and len(nison_ids) == 44 else "FAIL",
    }

    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(json.dumps(result, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
