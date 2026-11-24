from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import zipfile
from collections import Counter
from pathlib import Path

import pandas as pd

WINDOW_START = "2020-01-01"
WINDOW_END = "2021-01-01"
TIMEFRAMES = {
    "M5": ("5min", 5),
    "M15": ("15min", 15),
    "M30": ("30min", 30),
    "H1": ("1h", 60),
    "H4": ("4h", 240),
    "D1": ("1D", 1440),
}
OHLC = ("open", "high", "low", "close")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def archive_inventory(path: Path) -> list[dict]:
    with zipfile.ZipFile(path) as zf:
        return [
            {"member": x.filename, "size": x.file_size, "compressed_size": x.compress_size}
            for x in zf.infolist() if not x.is_dir()
        ]


def _normal_name(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(value).strip().lower())


def _read_m1_member(zf: zipfile.ZipFile) -> tuple[str, pd.DataFrame, dict]:
    candidates = [
        x for x in zf.infolist()
        if not x.is_dir() and x.filename.lower().endswith(".csv")
        and ("m1" in x.filename.lower() or "gbpusd" in x.filename.lower())
    ]
    if not candidates:
        candidates = [x for x in zf.infolist() if not x.is_dir() and x.filename.lower().endswith(".csv")]
    if not candidates:
        raise RuntimeError("NO_CSV_MEMBER_FOUND_IN_2020_ARCHIVE")

    last_error = None
    for info in candidates:
        try:
            raw = zf.read(info)
            sample = raw[:8192].decode("utf-8-sig", errors="replace")
            first = next(csv.reader(io.StringIO(sample)), [])
            normalized = {_normal_name(x) for x in first}
            has_header = bool({"open", "high", "low", "close"} <= normalized)
            frame = pd.read_csv(io.BytesIO(raw), header=0 if has_header else None, low_memory=False)
            if not has_header:
                if frame.shape[1] == 7:
                    frame.columns = ["date", "time", "open", "high", "low", "close", "volume"]
                elif frame.shape[1] == 6:
                    frame.columns = ["datetime", "open", "high", "low", "close", "volume"]
                else:
                    raise RuntimeError(f"UNRECOGNIZED_HEADERLESS_M1_COLUMN_COUNT={frame.shape[1]}")
            rename = {_normal_name(c): c for c in frame.columns}
            def find(*names: str):
                for name in names:
                    if name in rename:
                        return rename[name]
                return None
            date_col = find("date")
            time_col = find("time")
            datetime_col = find("timestamp", "datetime", "datetimeutc", "baropentime")
            if datetime_col:
                timestamps = pd.to_datetime(frame[datetime_col], errors="coerce", format="mixed")
            elif date_col and time_col:
                timestamps = pd.to_datetime(
                    frame[date_col].astype(str).str.strip() + " " + frame[time_col].astype(str).str.strip(),
                    errors="coerce", format="mixed"
                )
            else:
                raise RuntimeError("M1_TIMESTAMP_COLUMNS_NOT_RECOGNIZED")
            cols = {name: find(name) for name in OHLC}
            if any(v is None for v in cols.values()):
                raise RuntimeError("M1_OHLC_COLUMNS_NOT_RECOGNIZED")
            out = pd.DataFrame({"timestamp": timestamps})
            for name, col in cols.items():
                out[name] = pd.to_numeric(frame[col], errors="coerce")
            volume_col = find("volume", "tickvolume", "vol", "tickvol")
            if volume_col:
                out["volume"] = pd.to_numeric(frame[volume_col], errors="coerce")
            out = out[out["timestamp"].notna()].copy()
            out = out[(out["timestamp"] >= WINDOW_START) & (out["timestamp"] < WINDOW_END)].copy()
            if out.empty:
                raise RuntimeError("NO_2020_ROWS_IN_CANDIDATE_M1_MEMBER")
            metadata = {
                "member": info.filename,
                "raw_member_size": info.file_size,
                "header_detected": has_header,
                "original_columns": [str(x) for x in frame.columns],
                "volume_column_present": bool(volume_col),
                "timezone_policy": "timestamps parsed as stored; no localization or UTC conversion",
            }
            return info.filename, out, metadata
        except Exception as exc:
            last_error = f"{info.filename}: {type(exc).__name__}: {exc}"
    raise RuntimeError(f"NO_VALID_M1_CSV_MEMBER: {last_error}")


