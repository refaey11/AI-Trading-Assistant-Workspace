from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from MURPHY_EVALUATORS_V1.murphy_0021_0023_evaluator import evaluate_0021

REQUIRED_H1 = {"timestamp", "open", "high", "low", "close"}
REQUIRED_M1 = {"timestamp", "open", "high", "low", "close", "volume"}


def _load_ohlcv(path: str | Path, required: set[str]) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    if df["timestamp"].isna().any():
        raise ValueError("Invalid timestamps")
    if df["timestamp"].duplicated().any():
        raise ValueError("Duplicate timestamps")
    for col in sorted(required - {"timestamp"}):
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(f"Column {col!r} is not numeric")
    bad_ohlc = (df["high"] < df[["open", "close"]].max(axis=1)) | (df["low"] > df[["open", "close"]].min(axis=1))
    if bad_ohlc.any():
        raise ValueError(f"Invalid OHLC rows: {int(bad_ohlc.sum())}")
    return df.sort_values("timestamp").reset_index(drop=True)


def load_h1(path: str | Path) -> pd.DataFrame:
    """Load the full H1 history so 2025 rows can use the last prior completed H1 bar."""
    return _load_ohlcv(path, REQUIRED_H1)


def build_canonical_h1_volume_context(m1_path: str | Path) -> pd.DataFrame:
    """Recreate the existing project H1 volume_direction contract from M1 data.

    Canonical historical VOLUME_CONFIRMATION_V2 outputs use M1_TitanFX bars
    aggregated to H1, then compare current aggregated volume with the previous
    completed H1 volume. No new threshold is introduced.
    """
    m1 = _load_ohlcv(m1_path, REQUIRED_M1)
    m1["h1_timestamp"] = m1["timestamp"].dt.floor("h")
    h1 = (
        m1.groupby("h1_timestamp", as_index=False)
        .agg(volume=("volume", "sum"), m1_count=("volume", "size"))
        .sort_values("h1_timestamp")
        .reset_index(drop=True)
    )
    h1["previous_volume"] = h1["volume"].shift(1)
    h1["volume_direction"] = "FLAT"
    h1.loc[h1["previous_volume"].isna(), "volume_direction"] = None
    h1.loc[h1["volume"] > h1["previous_volume"], "volume_direction"] = "UP"
    h1.loc[h1["volume"] < h1["previous_volume"], "volume_direction"] = "DOWN"
    h1["volume_change_available"] = h1["previous_volume"].notna()
    return h1


def run(path: str | Path, m1_path: str | Path) -> tuple[pd.DataFrame, dict]:
    full_h1 = load_h1(path)
    df = full_h1[full_h1["timestamp"].dt.year.eq(2025)].copy().reset_index(drop=True)
    if df.empty:
        raise ValueError("No 2025 rows found")

    # Price context is source-faithful: carry the immediately preceding
    # completed H1 close into the first 2025 row when it exists. This avoids
    # treating the 2025 boundary itself as missing evidence when the source
    # contains the prior completed H1 bar.
    full_h1["previous_close"] = full_h1["close"].shift(1)
    df = full_h1[full_h1["timestamp"].dt.year.eq(2025)].copy().reset_index(drop=True)

    volume_context = build_canonical_h1_volume_context(m1_path)
    volume_2025 = volume_context[volume_context["h1_timestamp"].dt.year.eq(2025)].copy()
    if volume_2025.empty:
        raise ValueError("No 2025 H1 volume context found")

    merged = df.merge(
        volume_2025[["h1_timestamp", "volume_direction", "volume_change_available", "m1_count"]],
        left_on="timestamp",
        right_on="h1_timestamp",
        how="left",
        validate="one_to_one",
    )
    missing_volume_context_rows = int(merged["volume_direction"].isna().sum())

    rows = []
    for row in merged.itertuples(index=False):
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
        "missing_canonical_volume_context_rows": missing_volume_context_rows,
        "lookahead_policy": "previous completed bar only",
        "price_context_policy": "carry immediately preceding completed H1 close from the source history into the first 2025 row when available",
        "volume_semantics": "canonical project VOLUME_CONFIRMATION_V2: M1_TitanFX volume aggregated to H1, then current H1 volume versus previous completed H1 volume",
        "volume_source": "GBPUSD M1 master, source-faithful aggregation; no new threshold",
        "m1_rows_total": int(len(pd.read_csv(m1_path))),
        "tuning": False,
        "notes": [
            "Fresh 2025 production of MURPHY_0021 only.",
            "MURPHY_0022 and MURPHY_0023 are not produced here because approved futures OI evidence is unavailable on the spot-FX source path.",
            "This run is not a profitability test and does not generate a standalone trade decision.",
            "Previous fresh run was rejected as a context-wiring mismatch because it used raw H1 volume instead of the existing M1-derived H1 volume_direction contract.",
            "Rows without canonical M1-derived H1 volume evidence remain NOT_EVALUABLE; missing context is never substituted with raw H1 volume or a fabricated proxy."
        ],
    }
    return out, manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--m1-input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--manifest", required=True)
    args = parser.parse_args()

    out, manifest = run(args.input, args.m1_input)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.manifest).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output, index=False)
    Path(args.manifest).write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
