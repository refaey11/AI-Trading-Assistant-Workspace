from __future__ import annotations

"""Independent V1.2 setup-mode research comparator.

Research-only. Keeps V1.1 intact and tests three more selective setup modes:
trend pullback, breakout-retest, and range reversal. Same 15m execution,
confirmed 15m/30m/1h/4h/D MTF, next-bar entry, ATR risk, fixed round-trip cost,
and conservative ambiguous-bar handling as V1.1.
"""

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

from INDEPENDENT_FOUR_SYSTEM_COMPARATOR_V1 import (
    COST_PIPS_ROUND_TRIP,
    PIP,
    add_features,
    align_mtf,
    load_csv,
    load_m1_source,
    metrics,
    ohlcv_15m,
)


def add_v12_features(df: pd.DataFrame, m1: pd.DataFrame) -> pd.DataFrame:
    x = add_features(df)
    mtf = align_mtf(x, m1).set_index("timestamp")
    x = x.set_index("timestamp").join(mtf[["bull_mtf", "bear_mtf"]], how="left").reset_index()
    x[["bull_mtf", "bear_mtf"]] = x[["bull_mtf", "bear_mtf"]].fillna(False)

    x["bull_mtf4"] = (x[["t15", "t30", "t60", "t240", "td"]] == 1).sum(axis=1) >= 4 if all(c in x for c in ["t15", "t30", "t60", "t240", "td"]) else x.bull_mtf
    x["bear_mtf4"] = (x[["t15", "t30", "t60", "t240", "td"]] == -1).sum(axis=1) >= 4 if all(c in x for c in ["t15", "t30", "t60", "t240", "td"]) else x.bear_mtf

    # Recompute the confirmed MTF directions as columns for the stricter 4/5 gate.
    b = x[["timestamp"]].copy().set_index("timestamp")
    for rule, name in [("15min", "t15"), ("30min", "t30"), ("60min", "t60"), ("240min", "t240"), ("1D", "td")]:
        q = m1.set_index("timestamp").sort_index().resample(rule, label="left", closed="left").agg({"open":"first","high":"max","low":"min","close":"last"}).dropna()
        e = q.close.ewm(span=50, adjust=False, min_periods=50).mean()
        s = pd.Series(np.where(q.close > e, 1, np.where(q.close < e, -1, 0)), index=q.index).shift(1)
        b[name] = s.reindex(b.index, method="ffill")
    for c in ["t15", "t30", "t60", "t240", "td"]:
        x[c] = b[c].values
    x["bull_mtf4"] = (x[["t15", "t30", "t60", "t240", "td"]] == 1).sum(axis=1) >= 4
    x["bear_mtf4"] = (x[["t15", "t30", "t60", "t240", "td"]] == -1).sum(axis=1) >= 4

    x["ema21_dist_atr"] = (x.close - x.ema21) / x.atr
    x["bull_pullback"] = (
        x.murphy_bull & x.bull_mtf4 & (x.low <= x.ema21 + 0.35 * x.atr) &
        (x.close > x.ema21) & x.bull_nison & x.momentum_bull
    )
    x["bear_pullback"] = (
        x.murphy_bear & x.bear_mtf4 & (x.high >= x.ema21 - 0.35 * x.atr) &
        (x.close < x.ema21) & x.bear_nison & x.momentum_bear
    )

    # Breakout-retest: confirmed breakout in the recent 3 bars, followed by a
    # close back on the breakout side with a candle confirmation.
    x["recent_bull_break"] = x.bull_break.rolling(3, min_periods=1).max().astype(bool)
    x["recent_bear_break"] = x.bear_break.rolling(3, min_periods=1).max().astype(bool)
    x["bull_break_retest"] = (
        x.murphy_bull & x.bull_mtf4 & x.recent_bull_break &
        (x.close > x.recent_resistance - 0.25 * x.atr) & x.bull_nison & x.momentum_bull
    )
    x["bear_break_retest"] = (
        x.murphy_bear & x.bear_mtf4 & x.recent_bear_break &
        (x.close < x.recent_support + 0.25 * x.atr) & x.bear_nison & x.momentum_bear
    )

    # Range reversal: only when trend strength is weak; location + candle +
    # momentum reversal. No trend-direction gate is used here.
    x["range_regime"] = (x.adx < 20) & (x.atr_pct >= 0.05)
    x["bull_reversal"] = x.range_regime & x.near_support & x.bull_nison & (x.rsi > x.rsi.shift(1)) & (x.rsi <= 50)
    x["bear_reversal"] = x.range_regime & x.near_resistance & x.bear_nison & (x.rsi < x.rsi.shift(1)) & (x.rsi >= 50)
    return x


