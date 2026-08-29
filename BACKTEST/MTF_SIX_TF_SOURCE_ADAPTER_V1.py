from __future__ import annotations

"""Strict adapter/inspector for the canonical six-timeframe source package."""

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

import pandas as pd

SIX_TF = ("M5", "M15", "M30", "H1", "H4", "D1")
CANONICAL_SYMBOL = "GBPUSD"
SYMBOL_RE = re.compile(r"(?<![A-Z0-9])([A-Z]{6})(?![A-Z0-9])")
TIMEFRAME_RE = re.compile(r"(?<![A-Z0-9])(D1|H4|H1|M30|M15|M5)(?![A-Z0-9])", re.I)
TIMEFRAME_COLUMNS = {"timeframe", "tf", "period", "interval"}
SYMBOL_COLUMNS = {"symbol", "instrument", "pair", "ticker"}
TIMESTAMP_COLUMNS = ("timestamp", "datetime")
OHLC = ("open", "high", "low", "close")


def infer_tf_from_text(text: str) -> str | None:
    matches = [m.upper() for m in TIMEFRAME_RE.findall(text.upper())]
    return matches[0] if matches else None


def infer_symbol_from_text(text: str) -> str | None:
    for symbol in SYMBOL_RE.findall(text.upper()):
        if symbol in {CANONICAL_SYMBOL, "EURUSD", "USDCAD", "USDJPY", "XAUUSD"}:
            return symbol
    return None


def normalize_ohlc(columns: list[str]) -> dict[str, str]:
    lower = {str(c).strip().lower(): str(c) for c in columns}
    return {field: lower[field] for field in OHLC if field in lower}


