from __future__ import annotations

"""Fail-closed contract gate for the canonical six-timeframe MTF source.

The gate verifies that the producer already serialized numeric fields expected by
Decision Brain. It deliberately performs no categorical-to-numeric translation,
no imputation, no scaling, and no direction generation.
"""

import argparse
from pathlib import Path
import numpy as np
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


def parse_aware_timestamps(
    values: pd.Series,
    *,
    label: str,
    error_prefix: str = "BLOCKED_MTF",
) -> pd.Series:
    """Normalize explicitly aware source timestamps to UTC; never assign a timezone."""
    normalized: list[pd.Timestamp] = []
    for index, value in values.items():
        try:
            parsed = pd.Timestamp(value)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError(
                f"{error_prefix}_INVALID_TIMESTAMP:{label}:row={index}:{value!r}"
            ) from exc
        if pd.isna(parsed):
            raise ValueError(
                f"{error_prefix}_INVALID_TIMESTAMP:{label}:row={index}:{value!r}"
            )
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise ValueError(
                f"{error_prefix}_TIMEZONE_PROVENANCE_UNRESOLVED:{label}:row={index}:{value!r}"
            )
        normalized.append(parsed.tz_convert("UTC"))
    return pd.Series(pd.DatetimeIndex(normalized), index=values.index, name=values.name)


def inspect(path: Path) -> dict[str, object]:
    df = pd.read_csv(path, low_memory=False)
    missing = sorted(set(REQUIRED) - set(df.columns))
    if missing:
        raise SystemExit(f"BLOCKED_MTF_MISSING_REQUIRED_FIELDS:{missing}")
    if "timestamp" not in df.columns:
        raise SystemExit("BLOCKED_MTF_MISSING_TIMESTAMP_COLUMN")

    report: dict[str, object] = {
        "status": "PASS",
        "path": str(path),
        "rows": int(len(df)),
        "required_fields": list(REQUIRED),
        "categorical_translation_applied": False,
        "imputation_applied": False,
        "scaling_applied": False,
        "direction_generated": False,
    }

    source_issues: list[str] = []
    for field in REQUIRED:
        raw = df[field]
        numeric = pd.to_numeric(raw, errors="coerce")
        blank_tokens = raw.astype("string").str.strip().eq("").fillna(False)
        missing_mask = raw.isna() | blank_tokens
        invalid_mask = numeric.isna() & ~missing_mask
        non_finite_mask = pd.Series(
            np.isinf(numeric.to_numpy(dtype=float)),
            index=df.index,
        )

        if missing_mask.any():
            rows = df.index[missing_mask].tolist()[:20]
            source_issues.append(
                f"BLOCKED_MTF_MISSING_SOURCE_VALUE:{field}:"
                f"count={int(missing_mask.sum())}:rows={rows}"
            )
        if invalid_mask.any():
            rows = df.index[invalid_mask].tolist()[:20]
            tokens = raw.loc[invalid_mask].astype("string").dropna().unique().tolist()[:20]
            source_issues.append(
                f"BLOCKED_MTF_NON_NUMERIC_SOURCE_FIELD:{field}:"
                f"count={int(invalid_mask.sum())}:rows={rows}:raw_tokens={tokens}"
            )
        if non_finite_mask.any():
            rows = df.index[non_finite_mask].tolist()[:20]
            source_issues.append(
                f"BLOCKED_MTF_NON_FINITE_SOURCE_FIELD:{field}:"
                f"count={int(non_finite_mask.sum())}:rows={rows}"
            )

    if source_issues:
        raise SystemExit(";".join(source_issues))

    try:
        timestamps = parse_aware_timestamps(df["timestamp"], label=str(path))
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    if timestamps.duplicated().any():
        raise SystemExit("BLOCKED_MTF_DUPLICATE_TIMESTAMP")

    report["min_timestamp"] = timestamps.min().isoformat()
    report["max_timestamp"] = timestamps.max().isoformat()
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mtf", required=True, type=Path)
    args = parser.parse_args()
    print(inspect(args.mtf))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
