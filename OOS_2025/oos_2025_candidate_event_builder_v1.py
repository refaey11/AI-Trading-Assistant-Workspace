#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd

CANDIDATES = {
    "C1_HIGH_STRONG_BEARISH_MTF": lambda d: (d.volatility_state == "HIGH") & (d.mtf_context == "strong_bearish"),
    "C2_HIGH_H4_BEARISH": lambda d: (d.volatility_state == "HIGH") & (d.H4_trend_regime == -1),
    "C3_SELL_HIGH": lambda d: (d.direction == "SELL") & (d.volatility_state == "HIGH"),
}

def first_nonblank(primary, fallback, index):
    p = primary.astype("string") if primary is not None else pd.Series(pd.NA, index=index, dtype="string")
    f = fallback.astype("string") if fallback is not None else pd.Series(pd.NA, index=index, dtype="string")
    p = p.mask(p.str.strip().eq("") | p.isna())
    return p.fillna(f)

def main():
    ap = argparse.ArgumentParser()
    for n in ["murphy", "h1", "market-state", "mtf", "out-dir"]: ap.add_argument("--" + n, required=True)
    a = ap.parse_args(); out = Path(a.out_dir); out.mkdir(parents=True, exist_ok=True)
    mur = pd.read_csv(a.murphy, low_memory=False); h1 = pd.read_csv(a.h1, low_memory=False)
    ms = pd.read_csv(a.market_state, low_memory=False); mtf = pd.read_csv(a.mtf, low_memory=False)
    for df in [mur,h1,ms,mtf]: df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce", format="mixed")
    if any(df.timestamp.isna().any() for df in [mur,h1,ms,mtf]): raise SystemExit("FAIL_CLOSED_INVALID_TIMESTAMP")
    if set(mur.timestamp.dt.year.astype(int)) - {2025}: raise SystemExit("FAIL_CLOSED_MURPHY_NOT_2025_ONLY")
    mur["status"] = mur.get("status", pd.Series("", index=mur.index)).astype(str).str.upper().str.strip()
    mur["direction"] = first_nonblank(mur["direction"] if "direction" in mur.columns else None, mur["directional_confirmation"] if "directional_confirmation" in mur.columns else None, mur.index).str.upper().str.strip()
    mur["source_rule_id"] = first_nonblank(mur["source_rule_id"] if "source_rule_id" in mur.columns else None, mur["rule_id"] if "rule_id" in mur.columns else None, mur.index).fillna("")
    mur = mur[(mur.status == "PASS") & mur.direction.isin(["BUY","SELL","BULLISH","BEARISH"])].copy()
    mur["direction"] = mur.direction.replace({"BULLISH":"BUY","BEARISH":"SELL"})
    h1 = h1.sort_values("timestamp").drop_duplicates("timestamp", keep="last").reset_index(drop=True)
    if {"open","high","low","close"} - set(h1.columns): raise SystemExit("FAIL_CLOSED_H1_MISSING_OHLC")
    for c in ["open","high","low","close"]: h1[c] = pd.to_numeric(h1[c], errors="coerce")
    prev_close=h1.close.shift(1); tr=pd.concat([(h1.high-h1.low),(h1.high-prev_close).abs(),(h1.low-prev_close).abs()],axis=1).max(axis=1)
    h1["ATR20"] = tr.rolling(20,min_periods=20).mean().shift(1)
    ms=ms.sort_values("timestamp").drop_duplicates("timestamp", keep="last"); mtf=mtf.sort_values("timestamp").drop_duplicates("timestamp", keep="last"); mur=mur.sort_values("timestamp")
    if "volatility_state" not in ms.columns: raise SystemExit("FAIL_CLOSED_MARKET_STATE_MISSING_VOLATILITY_STATE")
    x=pd.merge_asof(mur,ms[[c for c in ["timestamp","volatility_state","trend","location"] if c in ms.columns]],on="timestamp",direction="backward",allow_exact_matches=False)
    if {"mtf_context","H4_trend_regime"}-set(mtf.columns): raise SystemExit("FAIL_CLOSED_MTF_REQUIRED_FIELDS")
    x=pd.merge_asof(x,mtf[[c for c in ["timestamp","mtf_context","H4_trend_regime","mtf_trend_score"] if c in mtf.columns]],on="timestamp",direction="backward",allow_exact_matches=False)
    x=pd.merge_asof(x,h1[["timestamp","ATR20"]],on="timestamp",direction="backward",allow_exact_matches=False)
    x["ATR20"]=pd.to_numeric(x.ATR20,errors="coerce"); x["H4_trend_regime"]=pd.to_numeric(x.H4_trend_regime,errors="coerce")
    x["volatility_state"]=x.volatility_state.astype("string").str.upper().str.strip(); x["mtf_context"]=x.mtf_context.astype("string").str.lower().str.strip()
    base=x.dropna(subset=["ATR20","volatility_state"]).copy()
    if base.empty: raise SystemExit("FAIL_CLOSED_NO_2025_EVENTS_AFTER_ATR_VOLATILITY_GATES")
    # Compare Timestamp objects directly. This avoids pandas 3 datetime-resolution
    # mismatches (us vs ns) that can make every event appear after the H1 window.
    h1_index = pd.DatetimeIndex(h1["timestamp"])
    rows=[]; skipped_end=0; skipped_missing_h4=0
    for r in base.itertuples(index=False):
        if pd.isna(r.H4_trend_regime) and (r.direction=="SELL" or r.mtf_context=="strong_bearish"): skipped_missing_h4+=1; continue
        j=int(h1_index.searchsorted(r.timestamp, side="right"))
        if j>=len(h1): skipped_end+=1; continue
        entry=float(h1.iloc[j].open); atr=float(r.ATR20)
        if not np.isfinite(entry) or atr<=0: continue
        dist=.75*atr; sl=entry-dist if r.direction=="BUY" else entry+dist; tp=entry+2*dist if r.direction=="BUY" else entry-2*dist
        outcome="OPEN"; exit_time=None; net=None
        for k in range(j,len(h1)):
            b=h1.iloc[k]; hi=float(b.high); lo=float(b.low); hit_sl=(lo<=sl) if r.direction=="BUY" else (hi>=sl); hit_tp=(hi>=tp) if r.direction=="BUY" else (lo<=tp)
            if hit_sl and hit_tp: outcome="AMBIGUOUS"; exit_time=b.timestamp; break
            if hit_tp: outcome="TP"; exit_time=b.timestamp; net=2.0; break
            if hit_sl: outcome="SL"; exit_time=b.timestamp; net=-1.0; break
        rows.append({"event_time":r.timestamp,"direction":r.direction,"source_rule_id":getattr(r,"source_rule_id",""),"volatility_state":r.volatility_state,"mtf_context":r.mtf_context,"H4_trend_regime":r.H4_trend_regime,"entry_time":h1.iloc[j].timestamp,"entry_price":entry,"ATR20_asof":atr,"exit_time":exit_time,"outcome":outcome,"net_R":net})
    ev=pd.DataFrame(rows)
    if ev.empty:
        print(json.dumps({"base_rows":len(base),"skipped_end":skipped_end,"skipped_missing_h4":skipped_missing_h4},indent=2)); raise SystemExit("FAIL_CLOSED_NO_2025_EVENTS_AFTER_ASOF_EXECUTION_GATES")
    ev.to_csv(out/"oos_2025_candidate_events.csv",index=False)
    stats=[]
    for cid,fn in CANDIDATES.items():
        g=ev[fn(ev)]; r=pd.to_numeric(g.net_R,errors="coerce").dropna(); wins=r[r>0].sum(); losses=-r[r<0].sum()
        stats.append({"candidate_id":cid,"events":len(g),"evaluated":len(r),"TP":int((g.outcome=="TP").sum()),"SL":int((g.outcome=="SL").sum()),"ambiguous":int((g.outcome=="AMBIGUOUS").sum()),"open":int((g.outcome=="OPEN").sum()),"win_rate":float((r>0).mean()) if len(r) else None,"expectancy_R":float(r.mean()) if len(r) else None,"profit_factor":float(wins/losses) if losses else None,"total_net_R":float(r.sum()) if len(r) else 0.0})
    pd.DataFrame(stats).to_csv(out/"oos_2025_candidate_results.csv",index=False)
    manifest={"status":"OOS_2025_EVALUATION_ONLY","window":"2025-only","candidate_set_frozen":True,"tuning_applied":False,"threshold_sweep":False,"future_data_used":False,"strict_asof_context":True,"missing_evidence_policy":"candidate-specific NOT_EVALUABLE","atr20_source":"H1_completed_bars_fallback_when_market_state_missing","entry_next_h1_open":True,"stop_atr":0.75,"target_R":2.0,"official_profitability_claim_allowed":False,"canonical_three_book_mode":False}
    (out/"oos_2025_candidate_manifest.json").write_text(json.dumps(manifest,indent=2)); print(pd.DataFrame(stats).to_string(index=False)); print(json.dumps(manifest,indent=2))
if __name__=="__main__": main()
