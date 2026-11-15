from __future__ import annotations

"""Fail-closed contract gate for the canonical six-timeframe MTF source.

The gate verifies that the producer already serialized numeric fields expected by
Decision Brain. It deliberately performs no categorical-to-numeric translation,
no imputation, no scaling, and no direction generation.
"""

import argparse
import json
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


def diagnose_field(df: pd.DataFrame, field: str, sample_limit: int = 10) -> dict[str, object]:
    """Classify source values without modifying or imputing them."""
    raw = df[field]
    text = raw.astype("string").str.strip()
    missing_mask = raw.isna() | text.eq("").fillna(False)
    numeric = pd.to_numeric(raw, errors="coerce")
    non_numeric_mask = ~missing_mask & numeric.isna()

    def samples(mask: pd.Series) -> list[dict[str, object]]:
        columns = [c for c in ("timestamp", field) if c in df.columns]
        return df.loc[mask, columns].head(sample_limit).astype("string").fillna("<NULL>").to_dict("records")

    return {
        "field": field,
        "missing_count": int(missing_mask.sum()),
        "non_numeric_count": int(non_numeric_mask.sum()),
        "missing_samples": samples(missing_mask),
        "non_numeric_samples": samples(non_numeric_mask),
    }


def inspect(path: Path) -> dict[str, object]:
    df = pd.read_csv(path, low_memory=False)
    missing = sorted(set(REQUIRED) - set(df.columns))
    if missing:
        raise SystemExit(f"BLOCKED_MTF_MISSING_REQUIRED_FIELDS:{missing}")

    diagnostics = [diagnose_field(df, field) for field in REQUIRED]
    failures = [item for item in diagnostics if item["missing_count"] or item["non_numeric_count"]]
    if failures:
        raise SystemExit(
            "BLOCKED_MTF_SOURCE_VALUE_DIAGNOSTICS:"
            + json.dumps(failures, ensure_ascii=False, sort_keys=True)
        )

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

    timestamps = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if timestamps.isna().any():
        raise SystemExit("BLOCKED_MTF_INVALID_TIMESTAMP")
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
