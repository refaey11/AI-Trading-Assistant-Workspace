from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Optional

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from OOS_2025.nison_2025_runtime_producer_v1 import run_ohlcv_2025

REQUIRED = {"timestamp", "open", "high", "low", "close"}
EXPECTED_RULES = 44


def load_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    if df["timestamp"].isna().any():
        raise ValueError("Input contains invalid timestamps")
    if df["timestamp"].duplicated().any():
        raise ValueError("Input contains duplicate timestamps")
    for col in ["open", "high", "low", "close"]:
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(f"Column {col!r} is not numeric")
    bad_ohlc = (df["high"] < df[["open", "close"]].max(axis=1)) | (df["low"] > df[["open", "close"]].min(axis=1))
    if bad_ohlc.any():
        raise ValueError(f"Invalid OHLC rows: {int(bad_ohlc.sum())}")
    return df.sort_values("timestamp").reset_index(drop=True)


def build_context(path: Optional[Path]) -> Optional[pd.DataFrame]:
    if path is None:
        return None
    ctx = pd.read_csv(path)
    if "timestamp" not in ctx.columns:
        raise ValueError("Context file must contain timestamp")
    ctx["timestamp"] = pd.to_datetime(ctx["timestamp"], utc=True)
    return ctx


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--context", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    args = parser.parse_args()

    bars_all = load_csv(args.input)
    bars_2025 = bars_all[bars_all["timestamp"].dt.year.eq(2025)].copy()
    if bars_2025.empty:
        raise ValueError("No 2025 rows found in input")

    context = build_context(args.context)
    evidence = run_ohlcv_2025(bars_2025, context)

    expected_rows = len(bars_2025) * EXPECTED_RULES
    if len(evidence) != expected_rows:
        raise AssertionError(f"Evidence row count {len(evidence)} != expected {expected_rows}")
    if evidence["rule_id"].nunique() != EXPECTED_RULES:
        raise AssertionError("Not all 44 Nison rule IDs were emitted")
    if pd.to_datetime(evidence["timestamp"], utc=True).dt.year.ne(2025).any():
        raise AssertionError("Evidence contains non-2025 timestamps")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    evidence.to_csv(args.output, index=False)

    status_counts = evidence["status"].value_counts().to_dict()
    per_rule = evidence.groupby(["rule_id", "status"]).size().unstack(fill_value=0).to_dict(orient="index")
    manifest = {
        "input": str(args.input),
        "context": str(args.context) if args.context else None,
        "scope": "2025-01-01T00:00:00Z..2025-12-31T23:59:59Z",
        "input_rows_total": int(len(bars_all)),
        "input_rows_2025": int(len(bars_2025)),
        "nison_rules": EXPECTED_RULES,
        "evidence_rows": int(len(evidence)),
        "status_counts": {k: int(v) for k, v in status_counts.items()},
        "per_rule_status_counts": {k: {sk: int(sv) for sk, sv in v.items()} for k, v in per_rule.items()},
        "lookahead_policy": "none",
        "oos_policy": "2025 is evaluation-only; no tuning or threshold selection",
    }
    args.manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")

    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
