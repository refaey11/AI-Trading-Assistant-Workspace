from __future__ import annotations

"""Fail-closed contract gate for the canonical six-timeframe MTF source.

The producer supplies six timeframe trend regimes as categorical state and
mtf_trend_score as a numeric field. This gate deliberately performs no
categorical-to-numeric translation, no imputation, no scaling, and no direction
generation. Missing values after the first fully-complete six-TF row remain a
hard failure.
"""

import argparse
from pathlib import Path
import pandas as pd

REGIME_FIELDS = (
    "M5_trend_regime",
    "M15_trend_regime",
    "M30_trend_regime",
    "H1_trend_regime",
    "H4_trend_regime",
    "D1_trend_regime",
)
NUMERIC_FIELDS = ("mtf_trend_score",)
REQUIRED = NUMERIC_FIELDS + REGIME_FIELDS


def inspect(path: Path) -> dict[str, object]:
    df = pd.read_csv(path, low_memory=False)
    missing = sorted(set(REQUIRED) - set(df.columns))
    if missing:
        raise SystemExit(f"BLOCKED_MTF_MISSING_REQUIRED_FIELDS:{missing}")

    if "timestamp" not in df.columns:
        raise SystemExit("BLOCKED_MTF_MISSING_REQUIRED_FIELDS:['timestamp']")

    timestamps = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if timestamps.isna().any():
        raise SystemExit("BLOCKED_MTF_INVALID_TIMESTAMP")
    if timestamps.duplicated().any():
        raise SystemExit("BLOCKED_MTF_DUPLICATE_TIMESTAMP")

    report: dict[str, object] = {
        "status": "PASS",
        "path": str(path),
        "rows": int(len(df)),
        "required_fields": list(REQUIRED),
        "numeric_fields": list(NUMERIC_FIELDS),
        "categorical_fields": list(REGIME_FIELDS),
        "producer_regime_values_used_verbatim": True,
        "categorical_translation_applied": False,
        "imputation_applied": False,
        "scaling_applied": False,
        "direction_generated": False,
        "warmup_prefix_allowed": True,
    }

    numeric = pd.DataFrame(index=df.index)
    for field in NUMERIC_FIELDS:
        numeric[field] = pd.to_numeric(df[field], errors="coerce")

    categorical = pd.DataFrame(index=df.index)
    for field in REGIME_FIELDS:
        values = df[field].astype("string").str.strip()
        values = values.mask(values.eq(""))
        categorical[field] = values

    complete = numeric.notna().all(axis=1) & categorical.notna().all(axis=1)
    if not complete.any():
        raise SystemExit("BLOCKED_MTF_NO_COMPLETE_SIX_TF_ROW")

    first_complete_idx = int(complete.idxmax())
    post_warmup_invalid = (~complete) & (df.index >= first_complete_idx)
    if post_warmup_invalid.any():
        bad = []
        for field in NUMERIC_FIELDS:
            bad_count = int(numeric.loc[first_complete_idx:, field].isna().sum())
            if bad_count:
                bad.append(f"{field}:{bad_count}")
        for field in REGIME_FIELDS:
            bad_count = int(categorical.loc[first_complete_idx:, field].isna().sum())
            if bad_count:
                bad.append(f"{field}:{bad_count}")
        raise SystemExit("BLOCKED_MTF_MISSING_AFTER_WARMUP:" + ",".join(bad))

    report["first_complete_timestamp"] = timestamps.iloc[first_complete_idx].isoformat()
    report["warmup_rows"] = first_complete_idx
    report["complete_rows"] = int(complete.sum())
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
