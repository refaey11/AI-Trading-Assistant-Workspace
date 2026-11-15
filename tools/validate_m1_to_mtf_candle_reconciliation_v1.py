from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

TIMEFRAMES = {
    "M5": ("5min", 5),
    "M15": ("15min", 15),
    "M30": ("30min", 30),
    "H1": ("1h", 60),
    "H4": ("4h", 240),
    "D1": ("1D", 1440),
}
DEVELOPMENT_START = "2016-01-01"
DEVELOPMENT_END_EXCLUSIVE = "2025-01-01"
OHLC = ("open", "high", "low", "close")


def _read_member(archive: zipfile.ZipFile, member: str) -> pd.DataFrame:
    try:
        with archive.open(member) as handle:
            return pd.read_csv(handle, low_memory=False)
    except KeyError as exc:
        raise SystemExit(f"ARCHIVE_MEMBER_MISSING member={member}") from exc


def _parse_bool(series: pd.Series) -> pd.Series:
    if pd.api.types.is_bool_dtype(series):
        return series.fillna(False)
    normalized = series.astype("string").str.strip().str.lower()
    return normalized.isin({"true", "1", "yes", "y"})


def reconcile_frames(m1: pd.DataFrame, actual: pd.DataFrame, timeframe: str) -> dict[str, Any]:
    if timeframe not in TIMEFRAMES:
        raise ValueError(f"unsupported timeframe: {timeframe}")
    freq, _nominal_minutes = TIMEFRAMES[timeframe]
    required_m1 = {"timestamp", *OHLC, "volume", "volume_available"}
    required_actual = {"timestamp", *OHLC, "volume", "m1_count", "bar_complete", "volume_available"}
    missing_m1 = sorted(required_m1 - set(m1.columns))
    missing_actual = sorted(required_actual - set(actual.columns))
    if missing_m1 or missing_actual:
        raise ValueError(f"missing columns m1={missing_m1} actual={missing_actual}")

    left = m1.copy()
    right = actual.copy()
    left["timestamp"] = pd.to_datetime(left["timestamp"], errors="coerce")
    right["timestamp"] = pd.to_datetime(right["timestamp"], errors="coerce")
    if left["timestamp"].isna().any() or right["timestamp"].isna().any():
        raise ValueError("invalid or unparseable timestamps")
    if getattr(left["timestamp"].dt, "tz", None) is not None or getattr(right["timestamp"].dt, "tz", None) is not None:
        raise ValueError("timezone-aware timestamps require an explicit source timezone contract; none is assumed here")

    left = left[(left["timestamp"] >= DEVELOPMENT_START) & (left["timestamp"] < DEVELOPMENT_END_EXCLUSIVE)].copy()
    right = right[(right["timestamp"] >= DEVELOPMENT_START) & (right["timestamp"] < DEVELOPMENT_END_EXCLUSIVE)].copy()
    if left["timestamp"].duplicated().any():
        raise ValueError("duplicate M1 timestamps in development window")
    if right["timestamp"].duplicated().any():
        raise ValueError(f"duplicate {timeframe} output timestamps in development window")
    if left.empty or right.empty:
        raise ValueError(f"empty development data for timeframe={timeframe}")

    for col in (*OHLC, "volume"):
        left[col] = pd.to_numeric(left[col], errors="coerce")
        right[col] = pd.to_numeric(right[col], errors="coerce")
    if left[list(OHLC)].isna().any().any() or right[list(OHLC)].isna().any().any():
        raise ValueError(f"missing/non-numeric OHLC in timeframe={timeframe}")

    left["volume_available"] = _parse_bool(left["volume_available"])
    right["volume_available"] = _parse_bool(right["volume_available"])
    right["bar_complete"] = _parse_bool(right["bar_complete"])
    left = left.sort_values("timestamp", kind="mergesort")
    left["bucket"] = left["timestamp"].dt.floor(freq)

    expected = left.groupby("bucket", sort=True).agg(
        open=("open", "first"),
        high=("high", "max"),
        low=("low", "min"),
        close=("close", "last"),
        volume=("volume", "sum"),
        m1_count=("timestamp", "size"),
        volume_available=("volume_available", "all"),
    ).reset_index().rename(columns={"bucket": "timestamp"})

    right = right.rename(columns={"m1_count": "m1_count_actual"})
    right["m1_count_actual"] = pd.to_numeric(right["m1_count_actual"], errors="coerce")

    joined = expected.merge(
        right[["timestamp", *OHLC, "volume", "m1_count_actual", "bar_complete", "volume_available"]],
        on="timestamp",
        how="outer",
        suffixes=("_expected", "_actual"),
        indicator=True,
        validate="one_to_one",
    )
    matched = joined[joined["_merge"] == "both"].copy()
    for col in OHLC:
        matched[f"{col}_match"] = np.isclose(
            matched[f"{col}_expected"].astype(float),
            matched[f"{col}_actual"].astype(float),
            rtol=0.0,
            atol=1e-9,
            equal_nan=False,
        )
    matched["m1_count_match"] = matched["m1_count"].eq(matched["m1_count_actual"])
    matched["volume_available_match"] = matched["volume_available_expected"].eq(matched["volume_available_actual"])
    volume_testable = matched["volume_available_expected"] & matched["volume_available_actual"]
    matched["volume_match"] = np.where(
        volume_testable,
        np.isclose(matched["volume_expected"], matched["volume_actual"], rtol=0.0, atol=1e-8),
        True,
    )
    match_cols = [f"{c}_match" for c in OHLC] + [
        "m1_count_match", "volume_available_match", "volume_match"
    ]
    matched["full_match"] = matched[match_cols].all(axis=1)

    mismatch_samples = []
    bad = matched[~matched["full_match"]].head(10)
    for _, row in bad.iterrows():
        mismatch_samples.append({
            "timestamp": row["timestamp"].isoformat(),
            "mismatch_fields": [c for c in match_cols if not bool(row[c])],
            "m1_count_expected": int(row["m1_count"]),
            "m1_count_actual": None if pd.isna(row["m1_count_actual"]) else int(row["m1_count_actual"]),
        })

    return {
        "timeframe": timeframe,
        "frequency": freq,
        "window": "2016-01-01 through 2024-12-31 inclusive",
        "m1_rows": int(len(left)),
        "expected_bars": int(len(expected)),
        "actual_bars": int(len(right)),
        "matched_timestamps": int(len(matched)),
        "missing_output_bars": int((joined["_merge"] == "left_only").sum()),
        "extra_output_bars": int((joined["_merge"] == "right_only").sum()),
        "ohlc_match_rows": int(matched[[f"{c}_match" for c in OHLC]].all(axis=1).sum()),
        "m1_count_match_rows": int(matched["m1_count_match"].sum()),
        "volume_available_match_rows": int(matched["volume_available_match"].sum()),
        "volume_testable_rows": int(volume_testable.sum()),
        "volume_match_rows": int(matched["volume_match"].sum()),
        "bar_complete_true_rows_reported": int(matched["bar_complete"].sum()),
        "bar_complete_false_rows_reported": int((~matched["bar_complete"]).sum()),
        "full_match_rows": int(matched["full_match"].sum()),
        "full_match_rate": float(matched["full_match"].mean()) if len(matched) else 0.0,
        "mismatch_samples": mismatch_samples,
    }


