from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

import pandas as pd


def _csv_members(path: str | Path) -> list[str]:
    with zipfile.ZipFile(path) as archive:
        return [name for name in archive.namelist() if name.lower().endswith(".csv")]


def _read_csv_from_zip(path: str | Path, *, required: set[str], preferred: str | None = None) -> pd.DataFrame:
    with zipfile.ZipFile(path) as archive:
        names = [n for n in archive.namelist() if n.lower().endswith(".csv")]
        if preferred:
            names = sorted(names, key=lambda n: (preferred.lower() not in Path(n).name.lower(), n))
        failures = []
        for name in names:
            try:
                with archive.open(name) as stream:
                    frame = pd.read_csv(stream)
                if required.issubset(set(frame.columns)):
                    frame["_source_member"] = name
                    return frame
                failures.append(f"{name}: missing {sorted(required - set(frame.columns))}")
            except Exception as exc:
                failures.append(f"{name}: {type(exc).__name__}: {exc}")
        raise ValueError("No CSV with required columns found: " + " | ".join(failures[:10]))


def _timestamps(frame: pd.DataFrame, label: str) -> pd.Series:
    values = pd.to_datetime(frame["timestamp"], utc=True, errors="coerce")
    if values.isna().any():
        raise ValueError(f"{label}: {int(values.isna().sum())} invalid timestamps")
    return values


