from __future__ import annotations

"""Executable deterministic trading adapter.

Uses the existing ATB V1 signal logic with next-bar-open entry, fixed 1 ATR
SL / 2R TP, and fail-closed intrabar ambiguity. Feature calculations use the
full supplied history for warm-up, while signal generation and trade exits are
strictly bounded to the requested evaluation window.
"""

import argparse
import json
from pathlib import Path
import pandas as pd

N = 20
ATR_PERIOD = 14
RSI_PERIOD = 14
EMA_FAST = 50
EMA_SLOW = 200
ATR_MIN_PERCENTILE = 30.0
SL_ATR = 1.0
TP_R = 2.0


def load_ohlc(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    cols = {str(c).strip().lower(): c for c in df.columns}
    def pick(*names):
        for n in names:
            if n in cols:
                return cols[n]
        raise ValueError(f"missing OHLC column {names}; columns={list(df.columns)}")
    t = pick("timestamp", "datetime", "date", "time")
    out = df.rename(columns={pick("open"): "open", pick("high"): "high", pick("low"): "low", pick("close"): "close", t: "timestamp"})[["timestamp", "open", "high", "low", "close"]].copy()
    out["timestamp"] = pd.to_datetime(out["timestamp"], utc=True, errors="coerce")
    for c in ["open", "high", "low", "close"]:
        out[c] = pd.to_numeric(out[c], errors="coerce")
    return out.dropna().sort_values("timestamp").drop_duplicates("timestamp").reset_index(drop=True)


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    x = df.copy()
    x["ema50"] = x.close.ewm(span=EMA_FAST, adjust=False).mean()
    x["ema200"] = x.close.ewm(span=EMA_SLOW, adjust=False).mean()
    prev = x.close.shift(1)
    tr = pd.concat([(x.high-x.low), (x.high-prev).abs(), (x.low-prev).abs()], axis=1).max(axis=1)
    x["atr"] = tr.rolling(ATR_PERIOD).mean()
    delta = x.close.diff()
    gain = delta.clip(lower=0).rolling(RSI_PERIOD).mean()
    loss = (-delta.clip(upper=0)).rolling(RSI_PERIOD).mean()
    rs = gain / loss.replace(0, pd.NA)
    x["rsi"] = (100 - 100/(1+rs)).fillna(50)
    x["atr_pct"] = x.atr / x.close.replace(0, pd.NA)
    x["atr_pctile"] = x.atr_pct.expanding(min_periods=ATR_PERIOD*3).rank(pct=True)*100
    x["prior_high"] = x.high.rolling(N).max().shift(1)
    x["prior_low"] = x.low.rolling(N).min().shift(1)
    x["ema50_slope"] = x.ema50.diff(5)
    return x


def signal(r: pd.Series) -> str:
    up = r.ema50 > r.ema200 and r.ema50_slope > 0 and r.close > r.ema50 and r.close > r.prior_high and r.rsi > 50
    dn = r.ema50 < r.ema200 and r.ema50_slope < 0 and r.close < r.ema50 and r.rsi < 50 and r.close < r.prior_low
    vol = pd.notna(r.atr_pctile) and r.atr_pctile >= ATR_MIN_PERCENTILE
    if up and vol: return "BUY"
    if dn and vol: return "SELL"
    return "NO_TRADE"


def simulate(x: pd.DataFrame, i: int, side: str, end_i: int) -> dict:
    r = x.iloc[i]
    entry_i = i + 1
    if entry_i >= len(x) or entry_i > end_i or pd.isna(r.atr) or float(r.atr) <= 0:
        return {"status": "NO_ENTRY"}
    entry = float(x.iloc[entry_i].open)
    dist = SL_ATR * float(r.atr)
    sl = entry-dist if side == "BUY" else entry+dist
    tp = entry+TP_R*dist if side == "BUY" else entry-TP_R*dist
    for j in range(entry_i, min(end_i, len(x)-1) + 1):
        b = x.iloc[j]
        hit_sl = float(b.low) <= sl if side == "BUY" else float(b.high) >= sl
        hit_tp = float(b.high) >= tp if side == "BUY" else float(b.low) <= tp
        base = {"signal_timestamp":r.timestamp,"entry_timestamp":x.iloc[entry_i].timestamp,"entry_price":entry,"stop_loss":sl,"take_profit":tp,"exit_timestamp":b.timestamp}
        if hit_sl and hit_tp:
            return {"status":"AMBIGUOUS", "r_multiple":None, **base}
        if hit_tp:
            return {"status":"TP", "r_multiple":TP_R, **base}
        if hit_sl:
            return {"status":"SL", "r_multiple":-1.0, **base}
    return {"status":"TIMEOUT", "r_multiple":None, "signal_timestamp":r.timestamp,"entry_timestamp":x.iloc[entry_i].timestamp,"entry_price":entry,"stop_loss":sl,"take_profit":tp,"exit_timestamp":None}


def run(path: Path, output: Path, start_date: str | None, end_date: str | None) -> dict:
    x = add_features(load_ohlc(path))
    dates = x.timestamp.dt.date
    start_i = 0 if start_date is None else int(x.index[dates >= pd.Timestamp(start_date).date()][0])
    end_candidates = x.index[dates <= pd.Timestamp(end_date).date()] if end_date else x.index
    end_i = int(end_candidates[-1])
    warm = max(EMA_SLOW, N, ATR_PERIOD*3) + 1
    i = max(warm, start_i)
    trades = []
    while i < min(end_i, len(x)-1):
        side = signal(x.iloc[i])
        if side == "NO_TRADE":
            i += 1; continue
        result = simulate(x, i, side, end_i)
        result.update({"direction":side,"model_version":"ATB_V1_EXECUTION_ADAPTER","sl_atr":SL_ATR,"tp_R":TP_R})
        trades.append(result)
        if result.get("exit_timestamp") is not None:
            idx = x.index[x.timestamp.eq(result["exit_timestamp"])]
            i = int(idx[0]) + 1 if len(idx) else i+1
        else:
            i += 1
    df = pd.DataFrame(trades)
    output.mkdir(parents=True, exist_ok=True)
    df.to_csv(output/"trades.csv", index=False)
    summary = {"model_version":"ATB_V1_EXECUTION_ADAPTER","input":str(path),"evaluation_start":str(x.iloc[start_i].timestamp),"evaluation_end":str(x.iloc[end_i].timestamp),"parameters":{"N":N,"ATR_PERIOD":ATR_PERIOD,"RSI_PERIOD":RSI_PERIOD,"EMA_FAST":EMA_FAST,"EMA_SLOW":EMA_SLOW,"ATR_MIN_PERCENTILE":ATR_MIN_PERCENTILE,"SL_ATR":SL_ATR,"TP_R":TP_R},"rows":int(len(x)),"trades":int(len(df))}
    valid = df[df.r_multiple.notna()].copy() if not df.empty else pd.DataFrame()
    if not valid.empty:
        eq = valid.r_multiple.cumsum(); wins=int((valid.r_multiple>0).sum()); losses=int((valid.r_multiple<0).sum())
        gl=float(-valid.loc[valid.r_multiple<0,'r_multiple'].sum()); gw=float(valid.loc[valid.r_multiple>0,'r_multiple'].sum())
        summary.update({"resolved_trades":int(len(valid)),"wins":wins,"losses":losses,"win_rate":wins/len(valid),"profit_factor":gw/gl if gl else None,"expectancy_R":float(valid.r_multiple.mean()),"total_R":float(valid.r_multiple.sum()),"max_drawdown_R":float((eq-eq.cummax()).min()),"ambiguous":int((df.status=='AMBIGUOUS').sum()),"timeouts":int((df.status=='TIMEOUT').sum())})
    else:
        summary.update({"resolved_trades":0,"wins":0,"losses":0,"win_rate":None,"profit_factor":None,"expectancy_R":None,"total_R":0.0,"max_drawdown_R":0.0,"ambiguous":int((df.status=='AMBIGUOUS').sum()) if not df.empty else 0,"timeouts":int((df.status=='TIMEOUT').sum()) if not df.empty else 0})
    summary.update({"entry_protocol":"next_bar_open","lookahead_safe":True,"costs_applied":False,"official_profitability_claim_allowed":False})
    (output/"metrics.json").write_text(json.dumps(summary,indent=2,default=str),encoding="utf-8")
    return summary


def main():
    p=argparse.ArgumentParser(); p.add_argument("input_csv",type=Path); p.add_argument("output_dir",type=Path); p.add_argument("--start-date"); p.add_argument("--end-date"); a=p.parse_args()
    print(json.dumps(run(a.input_csv,a.output_dir,a.start_date,a.end_date),indent=2,default=str))

if __name__ == "__main__": main()