def run(m1_zip: Path, mtf_zip: Path) -> dict[str, Any]:
    with zipfile.ZipFile(m1_zip) as m1_archive, zipfile.ZipFile(mtf_zip) as mtf_archive:
        m1 = _read_member(m1_archive, "GBPUSD_M1_MASTER_2016_2026.csv")
        results = []
        for timeframe in TIMEFRAMES:
            actual = _read_member(mtf_archive, f"GBPUSD/GBPUSD_{timeframe}.csv")
            results.append(reconcile_frames(m1, actual, timeframe))
    return {
        "audit": "GBPUSD_M1_TO_MULTITF_CANDLE_RECONCILIATION_V1",
        "status": "COMPLETED_READ_ONLY",
        "scope": "GBPUSD raw M1 to existing M5/M15/M30/H1/H4/D1 OHLCV outputs; 2016-2024 only.",
        "timezone_policy": "No timezone localization or conversion; source timestamps are compared as stored.",
        "aggregation_contract_tested": "open=first, high=max, low=min, close=last, volume=sum; M1 count and volume availability flags checked.",
        "bar_complete_policy": "Reported as an existing output flag only; no completeness formula is inferred.",
        "oos_policy": "2025+ excluded entirely; no tuning or calibration.",
        "timeframes": results,
        "interpretation": [
            "This verifies data-output consistency, not the identity or exact source code of the historical producer.",
            "A complete match supports the documented M1 aggregation lineage for the tested symbol and window.",
            "The bar_complete flag is reported but not independently judged because its exact completeness contract is not assumed.",
            "Market Structure and MTF feature/score producers remain separate lineage questions.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m1-archive", required=True, type=Path)
    parser.add_argument("--mtf-archive", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = run(args.m1_archive, args.mtf_archive)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
