from __future__ import annotations

"""Independent indicator comparator scaffold.

This intentionally starts with source-backed H1 bars and a conservative,
lookahead-safe signal/exit engine. It does not alter the governed Decision Brain.
"""
import argparse, json
from pathlib import Path
import pandas as pd


def load(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "timestamp" not in df.columns:
        raise ValueError(f"{path}: missing timestamp")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce", format="mixed")
    if df.timestamp.isna().any():
        raise ValueError(f"{path}: invalid timestamps")
    return df.sort_values("timestamp").drop_duplicates("timestamp").reset_index(drop=True)


def run(h1: Path, out: Path) -> dict:
    bars = load(h1)
    for c in ["open", "high", "low", "close"]:
        if c not in bars.columns:
            raise ValueError(f"H1 source missing {c}")
    # Source validation only in this first comparator commit. Signal parity with
    # Pine V1.1 is implemented in the next commit after this executable baseline.
    dev = bars[bars.timestamp.dt.year.between(2016, 2024)].copy()
    oos = bars[bars.timestamp.dt.year.eq(2025)].copy()
    result = {
        "status": "SOURCE_VALIDATED_PENDING_SIGNAL_PARITY",
        "development_bars": int(len(dev)),
        "oos_2025_bars": int(len(oos)),
        "lookahead_off": True,
        "oos_tuning": False,
        "systems": ["Baseline", "Murphy only", "Murphy + Nison", "Layered V1.1"],
        "metrics": ["trades", "win_rate", "profit_factor", "expectancy_R", "net_R", "max_drawdown_R", "no_trade_pct"],
    }
    out.mkdir(parents=True, exist_ok=True)
    (out / "four_system_comparator_status.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--h1", required=True, type=Path)
    p.add_argument("--output-dir", required=True, type=Path)
    a = p.parse_args()
    print(json.dumps(run(a.h1, a.output_dir), indent=2))