def _read_mtf_member(zf: zipfile.ZipFile, timeframe: str) -> tuple[str, pd.DataFrame]:
    # Strictly select GBPUSD, never the first matching timeframe from another symbol.
    candidates = [
        x for x in zf.infolist()
        if not x.is_dir() and x.filename.lower().endswith(".csv")
        and "gbpusd" in x.filename.lower()
        and re.search(rf"(^|[/_\\-]){timeframe.lower()}([._\\-]|$)", x.filename.lower())
    ]
    if len(candidates) != 1:
        raise RuntimeError(
            f"EXPECTED_EXACTLY_ONE_GBPUSD_MTF_MEMBER timeframe={timeframe}; "
            f"found={[x.filename for x in candidates]}"
        )
    info = candidates[0]
    frame = pd.read_csv(io.BytesIO(zf.read(info)), low_memory=False)
    cols = {_normal_name(c): c for c in frame.columns}
    if not all(k in cols for k in ("timestamp", "open", "high", "low", "close")):
        raise RuntimeError(f"GBPUSD_MTF_REQUIRED_COLUMNS_MISSING member={info.filename}")
    out = pd.DataFrame({
        "timestamp": pd.to_datetime(frame[cols["timestamp"]], errors="coerce", format="mixed")
    })
    for name in OHLC:
        out[name] = pd.to_numeric(frame[cols[name]], errors="coerce")
    for name in ("volume", "m1_count", "volume_available", "bar_complete"):
        if name in cols:
            out[name] = frame[cols[name]]
    out = out[out["timestamp"].notna()].copy()
    out = out[(out["timestamp"] >= WINDOW_START) & (out["timestamp"] < WINDOW_END)].copy()
    if out.empty:
        raise RuntimeError(f"NO_VALID_2020_GBPUSD_MTF_ROWS timeframe={timeframe}")
    return info.filename, out

def _bool_values(series: pd.Series) -> pd.Series:
    if pd.api.types.is_bool_dtype(series):
        return series.fillna(False)
    return series.astype("string").str.strip().str.lower().isin({"true", "1", "yes", "y"})


def duplicate_diagnostics(m1: pd.DataFrame) -> dict:
    duplicated = m1[m1["timestamp"].duplicated(keep=False)].copy()
    if duplicated.empty:
        return {
            "duplicate_timestamp_rows_including_first": 0,
            "duplicate_timestamp_extra_rows": 0,
            "duplicate_timestamp_groups": 0,
            "exact_duplicate_extra_rows": 0,
            "conflicting_duplicate_groups": 0,
            "sample_duplicate_groups": [],
        }
    value_cols = [c for c in ("open", "high", "low", "close", "volume") if c in duplicated.columns]
    groups = []
    exact_extra = 0
    conflicts = 0
    for ts, group in duplicated.groupby("timestamp", sort=True):
        distinct = group[value_cols].drop_duplicates()
        identical = len(distinct) == 1
        if identical:
            exact_extra += len(group) - 1
        else:
            conflicts += 1
        if len(groups) < 20:
            groups.append({
                "timestamp": str(ts),
                "rows": int(len(group)),
                "identical_values": bool(identical),
                "values": group[value_cols].to_dict(orient="records"),
            })
    return {
        "duplicate_timestamp_rows_including_first": int(len(duplicated)),
        "duplicate_timestamp_extra_rows": int(m1["timestamp"].duplicated().sum()),
        "duplicate_timestamp_groups": int(duplicated["timestamp"].nunique()),
        "exact_duplicate_extra_rows": int(exact_extra),
        "conflicting_duplicate_groups": int(conflicts),
        "sample_duplicate_groups": groups,
    }


