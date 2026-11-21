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
    candidates = [
        x for x in zf.infolist()
        if not x.is_dir() and x.filename.lower().endswith(".csv")
        and re.search(rf"(^|[/_\\-]){timeframe.lower()}([._\\-]|$)", x.filename.lower())
    ]
    if not candidates:
        candidates = [
            x for x in zf.infolist()
            if not x.is_dir() and x.filename.lower().endswith(".csv")
            and timeframe.lower() in x.filename.lower()
        ]
    if not candidates:
        raise RuntimeError(f"MTF_MEMBER_NOT_FOUND timeframe={timeframe}")
    for info in candidates:
        try:
            frame = pd.read_csv(io.BytesIO(zf.read(info)), low_memory=False)
            cols = {_normal_name(c): c for c in frame.columns}
            if not all(k in cols for k in ("timestamp", "open", "high", "low", "close")):
                continue
            out = pd.DataFrame({"timestamp": pd.to_datetime(frame[cols["timestamp"]], errors="coerce", format="mixed")})
            for name in OHLC:
                out[name] = pd.to_numeric(frame[cols[name]], errors="coerce")
            for name in ("volume", "m1_count", "volume_available", "bar_complete"):
                if name in cols:
                    out[name] = frame[cols[name]]
            out = out[out["timestamp"].notna()].copy()
            out = out[(out["timestamp"] >= WINDOW_START) & (out["timestamp"] < WINDOW_END)].copy()
            if not out.empty:
                return info.filename, out
        except Exception:
            continue
    raise RuntimeError(f"NO_VALID_2020_MTF_CSV timeframe={timeframe}")


def _bool_values(series: pd.Series) -> pd.Series:
    if pd.api.types.is_bool_dtype(series):
        return series.fillna(False)
    return series.astype("string").str.strip().str.lower().isin({"true", "1", "yes", "y"})


def compare(m1: pd.DataFrame, actual: pd.DataFrame, timeframe: str) -> dict:
    freq, _ = TIMEFRAMES[timeframe]
    if m1["timestamp"].duplicated().any():
        return {"timeframe": timeframe, "status": "BLOCKED_DUPLICATE_M1_TIMESTAMPS",
                "duplicate_m1_rows": int(m1["timestamp"].duplicated().sum())}
    if actual["timestamp"].duplicated().any():
        return {"timeframe": timeframe, "status": "BLOCKED_DUPLICATE_MTF_TIMESTAMPS",
                "duplicate_mtf_rows": int(actual["timestamp"].duplicated().sum())}
    source = m1.sort_values("timestamp", kind="mergesort").copy()
    source["bucket"] = source["timestamp"].dt.floor(freq)
    aggregations = {
        "open": ("open", "first"), "high": ("high", "max"),
        "low": ("low", "min"), "close": ("close", "last"),
        "m1_count": ("timestamp", "size"),
    }
    if "volume" in source.columns:
        aggregations["volume"] = ("volume", "sum")
    expected = source.groupby("bucket", sort=True).agg(**aggregations).reset_index().rename(columns={"bucket": "timestamp"})
    actual = actual.copy()
    actual = actual.sort_values("timestamp", kind="mergesort")
    joined = expected.merge(actual, on="timestamp", how="outer", suffixes=("_expected", "_actual"), indicator=True)
    both = joined[joined["_merge"] == "both"].copy()
    stats = {
        "timeframe": timeframe,
        "source_m1_rows_2020": int(len(source)),
        "expected_bars_2020": int(len(expected)),
        "actual_bars_2020": int(len(actual)),
        "matched_timestamps": int(len(both)),
        "missing_output_bars": int((joined["_merge"] == "left_only").sum()),
        "extra_output_bars": int((joined["_merge"] == "right_only").sum()),
    }
    checks = {}
    for col in OHLC:
        checks[f"{col}_match_rows"] = int(pd.Series(
            (both[f"{col}_expected"].astype(float) - both[f"{col}_actual"].astype(float)).abs() <= 1e-9
        ).sum())
    checks["m1_count_match_rows"] = int(
        (pd.to_numeric(both["m1_count_expected"], errors="coerce") ==
         pd.to_numeric(both.get("m1_count_actual", pd.Series(index=both.index, dtype=float)), errors="coerce")).sum()
    ) if "m1_count" in actual.columns else None
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
    stats["status"] = "EXACT_MATCH_ON_TESTED_FIELDS" if stats["missing_output_bars"] == 0 and stats["extra_output_bars"] == 0 and len(both) == len(expected) and all(full) else "MISMATCH_OR_PARTIAL"
    stats["interpretation"] = "data equivalence only; a match does not prove this archive was the producer input or authenticate its clock"
    return stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m1-archive", required=True, type=Path)
    parser.add_argument("--mtf-archive", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    with zipfile.ZipFile(args.m1_archive) as m1_zip, zipfile.ZipFile(args.mtf_archive) as mtf_zip:
        member, m1, member_meta = _read_m1_member(m1_zip)
        comparisons = []
        for tf in TIMEFRAMES:
            mtf_name, actual = _read_mtf_member(mtf_zip, tf)
            comparisons.append({"mtf_member": mtf_name, **compare(m1, actual, tf)})
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
            "duplicate_timestamp_rows": int(m1["timestamp"].duplicated().sum()),
            "invalid_ohlc_rows": int(m1[list(OHLC)].isna().any(axis=1).sum()),
            "volume_present": "volume" in m1.columns,
            "volume_nonzero_rows": int((m1["volume"].fillna(0) != 0).sum()) if "volume" in m1.columns else None,
            "volume_zero_rows": int((m1["volume"].fillna(0) == 0).sum()) if "volume" in m1.columns else None,
        },
        "mtf_archive": {
            "name": args.mtf_archive.name, "size_bytes": args.mtf_archive.stat().st_size,
            "sha256": sha256(args.mtf_archive), "members": archive_inventory(args.mtf_archive),
        },
        "comparisons": comparisons,
        "governance": [
            "No timestamps were localized or converted to UTC.",
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