def sha256(path: Path, block_size: int = 4 * 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(block_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def timestamp_series(frame: pd.DataFrame) -> tuple[pd.Series, str]:
    lower = {str(c).strip().lower(): c for c in frame.columns}
    for name in TIMESTAMP_COLUMNS:
        if name in lower:
            return pd.to_datetime(frame[lower[name]], utc=True, errors="coerce", format="mixed"), str(lower[name])
    if "date" in lower and "time" in lower:
        combined = frame[lower["date"]].astype(str).str.strip() + " " + frame[lower["time"]].astype(str).str.strip()
        return pd.to_datetime(combined, utc=True, errors="coerce", format="mixed"), f"{lower['date']}+{lower['time']}"
    raise ValueError("no supported timestamp/datetime or date+time columns")


def inspect_csv(path: Path, max_rows: int) -> dict[str, Any]:
    header = pd.read_csv(path, nrows=0, low_memory=False)
    columns = [str(c) for c in header.columns]
    ohlc = normalize_ohlc(columns)
    if len(ohlc) != 4:
        raise ValueError(f"{path}: missing OHLC columns; found={sorted(ohlc)}")

    sampled = pd.read_csv(path, nrows=max_rows, low_memory=False)
    ts, ts_col = timestamp_series(sampled)
    if ts.isna().any():
        raise ValueError(f"{path}: invalid timestamp/date-time in sampled rows")
    if ts.duplicated().any():
        raise ValueError(f"{path}: duplicate timestamp in sampled rows")

    lower = {str(c).strip().lower(): c for c in sampled.columns}
    symbol_col = next((lower[name] for name in SYMBOL_COLUMNS if name in lower), None)
    sampled_symbols = []
    if symbol_col is not None:
        sampled_symbols = sorted({str(x).upper().strip() for x in sampled[symbol_col].dropna().unique()})

    for field, col in ohlc.items():
        values = pd.to_numeric(sampled[col], errors="coerce")
        if values.isna().any():
            raise ValueError(f"{path}: non-numeric/NaN {field} in sampled rows")

    sampled_years = sorted({int(y) for y in ts.dt.year.unique()})
    return {
        "path": str(path),
        "sha256": sha256(path),
        "symbol_column": str(symbol_col) if symbol_col is not None else None,
        "sampled_symbols": sampled_symbols,
        "columns": columns,
        "timestamp_column": ts_col,
        "ohlc_columns": ohlc,
        "sampled_rows": int(len(sampled)),
        "sampled_min_timestamp": ts.min().isoformat() if len(ts) else None,
        "sampled_max_timestamp": ts.max().isoformat() if len(ts) else None,
        "sampled_years": sampled_years,
        "has_2025_sample": 2025 in sampled_years,
    }


def discover(root: Path, max_rows: int) -> tuple[dict[str, list[dict[str, Any]]], list[str], list[str]]:
    candidates = [p for p in root.rglob("*.csv") if p.is_file()]
    by_tf: dict[str, list[dict[str, Any]]] = {tf: [] for tf in SIX_TF}
    ignored: list[str] = []
    out_of_scope: list[str] = []

    for path in sorted(candidates):
        symbol_from_path = infer_symbol_from_text(path.name)
        if symbol_from_path is not None and symbol_from_path != CANONICAL_SYMBOL:
            out_of_scope.append(str(path))
            continue

        tf = infer_tf_from_text(path.name)
        if tf is None:
            try:
                header = pd.read_csv(path, nrows=0, low_memory=False)
                tf_cols = [c for c in header.columns if str(c).strip().lower() in TIMEFRAME_COLUMNS]
                if tf_cols:
                    sample = pd.read_csv(path, usecols=[tf_cols[0]], nrows=max_rows, low_memory=False)
                    unique = {str(x).upper().strip() for x in sample[tf_cols[0]].dropna().unique()}
                    matching = unique.intersection(SIX_TF)
                    tf = next(iter(sorted(matching))) if len(matching) == 1 else None
            except Exception:
                tf = None

        if tf not in SIX_TF:
            ignored.append(str(path))
            continue

        try:
            inspected = inspect_csv(path, max_rows)
        except Exception as exc:
            raise SystemExit(f"SOURCE_INVALID {path}: {exc}") from exc

        sampled_symbols = set(inspected.get("sampled_symbols", []))
        if sampled_symbols and sampled_symbols != {CANONICAL_SYMBOL}:
            if CANONICAL_SYMBOL not in sampled_symbols:
                out_of_scope.append(str(path))
                continue
            raise SystemExit(f"SOURCE_SYMBOL_AMBIGUOUS {path}: sampled_symbols={sorted(sampled_symbols)}")
        by_tf[tf].append(inspected)

    return by_tf, ignored, out_of_scope


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--report", type=Path, required=True)
    ap.add_argument("--max-rows", type=int, default=1000)
    ap.add_argument("--symbol", default=CANONICAL_SYMBOL)
    args = ap.parse_args()

    if args.symbol.upper() != CANONICAL_SYMBOL:
        raise SystemExit(f"UNSUPPORTED_CANONICAL_SYMBOL expected={CANONICAL_SYMBOL} got={args.symbol}")
    if not args.root.exists() or not args.root.is_dir():
        raise SystemExit(f"SOURCE_ROOT_NOT_FOUND {args.root}")
    if args.max_rows < 2:
        raise SystemExit("MAX_ROWS_TOO_SMALL")

    by_tf, ignored, out_of_scope = discover(args.root, args.max_rows)
    missing = [tf for tf in SIX_TF if not by_tf[tf]]
    duplicates = {tf: len(items) for tf, items in by_tf.items() if len(items) > 1}

    report: dict[str, Any] = {
        "adapter": "MTF_SIX_TF_SOURCE_ADAPTER_V2",
        "status": "PASS" if not missing and not duplicates else "BLOCKED",
        "canonical_symbol": CANONICAL_SYMBOL,
        "declared_timeframes": list(SIX_TF),
        "source_timeframes": {tf: len(by_tf[tf]) for tf in SIX_TF},
        "missing_timeframes": missing,
        "ambiguous_duplicate_timeframes": duplicates,
        "ignored_csv_count": len(ignored),
        "out_of_scope_symbol_csv_count": len(out_of_scope),
        "timeframes": by_tf,
        "governance": {
            "development_window": "2016-2024",
            "2025_used_for_tuning": False,
            "direction_generated": False,
            "sl_tp_generated": False,
            "atr_generated": False,
            "risk_generated": False,
        },
        "notes": [
            "Canonical scope is GBPUSD; other symbol datasets in the same package are out-of-scope, not timeframe duplicates.",
            "Exactly one canonical GBPUSD source is required for each of M5, M15, M30, H1, H4, D1.",
            "Multiple competing GBPUSD sources for one timeframe remain blocked rather than silently selected.",
            "Native source presence is proven from CSV content headers and sampled rows, not filename presence alone.",
            "Bare time columns are not accepted; date+time requires explicit combined parsing.",
            "No trend/setup/confirmation/direction is inferred from OHLC by this adapter.",
            "A source containing 2025 remains a source artifact; development consumers must explicitly exclude 2025 rows.",
        ],
    }

    for tf in SIX_TF:
        for item in by_tf[tf]:
            if item["has_2025_sample"]:
                report.setdefault("warnings", []).append(f"{tf}: sampled source contains 2025; development consumers must exclude it.")

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