def compare(m1: pd.DataFrame, actual: pd.DataFrame, timeframe: str, duplicate_policy: str) -> dict:
    freq, _ = TIMEFRAMES[timeframe]
    m1_diag = duplicate_diagnostics(m1)
    if m1_diag["conflicting_duplicate_groups"] > 0:
        return {
            "timeframe": timeframe,
            "status": "BLOCKED_CONFLICTING_DUPLICATE_M1_TIMESTAMPS",
            "duplicate_policy": duplicate_policy,
            **m1_diag,
        }
    if actual["timestamp"].duplicated().any():
        return {
            "timeframe": timeframe,
            "status": "BLOCKED_DUPLICATE_GBPUSD_MTF_TIMESTAMPS",
            "duplicate_mtf_rows": int(actual["timestamp"].duplicated().sum()),
        }
    source = m1.sort_values("timestamp", kind="mergesort").copy()
    if duplicate_policy == "collapse_exact_duplicate_rows":
        source = source.drop_duplicates(subset=["timestamp", "open", "high", "low", "close"] + (["volume"] if "volume" in source.columns else []), keep="first")
    elif source["timestamp"].duplicated().any():
        return {"timeframe": timeframe, "status": "BLOCKED_DUPLICATE_M1_TIMESTAMPS", **m1_diag}
    source["bucket"] = source["timestamp"].dt.floor(freq)
    aggregations = {
        "open": ("open", "first"), "high": ("high", "max"),
        "low": ("low", "min"), "close": ("close", "last"),
        "m1_count": ("timestamp", "size"),
    }
    if "volume" in source.columns:
        aggregations["volume"] = ("volume", "sum")
    expected = source.groupby("bucket", sort=True).agg(**aggregations).reset_index().rename(columns={"bucket": "timestamp"})
    actual = actual.copy().sort_values("timestamp", kind="mergesort")
    joined = expected.merge(actual, on="timestamp", how="outer", suffixes=("_expected", "_actual"), indicator=True)
    both = joined[joined["_merge"] == "both"].copy()
    # Diagnostic only: test fixed clock shifts without applying or endorsing one.
    shift_candidates = []
    actual_for_shift = actual[["timestamp", *OHLC]].copy()
    for offset_minutes in range(-14 * 60, 14 * 60 + 1, 15):
        shifted = expected[["timestamp", *OHLC]].copy()
        shifted["timestamp"] = shifted["timestamp"] + pd.Timedelta(minutes=offset_minutes)
        overlap = shifted.merge(actual_for_shift, on="timestamp", how="inner", suffixes=("_expected", "_actual"))
        if overlap.empty:
            exact_ohlc = 0
            median_close_error = None
        else:
            exact_rows = pd.Series(True, index=overlap.index)
            for field in OHLC:
                exact_rows &= (
                    (overlap[f"{field}_expected"].astype(float) -
                     overlap[f"{field}_actual"].astype(float)).abs() <= 1e-9
                )
            exact_ohlc = int(exact_rows.sum())
            median_close_error = float(
                (overlap["close_expected"].astype(float) -
                 overlap["close_actual"].astype(float)).abs().median()
            )
        shift_candidates.append({
            "expected_timestamp_shift_minutes": offset_minutes,
            "matched_timestamps": int(len(overlap)),
            "all_ohlc_exact_match_rows": exact_ohlc,
            "close_abs_error_median": median_close_error,
        })
    shift_candidates.sort(
        key=lambda x: (x["all_ohlc_exact_match_rows"], x["matched_timestamps"]),
        reverse=True,
    )
    stats = {
        "timeframe": timeframe,
        "mtf_timestamp_first": str(actual["timestamp"].min()),
        "mtf_timestamp_last": str(actual["timestamp"].max()),
        "mtf_volume_column_present": "volume" in actual.columns,
        "mtf_volume_nonzero_rows": int((pd.to_numeric(actual["volume"], errors="coerce").fillna(0) != 0).sum()) if "volume" in actual.columns else None,
        "mtf_volume_available_true_rows": int(_bool_values(actual["volume_available"]).sum()) if "volume_available" in actual.columns else None,
        "clock_shift_sensitivity_top_5": shift_candidates[:5],
        "mtf_sample_first_5": actual[["timestamp", *OHLC]].head(5).astype({"timestamp": str}).to_dict(orient="records"),
        "expected_sample_first_5": expected[["timestamp", *OHLC]].head(5).astype({"timestamp": str}).to_dict(orient="records"),
        "duplicate_policy": duplicate_policy,
        "source_m1_rows_2020_before_duplicate_policy": int(len(m1)),
        "source_m1_rows_2020_after_duplicate_policy": int(len(source)),
        "expected_bars_2020": int(len(expected)),
        "actual_bars_2020": int(len(actual)),
        "matched_timestamps": int(len(both)),
        "missing_output_bars": int((joined["_merge"] == "left_only").sum()),
        "extra_output_bars": int((joined["_merge"] == "right_only").sum()),
        **m1_diag,
    }
    checks = {}
    for col in OHLC:
        delta = (both[f"{col}_expected"].astype(float) - both[f"{col}_actual"].astype(float)).abs()
        checks[f"{col}_match_rows"] = int((delta <= 1e-9).sum())
        checks[f"{col}_abs_error_mean"] = float(delta.mean()) if len(delta) else None
        checks[f"{col}_abs_error_median"] = float(delta.median()) if len(delta) else None
        checks[f"{col}_abs_error_p95"] = float(delta.quantile(0.95)) if len(delta) else None
        checks[f"{col}_abs_error_max"] = float(delta.max()) if len(delta) else None
    if "m1_count" in actual.columns:
        checks["m1_count_match_rows"] = int(
            (pd.to_numeric(both["m1_count_expected"], errors="coerce") ==
             pd.to_numeric(both["m1_count_actual"], errors="coerce")).sum()
        )
    else:
        checks["m1_count_match_rows"] = None
    if "volume" in expected.columns and "volume" in actual.columns:
        checks["volume_match_rows"] = int((
            (pd.to_numeric(both["volume_expected"], errors="coerce") -
             pd.to_numeric(both["volume_actual"], errors="coerce")).abs() <= 1e-8
        ).sum())
    else:
        checks["volume_match_rows"] = None
    if "volume_available" in actual.columns:
        checks["actual_volume_available_true_rows"] = int(_bool_values(actual["volume_available"]).sum())
    full = [checks[f"{x}_match_rows"] == len(both) for x in OHLC]
    if checks["m1_count_match_rows"] is not None:
        full.append(checks["m1_count_match_rows"] == len(both))
    if checks["volume_match_rows"] is not None:
        full.append(checks["volume_match_rows"] == len(both))
    stats.update(checks)
    stats["status"] = (
        "EXACT_MATCH_ON_TESTED_FIELDS" if stats["missing_output_bars"] == 0
        and stats["extra_output_bars"] == 0 and len(both) == len(expected) and all(full)
        else "MISMATCH_OR_PARTIAL"
    )
    stats["interpretation"] = (
        "data equivalence only; a match does not prove this archive was the producer input or authenticate its clock"
    )
    return stats

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m1-archive", required=True, type=Path)
    parser.add_argument("--mtf-archive", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    with zipfile.ZipFile(args.m1_archive) as m1_zip, zipfile.ZipFile(args.mtf_archive) as mtf_zip:
        member, m1, member_meta = _read_m1_member(m1_zip)
        manifest_text = mtf_zip.read("MANIFEST.csv").decode("utf-8-sig", errors="replace") if "MANIFEST.csv" in mtf_zip.namelist() else "MISSING"
        readme_text = mtf_zip.read("README.json").decode("utf-8-sig", errors="replace") if "README.json" in mtf_zip.namelist() else "MISSING"
        comparisons = []
        duplicate_diag = duplicate_diagnostics(m1)
        # Preserve strict result and a separately-labelled sensitivity run that
        # collapses only byte-value-equivalent duplicate timestamp rows.
        duplicate_policy = (
            "collapse_exact_duplicate_rows"
            if duplicate_diag["conflicting_duplicate_groups"] == 0
            else "strict_block"
        )
        for tf in TIMEFRAMES:
            mtf_name, actual = _read_mtf_member(mtf_zip, tf)
            comparisons.append({
                "mtf_member": mtf_name,
                "strict": compare(m1, actual, tf, "strict_block"),
                "exact_duplicate_sensitivity": compare(m1, actual, tf, duplicate_policy),
            })
    report = {
        "audit": "DROPBOX_GBPUSD_HISTDATA_2020_VS_EXISTING_MTF_2016_2024_V1",
        "status": "COMPLETED_READ_ONLY",
        "scope": "Only the standalone 2020 GBPUSD M1 archive and the existing 2016-2024 MTF archive were downloaded. M1 rows were restricted to 2020. No 2025/2026 file or data was accessed.",
        "source_archive": {
            "name": args.m1_archive.name, "size_bytes": args.m1_archive.stat().st_size,
            "sha256": sha256(args.m1_archive), "members": archive_inventory(args.m1_archive),
            "selected_m1_member": member, **member_meta,
            "rows_2020": int(len(m1)), "first_timestamp": str(m1["timestamp"].min()),
            "last_timestamp": str(m1["timestamp"].max()),
            **duplicate_diagnostics(m1),
            "invalid_ohlc_rows": int(m1[list(OHLC)].isna().any(axis=1).sum()),
            "volume_present": "volume" in m1.columns,
            "volume_nonzero_rows": int((m1["volume"].fillna(0) != 0).sum()) if "volume" in m1.columns else None,
            "volume_zero_rows": int((m1["volume"].fillna(0) == 0).sum()) if "volume" in m1.columns else None,
        },
        "mtf_archive": {
            "name": args.mtf_archive.name, "size_bytes": args.mtf_archive.stat().st_size,
            "sha256": sha256(args.mtf_archive), "members": archive_inventory(args.mtf_archive),
            "manifest_text": manifest_text,
            "readme_text": readme_text,
        },
        "comparisons": comparisons,
        "governance": [
            "No timestamps were localized or converted to UTC.",
            "GBPUSD MTF member selection is exact and rejects ambiguous or cross-symbol matches.",
            "Duplicate timestamp sensitivity is reported separately; exact duplicates are never silently removed from the strict result.",
            "No provider timezone, broker timezone, DST, or clock semantics were inferred.",
            "A data match is not proof of actual source selection or original producer lineage.",
            "No strategy parameters, thresholds, features, or runtime code were changed.",
            "2025 remains locked OOS and was not accessed.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({
        "audit": report["audit"], "status": report["status"],
        "source_member": member, "source_rows_2020": len(m1),
        "comparisons": comparisons,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
