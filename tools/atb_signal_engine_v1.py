from __future__ import annotations

"""ATB V1 — independent, deterministic signal engine prototype.

Uses existing OHLC market data and optional governed Murphy/Nison evidence.
It deliberately does not alter Decision Brain, rule semantics, or 2025 OOS data.

Signal logic:
  1) Higher-timeframe trend: EMA50 vs EMA200 and EMA50 slope.
  2) Execution-timeframe breakout: close above/below prior N-bar range.
  3) Momentum: RSI around the 50 line.
  4) Volatility: ATR percentage percentile/rank gate.
  5) Optional evidence hooks are context/confirmation only; absence is NOT a
     directional opposite signal.

The runner emits BUY/SELL/NO_TRADE plus deterministic reason codes. Parameter
selection must be performed outside the locked OOS period.
"""

import argparse
import json
from pathlib import Path

import pandas as pd


DEFAULT_N = 20
DEFAULT_ATR_PERIOD = 14
DEFAULT_RSI_PERIOD = 14
DEFAULT_EMA_FAST = 50
DEFAULT_EMA_SLOW = 200
DEFAULT_ATR_MIN_PERCENTILE = 30.0
DEFAULT_SL_ATR = 1.0
DEFAULT_TP_R = 2.0


def _find_col(df: pd.DataFrame, names: list[str]) -> str:
    lower = {str(c).strip().lower(): c for c in df.columns}
    for name in names:
        if name.lower() in lower:
            return lower[name.lower()]
    raise ValueError(f"Missing OHLC column; tried {names}; columns={list(df.columns)}")


def load_ohlc(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    mapping = {
        "open": _find_col(df, ["open", "o"]),
        "high": _find_col(df, ["high", "h"]),
        "low": _find_col(df, ["low", "l"]),
        "close": _find_col(df, ["close", "c"]),
    }
    out = df.rename(columns={v: k for k, v in mapping.items()})
    time_candidates = [c for c in df.columns if str(c).lower() in {"time", "datetime", "date", "timestamp"}]
    if time_candidates:
        out["time"] = pd.to_datetime(df[time_candidates[0]], errors="coerce", utc=True)
    else:
        out["time"] = pd.RangeIndex(len(out))
    for c in ["open", "high", "low", "close"]:
        out[c] = pd.to_numeric(out[c], errors="coerce")
    out = out.dropna(subset=["open", "high", "low", "close"]).sort_values("time").reset_index(drop=True)
    return out


def indicators(df: pd.DataFrame) -> pd.DataFrame:
    x = df.copy()
    x["ema50"] = x["close"].ewm(span=DEFAULT_EMA_FAST, adjust=False).mean()
    x["ema200"] = x["close"].ewm(span=DEFAULT_EMA_SLOW, adjust=False).mean()
    prev_close = x["close"].shift(1)
    tr = pd.concat([
        x["high"] - x["low"],
        (x["high"] - prev_close).abs(),
        (x["low"] - prev_close).abs(),
    ], axis=1).max(axis=1)
    x["atr"] = tr.rolling(DEFAULT_ATR_PERIOD).mean()
    delta = x["close"].diff()
    gain = delta.clip(lower=0).rolling(DEFAULT_RSI_PERIOD).mean()
    loss = (-delta.clip(upper=0)).rolling(DEFAULT_RSI_PERIOD).mean()
    rs = gain / loss.replace(0, pd.NA)
    x["rsi"] = 100 - (100 / (1 + rs))
    x["rsi"] = x["rsi"].fillna(50)
    x["atr_pct"] = x["atr"] / x["close"].replace(0, pd.NA)
    # Expanding rank avoids look-ahead: rank at t uses observations through t only.
    x["atr_pctile"] = x["atr_pct"].expanding(min_periods=DEFAULT_ATR_PERIOD * 3).rank(pct=True) * 100
    x["prior_high"] = x["high"].rolling(DEFAULT_N).max().shift(1)
    x["prior_low"] = x["low"].rolling(DEFAULT_N).min().shift(1)
    x["ema50_slope"] = x["ema50"].diff(5)
    return x


def signal_row(r: pd.Series) -> dict:
    long_trend = r.ema50 > r.ema200 and r.ema50_slope > 0 and r.close > r.ema50
    short_trend = r.ema50 < r.ema200 and r.ema50_slope < 0 and r.close < r.ema50
    long_break = r.close > r.prior_high
    short_break = r.close < r.prior_low
    long_mom = r.rsi > 50
    short_mom = r.rsi < 50
    vol_ok = pd.notna(r.atr_pctile) and r.atr_pctile >= DEFAULT_ATR_MIN_PERCENTILE

    if long_trend and long_break and long_mom and vol_ok:
        side = "BUY"
    elif short_trend and short_break and short_mom and vol_ok:
        side = "SELL"
    else:
        side = "NO_TRADE"

    reasons = []
    if not (long_trend or short_trend): reasons.append("NO_CLEAR_TREND")
    if not (long_break or short_break): reasons.append("NO_BREAKOUT")
    if not (long_mom or short_mom): reasons.append("NO_MOMENTUM")
    if not vol_ok: reasons.append("VOLATILITY_FILTER")
    if side == "BUY": reasons = ["TREND_UP", "BREAKOUT_UP", "MOMENTUM_UP", "VOLATILITY_OK"]
    if side == "SELL": reasons = ["TREND_DOWN", "BREAKOUT_DOWN", "MOMENTUM_DOWN", "VOLATILITY_OK"]

    entry = float(r.close)
    atr = float(r.atr) if pd.notna(r.atr) else None
    stop = target = None
    if atr is not None and side == "BUY":
        stop = entry - DEFAULT_SL_ATR * atr
        target = entry + DEFAULT_TP_R * (entry - stop)
    elif atr is not None and side == "SELL":
        stop = entry + DEFAULT_SL_ATR * atr
        target = entry - DEFAULT_TP_R * (stop - entry)

    return {
        "time": str(r.time), "signal": side, "entry_reference_close": entry,
        "stop_reference": stop, "target_reference": target,
        "atr": atr, "rsi": float(r.rsi), "atr_percentile": None if pd.isna(r.atr_pctile) else float(r.atr_pctile),
        "reason_codes": reasons,
        "model_version": "ATB_V1",
    }


def run(input_csv: str, output_jsonl: str) -> None:
    x = indicators(load_ohlc(input_csv))
    warm = max(DEFAULT_EMA_SLOW, DEFAULT_N, DEFAULT_ATR_PERIOD * 3)
    rows = [signal_row(r) for _, r in x.iloc[warm:].iterrows()]
    with open(output_jsonl, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    counts = pd.Series([r["signal"] for r in rows]).value_counts().to_dict()
    print(json.dumps({"model_version": "ATB_V1", "rows": len(rows), "signal_counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("input_csv")
    p.add_argument("output_jsonl")
    a = p.parse_args()
    run(a.input_csv, a.output_jsonl)
