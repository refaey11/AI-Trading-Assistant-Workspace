from __future__ import annotations

"""Cheap real-source smoke test; no CircleCI trigger and no full backtest."""
import argparse
import importlib.util
from pathlib import Path
import pandas as pd


def load(path: Path, required: set[str]) -> pd.DataFrame:
    df = pd.read_csv(path, nrows=5000, low_memory=False)
    miss = sorted(required - set(df.columns))
    if miss:
        raise ValueError(f"{path}: missing {miss}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce", format="mixed")
    if df["timestamp"].isna().any():
        raise ValueError(f"{path}: invalid timestamp")
    return df.sort_values("timestamp").reset_index(drop=True)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--h1", type=Path, required=True)
    p.add_argument("--market", type=Path, required=True)
    p.add_argument("--mtf", type=Path, required=True)
    p.add_argument("--murphy", type=Path, required=True)
    p.add_argument("--nison", type=Path, required=True)
    p.add_argument("--hc", type=Path, required=True)
    p.add_argument("--ho", type=Path, required=True)
    args = p.parse_args()

    h1 = load(args.h1, {"timestamp", "open", "high", "low", "close"})
    market = load(args.market, {"timestamp"})
    mtf = load(args.mtf, {"timestamp"})
    murphy = load(args.murphy, {"timestamp", "status", "direction", "source_rule_id"})
    nison = load(args.nison, {"timestamp", "status", "direction", "rule_id"})
    hc = load(args.hc, {"timestamp", "context_signature"})
    ho = load(args.ho, {"timestamp", "context_signature"})

    assert h1.timestamp.max().year <= 2024, "H1 smoke sample contains 2025+"
    for label, df in {"market": market, "mtf": mtf, "murphy": murphy, "nison": nison, "hc": hc, "ho": ho}.items():
        if not df.empty and df.timestamp.min() > h1.timestamp.max():
            raise AssertionError(f"{label} has no usable as-of history for H1 sample")

    print("REAL_SOURCE_E2E_SMOKE=PASS")
    print(f"H1_ROWS={len(h1)} MARKET_ROWS={len(market)} MTF_ROWS={len(mtf)} MURPHY_ROWS={len(murphy)} NISON_ROWS={len(nison)} HC_ROWS={len(hc)} HO_ROWS={len(ho)}")
    print(f"H1_WINDOW={h1.timestamp.min().isoformat()}..{h1.timestamp.max().isoformat()}")


if __name__ == "__main__":
    main()
