from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

REQUIRED = {"timestamp", "close", "atr20"}


def build(source: Path, output_dir: Path, year: int) -> dict:
    df = pd.read_csv(source)
    missing = sorted(REQUIRED - set(df.columns))
    if missing:
        raise ValueError(f"source missing required columns: {missing}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if df["timestamp"].isna().any():
        raise ValueError("invalid timestamps in authoritative market-state source")
    df = df[df["timestamp"].dt.year == year].copy()
    df = df.sort_values("timestamp").drop_duplicates("timestamp", keep="last")
    df = df[df["close"].notna() & df["atr20"].notna() & (df["atr20"] > 0)]
    if df.empty:
        raise ValueError(f"no usable rows for year {year}")

    out = output_dir
    out.mkdir(parents=True, exist_ok=True)

    # Context: source-backed market state only. No direction is created here.
    context_cols = [c for c in df.columns if c not in {"open", "high", "low"}]
    context = df[context_cols].copy()
    context["entry_price"] = context["close"]
    context["atr"] = context["atr20"]
    context.to_csv(out / "context.csv", index=False)

    # Execution inputs: event-close entry and source ATR20, matching the frozen
    # evaluation convention. This file does not create BUY/SELL direction.
    execution = df[["timestamp", "close", "atr20"]].copy()
    execution = execution.rename(columns={"close": "entry_price", "atr20": "atr"})
    execution.to_csv(out / "execution.csv", index=False)

    manifest = {
        "status": "PASS",
        "mode": "SOURCE_BACKED_CONTEXT_EXECUTION_INPUTS",
        "evaluation_year": year,
        "rows": int(len(df)),
        "entry_policy": "event_close",
        "atr_source": "atr20",
        "direction_created": False,
        "risk_created": False,
        "tiz_created": False,
        "source_backed_only": True,
        "tuning": False,
    }
    (out / "CONTEXT_EXECUTION_INPUT_MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--source", required=True, type=Path)
    p.add_argument("--output-dir", required=True, type=Path)
    p.add_argument("--year", required=True, type=int)
    args = p.parse_args()
    print(json.dumps(build(args.source, args.output_dir, args.year), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
