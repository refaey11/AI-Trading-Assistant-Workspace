from __future__ import annotations

"""Independent Murphy/Nison four-system comparator.

Research-only. It does not modify the governed Decision Brain.
Execution timeframe is 15m so the configured 15m/30m/1h/4h/D MTF stack is
represented with higher-timeframe, lookahead-safe resampling from governed M1.
The Pine prototype has a chart timeframe plus five requested timeframes; this
comparator therefore treats 15m as the base execution timeframe and uses the
same five requested contexts where available.
"""

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd


COST_PIPS_ROUND_TRIP = 0.8
PIP = 0.0001


def load_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "timestamp" not in df.columns:
        raise ValueError(f"{path}: missing timestamp")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce", format="mixed")
    if df.timestamp.isna().any():
        raise ValueError(f"{path}: invalid timestamps")
    return df.sort_values("timestamp").drop_duplicates("timestamp").reset_index(drop=True)


def load_m1_source(path: Path) -> pd.DataFrame:
    if path.is_dir():
        files = sorted(path.rglob("*.csv"))
        if not files:
            raise ValueError(f"{path}: no CSV files")
        frames = [load_csv(p) for p in files]
        return pd.concat(frames, ignore_index=True).sort_values("timestamp").drop_duplicates("timestamp").reset_index(drop=True)
    return load_csv(path)


def ohlcv_15m(m1: pd.DataFrame) -> pd.DataFrame:
    required = ["open", "high", "low", "close"]
    for c in required:
        if c not in m1.columns:
            raise ValueError(f"M1 source missing {c}")
    x = m1.set_index("timestamp").sort_index()
    agg = {"open": "first", "high": "max", "low": "min", "close": "last"}
    if "volume" in x.columns:
        agg["volume"] = "sum"
    out = x.resample("15min", label="left", closed="left").agg(agg).dropna(subset=required).reset_index()
    return out


def resample_ohlcv(df: pd.DataFrame, rule: str) -> pd.DataFrame:
    x = df.set_index("timestamp").sort_index()
    agg = {"open": "first", "high": "max", "low": "min", "close": "last"}
    if "volume" in x.columns:
        agg["volume"] = "sum"
    return x.resample(rule, label="left", closed="left").agg(agg).dropna(subset=["open", "high", "low", "close"])


def ema(s: pd.Series, n: int) -> pd.Series:
    return s.ewm(span=n, adjust=False, min_periods=n).mean()


def rsi(s: pd.Series, n: int = 14) -> pd.Series:
    d = s.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    rs = up / dn.replace(0, np.nan)
    return 100 - 100 / (1 + rs)


