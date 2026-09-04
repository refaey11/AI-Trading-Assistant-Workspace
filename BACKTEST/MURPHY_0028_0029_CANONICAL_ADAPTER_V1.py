from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

LOCKED_YEAR = 2025
RULES = {
    "MURPHY_0028": ("rule_0028_status", "BEARISH", "HIGH", "BEARISH_WARNING"),
    "MURPHY_0029": ("rule_0029_status", "BULLISH", "LOW", "BULLISH_WARNING"),
}
REQUIRED = {
    "timeframe", "divergence_type", "pivot_type", "pivot_1_timestamp",
    "pivot_2_timestamp", "availability_timestamp", "source_pivot_file",
    "source_oscillator", "status",
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--report", type=Path, required=True)
    args = ap.parse_args()

    df = pd.read_csv(args.input, low_memory=False)
    missing = sorted(REQUIRED - set(df.columns))
    if missing:
        raise SystemExit(f"BLOCKED_0028_0029_MISSING_COLUMNS:{','.join(missing)}")

    for c in ["pivot_1_timestamp", "pivot_2_timestamp", "availability_timestamp"]:
        df[c] = pd.to_datetime(df[c], utc=True, errors="coerce", format="mixed")
    if df[["pivot_1_timestamp", "pivot_2_timestamp", "availability_timestamp"]].isna().any().any():
        raise SystemExit("BLOCKED_0028_0029_NULL_EVENT_TIME")
    years = df["availability_timestamp"].dt.year
    if years.eq(LOCKED_YEAR).any() or years.dropna().lt(2020).any() or years.dropna().gt(2024).any():
        raise SystemExit("BLOCKED_0028_0029_OUTSIDE_2020_2024_OR_2025")
    if not (df["availability_timestamp"] >= df["pivot_1_timestamp"]).all():
        raise SystemExit("BLOCKED_0028_0029_ASOF_PIVOT1")
    if not (df["availability_timestamp"] >= df["pivot_2_timestamp"]).all():
        raise SystemExit("BLOCKED_0028_0029_ASOF_PIVOT2")
    if df.duplicated().any():
        raise SystemExit("BLOCKED_0028_0029_DUPLICATE_EVIDENCE")

    out = []
    for rid, (status_col, div_type, piv_type, warning) in RULES.items():
        part = df.loc[
            (df["divergence_type"].astype(str).str.upper() == div_type)
            & (df["pivot_type"].astype(str).str.upper() == piv_type)
            & (df[status_col].astype(str).str.upper() == "PASS")
        ].copy()
        part["timestamp"] = part["availability_timestamp"]
        part["source_rule_id"] = rid
        part["rule_status"] = "PASS"
        part["direction"] = div_type
        part["signal"] = warning
        part["evidence_status"] = part["status"].astype(str)
        part["source_artifact"] = str(args.input)
        part["evidence_available_at"] = part["availability_timestamp"]
        part["strict_asof_verified"] = True
        part["synthetic_evidence"] = False
        part["future_2025_used"] = False
        out.append(part)

    if not out:
        raise SystemExit("BLOCKED_0028_0029_NO_EVENT_OUTPUT")

    combined = pd.concat(out, ignore_index=True, sort=False)
    combined = combined.sort_values(["timestamp", "source_rule_id"], kind="mergesort").reset_index(drop=True)
    combined["timestamp"] = combined["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S%z")
    combined["evidence_available_at"] = combined["evidence_available_at"].dt.strftime("%Y-%m-%d %H:%M:%S%z")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(args.output, index=False)

    counts = combined.groupby("source_rule_id").size().to_dict()
    report = {
        "status": "PASS",
        "rules": sorted(RULES),
        "rows": int(len(combined)),
        "rule_row_counts": {k: int(v) for k, v in sorted(counts.items())},
        "window": "2020-2024",
        "source_artifact": str(args.input),
        "strict_asof_verified": True,
        "availability_at_or_after_both_pivots": True,
        "duplicate_evidence": False,
        "synthetic_evidence_generated": False,
        "direction_generated": False,
        "future_2025_used": False,
        "decision_brain_promotion": False,
        "fan_in_promotion": False,
        "note": "Adapter preserves existing evaluator semantics and provenance; it does not rewrite evaluator logic or invent evidence.",
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
