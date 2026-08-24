from __future__ import annotations
import argparse,json
from pathlib import Path
import pandas as pd
REQUIRED={"timestamp","close","atr20"}
def build(source:Path,output_dir:Path,year:int)->dict:
 df=pd.read_csv(source); missing=sorted(REQUIRED-set(df.columns))
 if missing: raise ValueError(f"source missing required columns: {missing}")
 df["timestamp"]=pd.to_datetime(df["timestamp"],utc=True,errors="coerce")
 if df["timestamp"].isna().any(): raise ValueError("invalid timestamps in authoritative market-state source")
 df=df[df["timestamp"].dt.year==year].sort_values("timestamp").drop_duplicates("timestamp",keep="last")
 df=df[df["close"].notna()&df["atr20"].notna()&(df["atr20"]>0)]
 if df.empty: raise ValueError(f"no usable rows for year {year}")
 output_dir.mkdir(parents=True,exist_ok=True)
 context=df[[c for c in df.columns if c not in {"open","high","low"}]].copy(); context["entry_price"]=context["close"]; context["atr"]=context["atr20"]; context.to_csv(output_dir/"context.csv",index=False)
 execution=df[["timestamp","close","atr20"]].rename(columns={"close":"entry_price","atr20":"atr"}); execution.to_csv(output_dir/"execution.csv",index=False)
 m={"status":"PASS","mode":"SOURCE_BACKED_CONTEXT_EXECUTION_INPUTS","evaluation_year":year,"rows":int(len(df)),"entry_policy":"event_close","atr_source":"atr20","direction_created":False,"risk_created":False,"tiz_created":False,"source_backed_only":True,"tuning":False}; (output_dir/"CONTEXT_EXECUTION_INPUT_MANIFEST.json").write_text(json.dumps(m,indent=2)); return m
def main()->int:
 p=argparse.ArgumentParser(); p.add_argument("--source",required=True,type=Path); p.add_argument("--output-dir",required=True,type=Path); p.add_argument("--year",required=True,type=int); a=p.parse_args(); print(json.dumps(build(a.source,a.output_dir,a.year),indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