def atr(df: pd.DataFrame, n: int = 14) -> pd.Series:
    prev = df.close.shift(1)
    tr = pd.concat([df.high - df.low, (df.high - prev).abs(), (df.low - prev).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False, min_periods=n).mean()


def adx(df: pd.DataFrame, n: int = 14):
    up = df.high.diff()
    dn = -df.low.diff()
    plus_dm = pd.Series(np.where((up > dn) & (up > 0), up, 0.0), index=df.index)
    minus_dm = pd.Series(np.where((dn > up) & (dn > 0), dn, 0.0), index=df.index)
    a = atr(df, n)
    plus_di = 100 * plus_dm.ewm(alpha=1 / n, adjust=False, min_periods=n).mean() / a
    minus_di = 100 * minus_dm.ewm(alpha=1 / n, adjust=False, min_periods=n).mean() / a
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan)
    return plus_di, minus_di, dx.ewm(alpha=1 / n, adjust=False, min_periods=n).mean()


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    x = df.copy().sort_values("timestamp").reset_index(drop=True)
    x["ema21"] = ema(x.close, 21)
    x["ema50"] = ema(x.close, 50)
    x["atr"] = atr(x, 14)
    x["atr_pct"] = x.atr / x.close * 100
    x["di_plus"], x["di_minus"], x["adx"] = adx(x, 14)
    x["rsi"] = rsi(x.close, 14)
    x["vol_ma"] = x.volume.rolling(20, min_periods=20).mean() if "volume" in x else np.nan
    x["recent_resistance"] = x.high.shift(1).rolling(20, min_periods=20).max()
    x["recent_support"] = x.low.shift(1).rolling(20, min_periods=20).min()
    x["near_support"] = (x.close - x.recent_support).abs() <= x.atr * 1.25
    x["near_resistance"] = (x.close - x.recent_resistance).abs() <= x.atr * 1.25
    x["bull_break"] = x.close > x.recent_resistance
    x["bear_break"] = x.close < x.recent_support
    x["location_bull"] = x.near_support | x.bull_break
    x["location_bear"] = x.near_resistance | x.bear_break
    body = (x.close - x.open).abs()
    rng = (x.high - x.low).clip(lower=1e-12)
    upper = x.high - x[["open", "close"]].max(axis=1)
    lower = x[["open", "close"]].min(axis=1) - x.low
    x["bull_engulf"] = (x.close > x.open) & (x.close.shift(1) < x.open.shift(1)) & (x.close >= x.open.shift(1)) & (x.open <= x.close.shift(1))
    x["bear_engulf"] = (x.close < x.open) & (x.close.shift(1) > x.open.shift(1)) & (x.open >= x.close.shift(1)) & (x.close <= x.open.shift(1))
    x["bull_pin"] = (x.close > x.open) & (lower >= body * 1.5) & (lower >= upper * 1.2) & (x.close >= x.low + rng * 0.55)
    x["bear_pin"] = (x.close < x.open) & (upper >= body * 1.5) & (upper >= lower * 1.2) & (x.close <= x.high - rng * 0.55)
    inside = (x.high.shift(1) < x.high.shift(2)) & (x.low.shift(1) > x.low.shift(2))
    x["inside_bull"] = inside & (x.close > x.high.shift(1))
    x["inside_bear"] = inside & (x.close < x.low.shift(1))
    x["bull_confirm"] = x.bull_engulf | x.bull_pin | x.inside_bull
    x["bear_confirm"] = x.bear_engulf | x.bear_pin | x.inside_bear
    x["bull_bars"] = bars_since(x.bull_confirm)
    x["bear_bars"] = bars_since(x.bear_confirm)
    x["bull_nison"] = x.bull_bars <= 3
    x["bear_nison"] = x.bear_bars <= 3
    x["trend_regime"] = (x.adx >= 18) & (x.atr_pct >= 0.05)
    x["murphy_bull"], x["murphy_bear"] = murphy_direction(x)
    x["volume_known"] = x.get("volume", pd.Series(index=x.index, dtype=float)).notna() & x.vol_ma.notna()
    x["volume_bull"] = x.volume_known & (x.close > x.open) & (x.volume >= x.vol_ma)
    x["volume_bear"] = x.volume_known & (x.close < x.open) & (x.volume >= x.vol_ma)
    x["momentum_bull"] = (x.rsi >= 52) & (x.rsi > x.rsi.shift(1))
    x["momentum_bear"] = (x.rsi <= 48) & (x.rsi < x.rsi.shift(1))
    return x


def bars_since(s: pd.Series) -> pd.Series:
    out = []
    last = None
    for i, v in enumerate(s.fillna(False).astype(bool)):
        if v:
            last = i
            out.append(0)
        elif last is None:
            out.append(np.nan)
        else:
            out.append(i - last)
    return pd.Series(out, index=s.index)


def murphy_direction(x: pd.DataFrame):
    # Pine proxy: five independent directional votes, 3+ and strictly greater than opposite side.
    prev_high = x.high.shift(1)
    prev_low = x.low.shift(1)
    last_high = x.high.rolling(7, center=False, min_periods=7).max().shift(3)
    last_low = x.low.rolling(7, center=False, min_periods=7).min().shift(3)
    hhhl = last_high.notna() & last_low.notna() & (x.close > last_low) & (x.high >= prev_high) & (x.low >= prev_low)
    lhlh = last_high.notna() & last_low.notna() & (x.close < last_high) & (x.high <= prev_high) & (x.low <= prev_low)
    bull = (x.ema21 > x.ema50).astype(int) + (x.ema21 > x.ema21.shift(1)).astype(int) + (x.close > x.ema50).astype(int) + hhhl.astype(int) + (x.di_plus > x.di_minus).astype(int)
    bear = (x.ema21 < x.ema50).astype(int) + (x.ema21 < x.ema21.shift(1)).astype(int) + (x.close < x.ema50).astype(int) + lhlh.astype(int) + (x.di_minus > x.di_plus).astype(int)
    return (bull >= 3) & (bull > bear), (bear >= 3) & (bear > bull)


