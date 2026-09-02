from __future__ import annotations

"""Fail-closed bounded validation for governed Murphy 34 historical fan-in.

This utility validates the *shape* and provenance of an already-produced
historical evidence envelope. It never computes missing indicators, never
creates proxy values, never tunes thresholds, and never uses 2025.
"""

from pathlib import Path
import sys
import pandas as pd

GOVERNED = {
    "MURPHY_0003", "MURPHY_0004", "MURPHY_0006", "MURPHY_0007",
    "MURPHY_0018", "MURPHY_0019", "MURPHY_0021", "MURPHY_0022",
    "MURPHY_0023", "MURPHY_0025", "MURPHY_0026", "MURPHY_0028",
    "MURPHY_0029", "MURPHY_0030", "MURPHY_0031", "MURPHY_0032",
    "MURPHY_0033", "MURPHY_0034", "MURPHY_0035", "MURPHY_0036",
    "MURPHY_0037", "MURPHY_0038", "MURPHY_0039", "MURPHY_0040",
    "MURPHY_0041", "MURPHY_0042", "MURPHY_0043", "MURPHY_0044",
    "MURPHY_0045", "MURPHY_0047", "MURPHY_0048", "MURPHY_0049",
    "MURPHY_0050", "MURPHY_0051",
}
ALLOWED_STATUS = {"PASS", "FAIL", "NOT_EVALUABLE", "CONFLICT"}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(2)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python MURPHY_34_BOUNDED_VALIDATION_V1.py <historical_fanin.csv>")
        return 2

    path = Path(sys.argv[1])
    if not path.is_file():
        fail(f"source file not found: {path}")

    df = pd.read_csv(path)
    required = {"timestamp", "source_rule_id", "status"}
    missing = required - set(df.columns)
    if missing:
        fail(f"missing required columns: {sorted(missing)}")

    ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if ts.isna().any():
        fail("invalid timestamp values present")

    if (ts.dt.year >= 2025).any():
        fail("2025 or later data detected; OOS lock violated")

    unknown = sorted(set(df["source_rule_id"].dropna().astype(str)) - GOVERNED)
    if unknown:
        fail(f"unknown/non-governed rule IDs present: {unknown}")

    bad_status = sorted(set(df["status"].dropna().astype(str)) - ALLOWED_STATUS)
    if bad_status:
        fail(f"unsupported status values present: {bad_status}")

    if df["timestamp"].duplicated().any() and "source_rule_id" not in df.columns:
        fail("duplicate timestamp policy cannot be evaluated")

    observed = set(df["source_rule_id"].dropna().astype(str))
    missing_rules = sorted(GOVERNED - observed)

    print(f"rows={len(df)}")
    print(f"unique_rule_ids={len(observed)}/{len(GOVERNED)}")
    print(f"min_timestamp={ts.min().isoformat()}")
    print(f"max_timestamp={ts.max().isoformat()}")
    print(f"missing_rule_ids={missing_rules}")
    print("PASS: bounded schema/provenance gate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
