from __future__ import annotations

"""Fail-closed schema gate for already-produced six-timeframe MTF source.

This validates numeric serialization and explicit timezone-aware timestamps only.
It does not prove broker-clock truth, producer formulas, or feature semantics.
"""

import argparse
import math
from pathlib import Path

import pandas as pd

REQUIRED = (
    "mtf_trend_score",
    "M5_trend_regime",
    "M15_trend_regime",
    "M30_trend_regime",
    "H1_trend_regime",
    "H4_trend_regime",
    "D1_trend_regime",
)


def _parse_explicitly_aware_utc(values: pd.Series) -> pd.Series:
    normalized: list[pd.Timestamp] = []
    for index, value in values.items():
        try:
            parsed = pd.Timestamp(value)
        except (TypeError, ValueError, OverflowError) as exc:
            raise SystemExit(f"BLOCKED_MTF_INVALID_TIMESTAMP:row={index}") from exc
        if pd.isna(parsed):
            raise SystemExit(f"BLOCKED_MTF_INVALID_TIMESTAMP:row={index}")
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise SystemExit(
                f"BLOCKED_MTF_TIMEZONE_PROVENANCE_UNRESOLVED_NAIVE_TIMESTAMP:row={index}"
            )
        normalized.append(parsed.tz_convert("UTC"))
    return pd.Series(pd.DatetimeIndex(normalized), index=values.index, name=values.name)


def inspect(path: Path) -> dict[str, object]:
    df = pd.read_csv(path, low_memory=False)
    required_columns = {"timestamp", *REQUIRED}
    missing = sorted(required_columns - set(df.columns))
    if missing:
        raise SystemExit(f"BLOCKED_MTF_MISSING_REQUIRED_FIELDS:{missing}")
    if df.empty:
        raise SystemExit("BLOCKED_MTF_EMPTY_SOURCE")

    report: dict[str, object] = {
        "status": "PASS_SCHEMA_AND_AWARE_TIMESTAMP_ONLY",
        "path": str(path),
        "rows": int(len(df)),
        "required_fields": ["timestamp", *REQUIRED],
        "categorical_translation_applied": False,
        "imputation_applied": False,
        "scaling_applied": False,
        "direction_generated": False,
        "broker_timezone_truth_verified": False,
        "producer_formula_verified": False,
    }

    for field in REQUIRED:
        numeric = pd.to_numeric(df[field], errors="coerce")
        if numeric.isna().any():
            bad = df.loc[numeric.isna(), field].astype("string").fillna("<NULL>").unique().tolist()
            raise SystemExit(
                f"BLOCKED_MTF_MISSING_OR_NON_NUMERIC_SOURCE_FIELD:{field}:"
                f"raw_tokens={bad[:20]}"
            )
        if not numeric.map(lambda value: math.isfinite(float(value))).all():
            raise SystemExit(f"BLOCKED_MTF_NON_FINITE_SOURCE_FIELD:{field}")

    timestamps = _parse_explicitly_aware_utc(df["timestamp"])
    if timestamps.duplicated().any():
        raise SystemExit("BLOCKED_MTF_DUPLICATE_TIMESTAMP")

    report["min_timestamp_utc"] = timestamps.min().isoformat()
    report["max_timestamp_utc"] = timestamps.max().isoformat()
    report["timestamp_values_are_explicitly_aware"] = True
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mtf", required=True, type=Path)
    args = parser.parse_args()
    print(inspect(args.mtf))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