def align_mtf(base: pd.DataFrame, m1: pd.DataFrame) -> pd.DataFrame:
    """Return confirmed 15m/30m/1h/4h/D EMA50 directions aligned to 15m bars."""
    b = base[["timestamp"]].copy().set_index("timestamp")
    out = pd.DataFrame(index=b.index)
    for rule, name in [("15min", "t15"), ("30min", "t30"), ("60min", "t60"), ("240min", "t240"), ("1D", "td")]:
        q = resample_ohlcv(m1, rule)
        q["ema50"] = ema(q.close, 50)
        direction = np.where(q.close > q.ema50, 1, np.where(q.close < q.ema50, -1, 0))
        s = pd.Series(direction, index=q.index, name=name)
        # Only completed source bars are usable: shift one source bar before asof alignment.
        s = s.shift(1)
        out[name] = s.reindex(out.index, method="ffill")
    out["bull_mtf"] = (out[["t15", "t30", "t60", "t240", "td"]] == 1).sum(axis=1) >= 3
    out["bear_mtf"] = (out[["t15", "t30", "t60", "t240", "td"]] == -1).sum(axis=1) >= 3
    return out.reset_index()


def attach_signals(base: pd.DataFrame, m1: pd.DataFrame) -> pd.DataFrame:
    x = add_features(base)
    mtf = align_mtf(x, m1).set_index("timestamp")
    x = x.set_index("timestamp")
    x = x.join(mtf[["bull_mtf", "bear_mtf"]], how="left").reset_index()
    x[["bull_mtf", "bear_mtf"]] = x[["bull_mtf", "bear_mtf"]].fillna(False)
    x["bull_score"] = (x.murphy_bull.astype(int) * 3 + x.location_bull.astype(int) + x.bull_nison.astype(int) * 2 + x.volume_bull.astype(int) + x.momentum_bull.astype(int) + x.bull_mtf.astype(int) * 2)
    x["bear_score"] = (x.murphy_bear.astype(int) * 3 + x.location_bear.astype(int) + x.bear_nison.astype(int) * 2 + x.volume_bear.astype(int) + x.momentum_bear.astype(int) + x.bear_mtf.astype(int) * 2)
    x["buy_layered"] = x.trend_regime & x.murphy_bull & x.bull_nison & x.bull_mtf & (x.bull_score >= 7) & (~x.murphy_bear)
    x["sell_layered"] = x.trend_regime & x.murphy_bear & x.bear_nison & x.bear_mtf & (x.bear_score >= 7) & (~x.murphy_bull)
    x["buy_murphy"] = x.trend_regime & x.murphy_bull & (~x.murphy_bear)
    x["sell_murphy"] = x.trend_regime & x.murphy_bear & (~x.murphy_bull)
    x["buy_combo"] = x.buy_murphy & x.bull_nison & x.location_bull
    x["sell_combo"] = x.sell_murphy & x.bear_nison & x.location_bear
    # Baseline: simple trend-following EMA cross with ATR regime gate.
    x["ema_cross_up"] = (x.ema21 > x.ema50) & (x.ema21.shift(1) <= x.ema50.shift(1))
    x["ema_cross_dn"] = (x.ema21 < x.ema50) & (x.ema21.shift(1) >= x.ema50.shift(1))
    x["buy_baseline"] = x.ema_cross_up & x.trend_regime
    x["sell_baseline"] = x.ema_cross_dn & x.trend_regime
    return x


def run_system(df: pd.DataFrame, system: str, cost_pips: float = COST_PIPS_ROUND_TRIP) -> list[dict]:
    if system == "Baseline":
        buy, sell = df.buy_baseline, df.sell_baseline
    elif system == "Murphy only":
        buy, sell = df.buy_murphy, df.sell_murphy
    elif system == "Murphy + Nison":
        buy, sell = df.buy_combo, df.sell_combo
    elif system == "Layered V1.1":
        buy, sell = df.buy_layered, df.sell_layered
    else:
        raise ValueError(system)

    trades = []
    in_pos = False
    i = 0
    cost = cost_pips * PIP
    while i < len(df) - 1:
        if in_pos:
            i += 1
            continue
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
        sl = entry - risk if side == 1 else entry + risk
        tp = entry + risk * 2.0 if side == 1 else entry - risk * 2.0
        exit_i = None
        outcome = None
        for j in range(i + 1, len(df)):
            hi, lo = float(df.high.iloc[j]), float(df.low.iloc[j])
            hit_sl = lo <= sl if side == 1 else hi >= sl
            hit_tp = hi >= tp if side == 1 else lo <= tp
            if hit_sl and hit_tp:
                outcome = "AMBIGUOUS_LOSS"
                exit_i = j
                exit_px = sl
                break
            if hit_sl:
                outcome = "LOSS"
                exit_i = j
                exit_px = sl
                break
            if hit_tp:
                outcome = "WIN"
                exit_i = j
                exit_px = tp
                break
        if exit_i is None:
            exit_i = len(df) - 1
            exit_px = float(df.close.iloc[exit_i])
            outcome = "OPEN_AT_END"
        gross_r = (exit_px - entry) / risk if side == 1 else (entry - exit_px) / risk
        cost_r = cost / risk
        net_r = gross_r - cost_r
        trades.append({
            "system": system,
            "entry_time": str(df.timestamp.iloc[i + 1]),
            "signal_time": str(df.timestamp.iloc[i]),
            "exit_time": str(df.timestamp.iloc[exit_i]),
            "side": "BUY" if side == 1 else "SELL",
            "entry": entry,
            "exit": exit_px,
            "sl": sl,
            "tp": tp,
            "gross_R": gross_r,
            "cost_R": cost_r,
            "net_R": net_r,
            "outcome": outcome,
            "bars_held": int(exit_i - (i + 1)),
        })
        i = exit_i + 1
    return trades


