from __future__ import annotations

"""Fail-closed contract gate for the canonical six-timeframe MTF source.

The producer supplies six timeframe trend regimes as categorical state and
mtf_trend_score as a numeric field. This gate deliberately performs no
categorical-to-numeric translation, no imputation, no scaling, and no direction
generation. Annual source files may restart with an expected producer warm-up
prefix; missing values after the first fully-complete six-TF row within that
calendar-year segment remain a hard failure.
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
        "warmup_scope": "PER_CALENDAR_YEAR_SOURCE_SEGMENT",
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

    warmup_rows: dict[str, int] = {}
    invalid_rows: list[int] = []
    first_complete_timestamps: dict[str, str] = {}
    years = timestamps.dt.year.astype(int)

    for year in sorted(years.unique().tolist()):
        idx = df.index[years.eq(year)]
        year_complete = complete.loc[idx]
        if not year_complete.any():
            raise SystemExit(f"BLOCKED_MTF_NO_COMPLETE_SIX_TF_ROW:{year}")
        first_complete_idx = int(year_complete[year_complete].index[0])
        warmup_count = int((idx < first_complete_idx).sum())
        warmup_rows[str(year)] = warmup_count
        first_complete_timestamps[str(year)] = timestamps.loc[first_complete_idx].isoformat()
        post_warmup = idx >= first_complete_idx
        bad_idx = idx[post_warmup & ~complete.loc[idx]]
        invalid_rows.extend(int(x) for x in bad_idx.tolist())

    if invalid_rows:
        bad_counts = []
        bad_index = pd.Index(sorted(set(invalid_rows)))
        for field in NUMERIC_FIELDS:
            n = int(numeric.loc[bad_index, field].isna().sum())
            if n:
                bad_counts.append(f"{field}:{n}")
        for field in REGIME_FIELDS:
            n = int(categorical.loc[bad_index, field].isna().sum())
            if n:
                bad_counts.append(f"{field}:{n}")
        raise SystemExit("BLOCKED_MTF_MISSING_AFTER_WARMUP:" + ",".join(bad_counts))

    report["first_complete_timestamp_by_year"] = first_complete_timestamps
    report["warmup_rows_by_year"] = warmup_rows
    report["warmup_rows_total"] = int(sum(warmup_rows.values()))
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