def simulate(df: pd.DataFrame, buy: pd.Series, sell: pd.Series, cost_pips: float) -> list[dict]:
    trades = []
    i = 0
    cost = cost_pips * PIP
    while i < len(df) - 1:
        side = 1 if bool(buy.iloc[i]) else -1 if bool(sell.iloc[i]) else 0
        if side == 0:
            i += 1
            continue
        atr_v = float(df.atr.iloc[i]) if pd.notna(df.atr.iloc[i]) else math.nan
        entry = float(df.open.iloc[i + 1])
        if not np.isfinite(atr_v) or not np.isfinite(entry) or atr_v <= 0:
            i += 1
            continue
        risk = atr_v * 1.2
        sl = entry - side * risk
        tp = entry + side * (2.0 * risk)
        exit_i = None
        outcome = "OPEN_END"
        gross_r = 0.0
        for j in range(i + 1, len(df)):
            hi, lo = float(df.high.iloc[j]), float(df.low.iloc[j])
            hit_sl = lo <= sl if side == 1 else hi >= sl
            hit_tp = hi >= tp if side == 1 else lo <= tp
            if hit_sl and hit_tp:
                exit_i = j; outcome = "AMBIGUOUS_LOSS"; gross_r = -1.0; break
            if hit_sl:
                exit_i = j; outcome = "LOSS"; gross_r = -1.0; break
            if hit_tp:
                exit_i = j; outcome = "WIN"; gross_r = 2.0; break
        if exit_i is None:
            exit_i = len(df) - 1
            px = float(df.close.iloc[exit_i])
            gross_r = side * (px - entry) / risk
        net_r = gross_r - cost / risk
        trades.append({
            "entry_time": df.timestamp.iloc[i + 1].isoformat(),
            "signal_time": df.timestamp.iloc[i].isoformat(),
            "side": "BUY" if side == 1 else "SELL",
            "entry": entry, "sl": sl, "tp": tp,
            "gross_R": gross_r, "cost_R": cost / risk, "net_R": net_r,
            "outcome": outcome, "bars_held": int(exit_i - (i + 1)),
        })
        i = exit_i + 1
    return trades


def run(h1_path: Path, m1_path: Path, out: Path, cost_pips: float) -> dict:
    h1 = load_csv(h1_path)
    m1 = load_m1_source(m1_path)
    bars = ohlcv_15m(m1)
    bars = bars[bars.timestamp.dt.year.between(2016, 2025)].reset_index(drop=True)
    x = add_v12_features(bars, m1)
    systems = {
        "V1.2 Trend Pullback": (x.bull_pullback, x.bear_pullback),
        "V1.2 Breakout Retest": (x.bull_break_retest, x.bear_break_retest),
        "V1.2 Range Reversal": (x.bull_reversal, x.bear_reversal),
    }
    summary = {}
    all_trades = []
    dev_bars = int((x.timestamp.dt.year <= 2024).sum())
    oos_bars = int((x.timestamp.dt.year == 2025).sum())
    for name, (buy, sell) in systems.items():
        t = simulate(x, buy, sell, cost_pips)
        all_trades.extend([{**z, "system": name} for z in t])
        summary[name] = {
            "development_2016_2024": metrics([z for z in t if pd.Timestamp(z["entry_time"]).year <= 2024], dev_bars),
            "oos_2025": metrics([z for z in t if pd.Timestamp(z["entry_time"]).year == 2025], oos_bars),
        }
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(all_trades).to_csv(out / "v12_setup_mode_trades.csv", index=False)
    result = {
        "status": "V1_2_COMPARATOR_EXECUTABLE",
        "execution_timeframe": "15m",
        "mtf": ["15m", "30m", "1h", "4h", "D"],
        "mtf_gate": "4_of_5",
        "lookahead_off": True,
        "oos_tuning": False,
        "cost_pips_round_trip": cost_pips,
        "ambiguous_policy": "LOSS",
        "entry_policy": "signal_on_close_next_bar_open",
        "risk_model": "ATR14 * 1.2 stop, 2.0R target",
        "source_validation": {"h1_rows": int(len(h1)), "m1_rows": int(len(m1)), "execution_bars": int(len(x)), "development_bars": dev_bars, "oos_2025_bars": oos_bars},
        "systems": list(systems),
        "summary": summary,
        "note": "Independent research comparator; V1.2 is an experiment, not an official Decision Brain result or profitability promise.",
    }
    (out / "v12_setup_mode_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--h1", required=True, type=Path)
    p.add_argument("--m1", required=True, type=Path)
    p.add_argument("--output-dir", required=True, type=Path)
    p.add_argument("--cost-pips", type=float, default=COST_PIPS_ROUND_TRIP)
    a = p.parse_args()
    print(json.dumps(run(a.h1, a.m1, a.output_dir, a.cost_pips), indent=2))