def metrics(trades: list[dict], bars: int) -> dict:
    if not trades:
        return {"trades": 0, "win_rate": 0.0, "profit_factor": 0.0, "expectancy_R": 0.0, "net_R": 0.0, "max_drawdown_R": 0.0, "avg_win_R": 0.0, "avg_loss_R": 0.0, "no_trade_pct": 100.0}
    r = np.array([t["net_R"] for t in trades], dtype=float)
    wins = r[r > 0]
    losses = r[r < 0]
    eq = np.cumsum(r)
    dd = np.maximum.accumulate(eq) - eq
    return {
        "trades": int(len(r)),
        "win_rate": round(float((r > 0).mean() * 100), 3),
        "profit_factor": round(float(wins.sum() / abs(losses.sum())) if losses.size else float("inf"), 4),
        "expectancy_R": round(float(r.mean()), 5),
        "net_R": round(float(r.sum()), 5),
        "max_drawdown_R": round(float(dd.max()), 5),
        "avg_win_R": round(float(wins.mean()) if wins.size else 0.0, 5),
        "avg_loss_R": round(float(losses.mean()) if losses.size else 0.0, 5),
        "no_trade_pct": round(float(max(0, 100 * (bars - len(r)) / bars)), 3),
    }


def run(h1_path: Path, m1_path: Path, out: Path, cost_pips: float) -> dict:
    h1 = load_csv(h1_path)
    m1 = load_m1_source(m1_path)
    for c in ["open", "high", "low", "close"]:
        if c not in h1.columns or c not in m1.columns:
            raise ValueError(f"missing required OHLC column: {c}")
    bars = ohlcv_15m(m1)
    # Keep execution data inside the governed study period.  2025 is OOS only.
    bars = bars[bars.timestamp.dt.year.between(2016, 2025)].reset_index(drop=True)
    x = attach_signals(bars, m1)
    systems = ["Baseline", "Murphy only", "Murphy + Nison", "Layered V1.1"]
    all_trades = []
    summary = {}
    for system in systems:
        t = run_system(x, system, cost_pips)
        all_trades.extend(t)
        summary[system] = {
            "development_2016_2024": metrics([z for z in t if pd.Timestamp(z["entry_time"]).year <= 2024], int((x.timestamp.dt.year <= 2024).sum())),
            "oos_2025": metrics([z for z in t if pd.Timestamp(z["entry_time"]).year == 2025], int((x.timestamp.dt.year == 2025).sum())),
        }
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(all_trades).to_csv(out / "four_system_trades.csv", index=False)
    result = {
        "status": "COMPARATOR_EXECUTABLE",
        "execution_timeframe": "15m",
        "mtf": ["15m", "30m", "1h", "4h", "D"],
        "lookahead_off": True,
        "oos_tuning": False,
        "cost_pips_round_trip": cost_pips,
        "ambiguous_policy": "LOSS",
        "entry_policy": "signal_on_close_next_bar_open",
        "risk_model": "ATR14 * 1.2 stop, 2.0R target",
        "source_validation": {
            "h1_rows": int(len(h1)),
            "m1_rows": int(len(m1)),
            "execution_bars": int(len(x)),
            "development_bars": int((x.timestamp.dt.year <= 2024).sum()),
            "oos_2025_bars": int((x.timestamp.dt.year == 2025).sum()),
        },
        "systems": systems,
        "summary": summary,
        "note": "Independent research comparator; not an official Decision Brain result and not a promise of profitability.",
    }
    (out / "four_system_comparator_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--h1", required=True, type=Path)
    p.add_argument("--m1", required=True, type=Path)
    p.add_argument("--output-dir", required=True, type=Path)
    p.add_argument("--cost-pips", type=float, default=COST_PIPS_ROUND_TRIP)
    a = p.parse_args()
    print(json.dumps(run(a.h1, a.m1, a.output_dir, a.cost_pips), indent=2))
