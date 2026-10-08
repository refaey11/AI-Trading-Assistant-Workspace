from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from MURPHY_EVALUATORS_V1.murphy_runtime_entrypoint_v1 import evaluate_rule

MURPHY_RULES = (
    "MURPHY_0003","MURPHY_0004","MURPHY_0006","MURPHY_0007",
    "MURPHY_0018","MURPHY_0019","MURPHY_0021","MURPHY_0022","MURPHY_0023",
    "MURPHY_0025","MURPHY_0026","MURPHY_0028","MURPHY_0029","MURPHY_0030",
    "MURPHY_0031","MURPHY_0032","MURPHY_0033","MURPHY_0034","MURPHY_0035",
    "MURPHY_0036","MURPHY_0037","MURPHY_0038","MURPHY_0039","MURPHY_0040",
    "MURPHY_0041","MURPHY_0042","MURPHY_0043","MURPHY_0044","MURPHY_0045",
    "MURPHY_0047","MURPHY_0048","MURPHY_0049","MURPHY_0050","MURPHY_0051",
)
DEV_START = pd.Timestamp("2016-01-01", tz="UTC")
DEV_END = pd.Timestamp("2025-01-01", tz="UTC")

def load_xau(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    req={"timestamp","open","high","low","close"}
    missing=sorted(req-set(df.columns))
    if missing: raise ValueError(f"Missing OHLC columns: {missing}")
    df["timestamp"]=pd.to_datetime(df["timestamp"],utc=True,errors="coerce")
    if df["timestamp"].isna().any() or df["timestamp"].duplicated().any():
        raise ValueError("Invalid or duplicated timestamps")
    df=df.sort_values("timestamp").reset_index(drop=True)
    return df[(df.timestamp>=DEV_START)&(df.timestamp<DEV_END)].reset_index(drop=True)

def pivots(df):
    lo=df.low.to_numpy(float); hi=df.high.to_numpy(float); n=len(df)
    pl=np.zeros(n,dtype=bool); ph=np.zeros(n,dtype=bool)
    for i in range(2,n-2):
        pl[i]=lo[i]<lo[i-1] and lo[i]<lo[i-2] and lo[i]<lo[i+1] and lo[i]<lo[i+2]
        ph[i]=hi[i]>hi[i-1] and hi[i]>hi[i-2] and hi[i]>hi[i+1] and hi[i]>hi[i+2]
    return pl,ph

def atr14(df):
    c=df.close.to_numpy(float); h=df.high.to_numpy(float); l=df.low.to_numpy(float)
    prev=np.r_[np.nan,c[:-1]]
    tr=np.maximum.reduce([h-l,np.abs(h-prev),np.abs(l-prev)])
    return pd.Series(tr).ewm(alpha=1/14,adjust=False,min_periods=14).mean().to_numpy()

def emit(df):
    pl,ph=pivots(df); atr=atr14(df); rows=[]
    for i in range(len(df)):
        lows=np.where(pl[:i+1])[0]; highs=np.where(ph[:i+1])[0]
        payload={
            "events":[],"line_price_at":{},
            "atr":float(atr[i]) if np.isfinite(atr[i]) else None,
            "current_reaction_peak":float(df.high.iloc[highs[-1]]) if len(highs) else None,
            "prior_reaction_peak":float(df.high.iloc[highs[-2]]) if len(highs)>=2 else None,
            "current_reaction_trough":float(df.low.iloc[lows[-1]]) if len(lows) else None,
            "prior_reaction_trough":float(df.low.iloc[lows[-2]]) if len(lows)>=2 else None,
        }
        for rule_id in MURPHY_RULES:
            if rule_id in {"MURPHY_0006","MURPHY_0007"}:
                result={"rule_id":rule_id,"status":"NOT_EVALUABLE",
                        "reason":"Requires source-backed event/line geometry; OHLC adapter will not synthesize it."}
            elif rule_id in {"MURPHY_0039","MURPHY_0042","MURPHY_0043","MURPHY_0044","MURPHY_0045"}:
                result={"rule_id":rule_id,"status":"NOT_EVALUABLE",
                        "reason":"Requires explicit process/capital/exposure/margin source inputs; OHLC is insufficient."}
            else:
                result=evaluate_rule(rule_id,payload)
            direction="UNKNOWN"
            if result["status"]=="PASS" and rule_id=="MURPHY_0003": direction="BULLISH"
            if result["status"]=="PASS" and rule_id=="MURPHY_0004": direction="BEARISH"
            rows.append({
                "timestamp":df.timestamp.iloc[i],"rule_id":rule_id,
                "status":result["status"],"direction":direction,
                "reason":result["reason"],"source":"XAUUSD_M1_MASTER_2016_2026_08_V1",
                "as_of_timestamp":df.timestamp.iloc[i],"2025_excluded":True,
            })
    return pd.DataFrame(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    df=load_xau(args.input); evidence=emit(df)
    args.output.parent.mkdir(parents=True,exist_ok=True); evidence.to_csv(args.output,index=False)
    manifest={
        "status":"PASS_WITH_NOT_EVALUABLES","mode":"XAUUSD_MURPHY_EVIDENCE_ADAPTER_V1",
        "development_window":"2016-2024","rules":len(MURPHY_RULES),
        "rows":int(len(evidence)),"2025_used":False,
        "lookahead_policy":"confirmed-past-pivots-only","fail_closed":True,
        "synthetic_geometry":False,"source":str(args.input),"output":str(args.output),
    }
    (args.output.parent/"XAUUSD_MURPHY_EVIDENCE_MANIFEST.json").write_text(
        json.dumps(manifest,indent=2,sort_keys=True),encoding="utf-8")
    print(json.dumps(manifest,indent=2))
if __name__=="__main__":
    main()
