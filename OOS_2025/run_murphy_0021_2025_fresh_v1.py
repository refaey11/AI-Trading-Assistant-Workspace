from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from MURPHY_EVALUATORS_V1.murphy_0021_0023_evaluator import evaluate_0021

REQUIRED = {"timestamp", "open", "high", "low", "close", "volume"}


def load_2025(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    if df["timestamp"].isna().any():
        raise ValueError("Invalid timestamps")
    if df["timestamp"].duplicated().any():
        raise ValueError("Duplicate timestamps")
    for col in ["open", "high", "low", "close", "volume"]:
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(f"Column {col!r} is not numeric")
    bad_ohlc = (df["high"] < df[["open", "close"]].max(axis=1)) | (df["low"] > df[["open", "close"]].min(axis=1))
    if bad_ohlc.any():
        raise ValueError(f"Invalid OHLC rows: {int(bad_ohlc.sum())}")
    df = df.sort_values("timestamp").reset_index(drop=True)
    df = df[df["timestamp"].dt.year.eq(2025)].copy().reset_index(drop=True)
    if df.empty:
        raise ValueError("No 2025 rows found")
    return df


def volume_direction(series: pd.Series) -> pd.Series:
    prev = series.shift(1)
    out = pd.Series("FLAT", index=series.index, dtype="object")
    out[series > prev] = "UP"
    out[series < prev] = "DOWN"
    out[prev.isna()] = None
    return out


def run(path: str | Path) -> tuple[pd.DataFrame, dict]:
    df = load_2025(path)
    df["previous_close"] = df["close"].shift(1)
    df["volume_direction"] = volume_direction(df["volume"])

    rows = []
    for row in df.itertuples(index=False):
        result = evaluate_0021({
            "close": row.close,
            "previous_close": row.previous_close,
            "volume_direction": row.volume_direction,
        })
        rows.append({
            "timestamp": row.timestamp,
            "rule_id": result["rule_id"],
            "status": result["status"],
            "directional_confirmation": result["directional_confirmation"],
            "reason": result["reason"],
        })
    out = pd.DataFrame(rows)
    counts = out["status"].value_counts().to_dict()
    manifest = {
        "status": "FRESH_MURPHY_2025_OOS_ONLY",
        "rule_id": "MURPHY_0021",
        "input_rows_2025": int(len(df)),
        "output_rows": int(len(out)),
        "pass_rows": int(counts.get("PASS", 0)),
        "fail_rows": int(counts.get("FAIL", 0)),
        "not_evaluable_rows": int(counts.get("NOT_EVALUABLE", 0)),
        "lookahead_policy": "previous completed bar only",
        "volume_semantics": "existing project volume_direction: current volume versus previous completed bar; no new threshold",
        "tuning": False,
        "notes": [
            "Fresh 2025 production of MURPHY_0021 only.",
            "MURPHY_0022 and MURPHY_0023 are not produced here because approved futures OI evidence is unavailable on the spot-FX source path.",
            "This run is not a profitability test and does not generate a standalone trade decision."
        ],
    }
    return out, manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--manifest", required=True)
    args = parser.parse_args()

    out, manifest = run(args.input)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.manifest).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output, index=False)
    Path(args.manifest).write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
