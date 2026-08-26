from __future__ import annotations

import argparse, json, math, sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from RECOVERED_SOURCES.DECISION_BRAIN_V1 import decision_brain

DIRECTIONAL = {"BULLISH", "BEARISH"}
LOCKED = 2025
SCORES = {"BULL_TREND":1.0,"BULLISH":1.0,"UPTREND":1.0,"BEAR_TREND":-1.0,"BEARISH":-1.0,"DOWNTREND":-1.0,"TRANSITION":0.0,"RANGE":0.0,"INSIDE_RANGE":0.0,"MIXED":0.0}

def read(path, required):
    df = pd.read_csv(path)
    miss = sorted(set(required)-set(df.columns))
    if miss: raise ValueError(f"{path}: missing columns {miss}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    if df.timestamp.isna().any(): raise ValueError(f"{path}: invalid timestamps")
    return df.sort_values("timestamp", kind="stable").drop_duplicates("timestamp", keep="last").reset_index(drop=True)

def norm(v):
    s=str(v or "").upper()
    if s in {"BULL","BULLISH","UP","UPTREND"}: return "BULLISH"
    if s in {"BEAR","BEARISH","DOWN","DOWNTREND"}: return "BEARISH"
    return "NONE"

def murphy_0021(h1,m1):
    from MURPHY_EVALUATORS_V1.murphy_0021_0023_evaluator import evaluate_0021
    h=h1.copy(); m=m1.copy(); h["previous_close"]=h.close.shift(1); m["h1_timestamp"]=m.timestamp.dt.floor("h")
    vol=m.groupby("h1_timestamp",as_index=False).agg(volume=("volume","sum")).sort_values("h1_timestamp")
    vol["previous_volume"]=vol.volume.shift(1); vol["volume_direction"]=None
    vol.loc[vol.volume>vol.previous_volume,"volume_direction"]="UP"; vol.loc[vol.volume<vol.previous_volume,"volume_direction"]="DOWN"
    x=h.merge(vol[["h1_timestamp","volume_direction"]],left_on="timestamp",right_on="h1_timestamp",how="left")
    out=[]
    for r in x.itertuples(index=False):
        z=evaluate_0021({"close":r.close,"previous_close":r.previous_close,"volume_direction":r.volume_direction})
        out.append({"timestamp":r.timestamp,"direction":norm(z.get("directional_confirmation"))})
    return pd.DataFrame(out)

def bucket(brain, md, mtf):
    bias=norm(brain.directional_bias)
    if md not in DIRECTIONAL: return "NO_MURPHY_DIRECTION"
    if brain.market_state=="trend" and bias==md: return "TREND_ALIGNED"
    if brain.market_state=="trend" and bias in DIRECTIONAL and bias!=md: return "TREND_OPPOSED"
    if mtf=="MIXED": return "MTF_MIXED"
    if brain.market_state=="range/transition": return "RANGE_TRANSITION"
    if brain.market_state=="uncertain": return "UNCERTAIN"
    return "OTHER"

def signed(now,future,d):
    r=(future/now)-1.0
    return r if d=="BULLISH" else -r

def audit(market,mtf,h1,m1,year,out):
    if year>=LOCKED: raise ValueError("2025_OOS_LOCKED")
    state=read(market,{"timestamp","close"}); state=state[state.timestamp.dt.year.eq(year)].copy()
    mt=read(mtf,{"timestamp","H4_trend","H1_trend","MTF_state"})
    h=read(h1,{"timestamp","open","high","low","close"}).set_index("timestamp")
    h["f12"]=h.close.shift(-12); h["f24"]=h.close.shift(-24); h["f48"]=h.close.shift(-48)
    m=read(m1,{"timestamp","open","high","low","close","volume"})
    mur=murphy_0021(h.reset_index().drop(columns=[c for c in ["f12","f24","f48"] if c in h.reset_index().columns]),m).set_index("timestamp")
    mt=mt.set_index("timestamp"); rec=[]
    for ts,s in state.set_index("timestamp").iterrows():
        if ts not in mt.index or ts not in mur.index or ts not in h.index: continue
        mr=mur.loc[ts]; tr=mt.loc[ts]; hr=h.loc[ts]; md=str(mr.direction)
        sc=(SCORES.get(str(tr.H4_trend).upper(),0.0)+SCORES.get(str(tr.H1_trend).upper(),0.0))/2.0
        brain=decision_brain.assess({"mtf_trend_score":sc,"H1_trend_regime":SCORES.get(str(tr.H1_trend).upper(),0.0),"H4_trend_regime":SCORES.get(str(tr.H4_trend).upper(),0.0),"volume_available":False},similarity=None)
        r={"timestamp":ts.isoformat(),"murphy_direction":md,"brain_state":brain.market_state,"brain_bias":brain.directional_bias,"brain_confidence":float(brain.confidence),"h4_trend":tr.H4_trend,"h1_trend":tr.H1_trend,"mtf_state":tr.MTF_state,"context_bucket":bucket(brain,md,str(tr.MTF_state)),"fwd12_signed_return":None,"fwd24_signed_return":None,"fwd48_signed_return":None}
        for n,key in [(12,"f12"),(24,"f24"),(48,"f48")]:
            fut=hr.get(key)
            if md in DIRECTIONAL and pd.notna(fut) and (ts+pd.Timedelta(hours=n)).year < LOCKED: r[f"fwd{n}_signed_return"]=signed(float(hr.close),float(fut),md)
        rec.append(r)
    df=pd.DataFrame(rec); out.parent.mkdir(parents=True,exist_ok=True); df.to_csv(out,index=False)
    sig=df[df.murphy_direction.isin(DIRECTIONAL)]
    buckets=[]
    for b,g in sig.groupby("context_bucket",dropna=False):
        row={"context_bucket":b,"signals":int(len(g))}
        for n in (12,24,48):
            x=g[f"fwd{n}_signed_return"].dropna(); row[f"fwd{n}_count"]=int(x.size); row[f"fwd{n}_hit_rate_pct"]=round(100*(x>0).mean(),4) if len(x) else 0.0; row[f"fwd{n}_mean_signed_return"]=float(x.mean()) if len(x) else 0.0
        buckets.append(row)
    summary={"status":"PASS_SHADOW_ONLY","mode":"REAL_DATA_PRE2025_CONTEXT_GATE_SHADOW_V2","evaluation_year":year,"pair":"GBPUSD","events":int(len(df)),"murphy_directional_events":int(len(sig)),"context_buckets":buckets,"brain_role":"context_and_regime_only","murphy_role":"directional_anchor_MURPHY_0021","new_rule_semantics":False,"policy_changed":False,"replacement_pnl":False,"oos_2025_locked":True,"oos_tuning":False,"future_feature_leakage":False,"nison_used":False,"memory_used":False,"risk_used":False,"execution_used":False}
    out.with_suffix(".json").write_text(json.dumps(summary,indent=2,sort_keys=True),encoding="utf-8")

def main():
    p=argparse.ArgumentParser(); p.add_argument("--market-state",type=Path,required=True); p.add_argument("--mtf",type=Path,required=True); p.add_argument("--h1",type=Path,required=True); p.add_argument("--m1",type=Path,required=True); p.add_argument("--year",type=int,required=True); p.add_argument("--output",type=Path,required=True); a=p.parse_args(); print(json.dumps(audit(a.market_state,a.mtf,a.h1,a.m1,a.year,a.output),indent=2))
if __name__=="__main__": main()
