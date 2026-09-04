from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

EXPECTED = {"MURPHY_0003", "MURPHY_0004"}
START = pd.Timestamp("2016-01-01", tz="UTC")
END = pd.Timestamp("2024-12-31 23:59:59", tz="UTC")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    df = pd.read_csv(args.input, low_memory=False)
    required = {"timeframe", "pivot_timestamp", "availability_timestamp", "rule_id", "status"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise SystemExit(f"BLOCKED_MISSING_COLUMNS:{','.join(missing)}")

    pivot = pd.to_datetime(df["pivot_timestamp"], utc=True, errors="coerce")
    avail = pd.to_datetime(df["availability_timestamp"], utc=True, errors="coerce")
    bad_time = pivot.isna() | avail.isna()
    future_2025 = avail.dt.year.eq(2025)
    outside = ~avail.between(START, END, inclusive="both")
    pre_availability = avail < pivot
    rules = set(df["rule_id"].astype(str).str.upper().unique())
    unexpected_rules = sorted(rules - EXPECTED)
    dup_key = df.assign(_avail=avail).duplicated(["_avail", "rule_id", "timeframe"], keep=False)

    yearly = avail.dt.year.value_counts(dropna=True).sort_index().astype(int).to_dict()
    rule_counts = df["rule_id"].astype(str).str.upper().value_counts().to_dict()
    status_counts = df["status"].astype(str).str.upper().value_counts().to_dict()

    failures = {
        "missing_or_invalid_time": int(bad_time.sum()),
        "outside_2016_2024": int(outside.sum()),
        "2025_rows": int(future_2025.sum()),
        "availability_before_pivot": int(pre_availability.sum()),
        "unexpected_rule_ids": unexpected_rules,
    }
    # Duplicate event keys are informational until the downstream join contract defines whether
    # multiple timeframes at the same availability instant are distinct evidence rows.
    report = {
        "schema_version": "1.0",
        "status": "PASS" if not any([bad_time.any(), outside.any(), future_2025.any(), pre_availability.any(), unexpected_rules]) else "BLOCKED",
        "scope": "MURPHY_0003_0004",
        "source_file": str(args.input),
        "rows": int(len(df)),
        "rules": sorted(rules),
        "rule_row_counts": {k: int(v) for k, v in sorted(rule_counts.items())},
        "status_counts": {k: int(v) for k, v in sorted(status_counts.items())},
        "availability_year_counts": {str(k): int(v) for k, v in yearly.items()},
        "failures": failures,
        "duplicate_event_key_rows_informational": int(dup_key.sum()),
        "strict_asof_join_verified": False,
        "decision_brain_promotion": False,
        "synthetic_evidence_generated": False,
        "note": "This audit proves source timestamp hygiene only. It does not prove strict as-of relative to the final Decision Brain join/entry contract and therefore does not promote the rules.",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