def audit(m1_zip: str | Path, h1_zip: str | Path) -> dict:
    m1 = _read_csv_from_zip(m1_zip, required={"timestamp", "open", "high", "low", "close", "volume"}, preferred="M1")
    h1 = _read_csv_from_zip(h1_zip, required={"timestamp", "open", "high", "low", "close"}, preferred="H1")
    m1_ts = _timestamps(m1, "M1")
    h1_ts = _timestamps(h1, "H1")

    # Restrict all measured source rows to the development period; frozen 2025 OOS is excluded.
    m1 = m1.loc[m1_ts.dt.year.between(2016, 2024)].copy().reset_index(drop=True)
    m1_ts = m1_ts.loc[m1_ts.dt.year.between(2016, 2024)].reset_index(drop=True)
    h1 = h1.loc[h1_ts.dt.year.between(2016, 2024)].copy().reset_index(drop=True)
    h1_ts = h1_ts.loc[h1_ts.dt.year.between(2016, 2024)].reset_index(drop=True)

    m1 = m1.copy()
    m1["_ts"] = m1_ts
    m1["_volume"] = pd.to_numeric(m1["volume"], errors="coerce")
    invalid_volume = int(m1["_volume"].isna().sum())
    duplicate_m1 = int(m1["_ts"].duplicated(keep=False).sum())
    off_minute = int((m1["_ts"] != m1["_ts"].dt.floor("min")).sum())
    m1 = m1.sort_values("_ts").reset_index(drop=True)
    for col in ("open", "high", "low", "close"):
        m1[col] = pd.to_numeric(m1[col], errors="coerce")
    m1["_hour"] = m1["_ts"].dt.floor("h")
    hourly = m1.groupby("_hour").agg(
        m1_rows=("_ts", "size"),
        unique_minutes=("_ts", "nunique"),
        first_m1=("_ts", "min"),
        last_m1=("_ts", "max"),
        volume_sum=("_volume", "sum"),
        m1_open=("open", "first"),
        m1_high=("high", "max"),
        m1_low=("low", "min"),
        m1_close=("close", "last"),
    ).reset_index()
    hourly["minute_span"] = (
        (hourly["last_m1"] - hourly["first_m1"]).dt.total_seconds().div(60).add(1)
    )
    hourly["internal_missing_minutes"] = hourly["minute_span"] - hourly["unique_minutes"]
    hourly["contiguous_partial_hour"] = (
        hourly["unique_minutes"].lt(60) & hourly["internal_missing_minutes"].eq(0)
    )

    h1 = h1.copy()
    h1["_ts"] = h1_ts
    duplicate_h1 = int(h1["_ts"].duplicated(keep=False).sum())
    h1["_hour_floor"] = h1["_ts"].dt.floor("h")
    joined = h1.merge(hourly, left_on="_hour_floor", right_on="_hour", how="left")
    joined["m1_count"] = joined["m1_rows"].fillna(0).astype(int)
    joined["m1_complete_60"] = joined["unique_minutes"].eq(60)
    joined["latest_m1_minute"] = joined["last_m1"]
    joined["hour_end_utc"] = joined["_hour_floor"] + pd.Timedelta(hours=1)
    joined["m1_reaches_hour_end"] = joined["last_m1"].eq(joined["hour_end_utc"] - pd.Timedelta(minutes=1))
    joined["timestamp_equals_hour_start"] = joined["_ts"].eq(joined["_hour_floor"])
    joined["timestamp_equals_hour_end"] = joined["_ts"].eq(joined["hour_end_utc"])

    # Compare H1 OHLC to M1-derived OHLC for the timestamp's hour and prior hour.
    # This is diagnostic only and does not rewrite timestamps or trading inputs.
    for col in ("open", "high", "low", "close"):
        joined[f"{col}_match_current_hour"] = (
            pd.to_numeric(joined[col], errors="coerce").sub(joined[f"m1_{col}"]).abs().le(1e-8)
        )
    joined["h1_ohlc_all_match_current_hour"] = joined[
        [f"{col}_match_current_hour" for col in ("open", "high", "low", "close")]
    ].all(axis=1)
    prior_hour = hourly.copy()
    prior_hour["_hour"] = prior_hour["_hour"] + pd.Timedelta(hours=1)
    prior_hour = prior_hour.rename(columns={f"m1_{col}": f"prior_m1_{col}" for col in ("open", "high", "low", "close")})
    joined = joined.merge(
        prior_hour[["_hour", *[f"prior_m1_{col}" for col in ("open", "high", "low", "close")]]],
        left_on="_hour_floor", right_on="_hour", how="left", suffixes=("", "_prior_map")
    )
    for col in ("open", "high", "low", "close"):
        joined[f"{col}_match_prior_hour"] = (
            pd.to_numeric(joined[col], errors="coerce").sub(joined[f"prior_m1_{col}"]).abs().le(1e-8)
        )
    joined["h1_ohlc_all_match_prior_hour"] = joined[
        [f"{col}_match_prior_hour" for col in ("open", "high", "low", "close")]
    ].all(axis=1)

    # These are descriptive diagnostics only. They do not alter or certify a trading input.
    report = {
        "audit": "READ_ONLY_M1_TO_H1_COMPLETENESS_AND_TIMESTAMP_2016_2024_ONLY",
        "development_year_scope": "2016-2024; 2025 OOS and 2026 rows excluded",
        "m1_archive": str(m1_zip),
        "h1_archive": str(h1_zip),
        "m1_csv_member": str(m1["_source_member"].iloc[0]),
        "h1_csv_member": str(h1["_source_member"].iloc[0]),
        "m1_rows": int(len(m1)),
        "h1_rows": int(len(h1)),
        "m1_invalid_volume_rows": invalid_volume,
        "m1_duplicate_timestamp_rows": duplicate_m1,
        "m1_off_minute_timestamp_rows": off_minute,
        "h1_duplicate_timestamp_rows": duplicate_h1,
        "active_m1_hours": int(len(hourly)),
        "active_hours_with_exactly_60_unique_minutes": int(hourly["unique_minutes"].eq(60).sum()),
        "active_hours_with_less_than_60_unique_minutes": int(hourly["unique_minutes"].lt(60).sum()),
        "active_hours_with_more_than_60_unique_minutes": int(hourly["unique_minutes"].gt(60).sum()),
        "partial_hours_with_internal_missing_minutes": int(hourly["internal_missing_minutes"].gt(0).sum()),
        "partial_hours_contiguous_from_first_to_last_observed_minute": int(hourly["contiguous_partial_hour"].sum()),
        "m1_unique_minutes_per_hour_distribution": {
            str(int(k)): int(v) for k, v in hourly["unique_minutes"].value_counts().sort_index().items()
        },
        "h1_rows_with_matching_m1_hour": int(joined["m1_rows"].notna().sum()),
        "h1_rows_with_60_unique_m1_minutes": int(joined["m1_complete_60"].sum()),
        "h1_rows_where_m1_reaches_minute_59": int(joined["m1_reaches_hour_end"].sum()),
        "h1_rows_where_all_ohlc_matches_same_hour_m1_aggregation": int(joined["h1_ohlc_all_match_current_hour"].sum()),
        "h1_rows_where_all_ohlc_matches_previous_hour_m1_aggregation": int(joined["h1_ohlc_all_match_prior_hour"].sum()),
        "h1_ohlc_field_matches_same_hour_m1_aggregation": {
            col: int(joined[f"{col}_match_current_hour"].sum()) for col in ("open", "high", "low", "close")
        },
        "h1_rows_with_all_ohlc_matching_same_hour_and_60_m1_minutes": int(
            (joined["h1_ohlc_all_match_current_hour"] & joined["m1_complete_60"]).sum()
        ),
        "ohlc_comparison_tolerance": "absolute price difference <= 1e-8 for each OHLC field",
        "h1_timestamp_equals_hour_start_rows": int(joined["timestamp_equals_hour_start"].sum()),
        "h1_timestamp_equals_hour_end_rows": int(joined["timestamp_equals_hour_end"].sum()),
        "h1_timestamp_sample": [
            {
                "h1_timestamp": row["_ts"].isoformat(),
                "m1_rows_in_floor_hour": int(row["m1_count"]),
                "first_m1": row["first_m1"].isoformat() if pd.notna(row["first_m1"]) else None,
                "last_m1": row["last_m1"].isoformat() if pd.notna(row["last_m1"]) else None,
                "hour_end_utc": row["hour_end_utc"].isoformat(),
                "m1_reaches_minute_59": bool(row["m1_reaches_hour_end"]),
                "h1_ohlc_matches_same_hour_m1": bool(row["h1_ohlc_all_match_current_hour"]),
                "h1_ohlc_matches_previous_hour_m1": bool(row["h1_ohlc_all_match_prior_hour"]),
                "same_hour_m1_volume_sum": float(row["volume_sum"]) if pd.notna(row["volume_sum"]) else None,
                "same_hour_m1_unique_minutes": int(row["unique_minutes"]) if pd.notna(row["unique_minutes"]) else 0,
            }
            for _, row in joined.head(20).iterrows()
        ],
        "interpretation": [
            "A count of 60 unique M1 timestamps is a completeness indicator for an hour, not proof of exchange/session correctness.",
            "Partial hours are split into contiguous partial spans versus hours with internal missing minutes; do not assume all partial hours are market closures.",
            "The M1 aggregation bucket starts at the H1 timestamp and its volume is only complete at the following hour boundary; using it at the bucket start is look-ahead.",
            "An H1 timestamp at the hour start cannot be treated as an available completed H1 bar until the corresponding hour has closed.",
            "Same-hour versus prior-hour OHLC matches are source-alignment diagnostics; mismatches do not prove a different timestamp convention unless source OHLC lineage is known.",
            "This report is diagnostic only; it does not change volume calculations, thresholds, runtime behavior, or any 2025/OOS artifact.",
        ],
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m1-zip", required=True)
    parser.add_argument("--h1-zip", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    report = audit(args.m1_zip, args.h1_zip)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
