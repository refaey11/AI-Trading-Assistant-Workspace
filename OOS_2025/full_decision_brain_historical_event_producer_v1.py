from __future__ import annotations
import argparse,json
from pathlib import Path
from typing import Any
import pandas as pd
from RECOVERED_SOURCES.DECISION_BRAIN_V1 import decision_brain
from OOS_2025.full_decision_brain_assembler_v1 import assemble_decision_event
REQUIRED_CONTEXT={"timestamp"}; REQUIRED_MURPHY={"timestamp","status","direction","source_rule_id"}; REQUIRED_NISON={"timestamp","confirmation","contradiction","source_rule_id"}; REQUIRED_RISK={"timestamp","risk_status"}; REQUIRED_EXECUTION={"timestamp","entry_price","atr"}; REQUIRED_TIZ={"timestamp","process_gate"}

def _read(path:Path,required:set[str])->pd.DataFrame:
 df=pd.read_csv(path); missing=required-set(df.columns)
 if missing: raise ValueError(f"{path}: missing required columns: {sorted(missing)}")
 df["timestamp"]=pd.to_datetime(df["timestamp"],utc=True,errors="coerce")
 if df["timestamp"].isna().any(): raise ValueError(f"{path}: invalid timestamps")
 return df.sort_values("timestamp").drop_duplicates("timestamp",keep="last")

def _read_tiz(path:Path|None): return None if path is None else _read(path,REQUIRED_TIZ)

def _optional_tiz(ts,tiz):
 if tiz is None: return {"process_gate":"NOT_EVALUABLE"}
 row=tiz.loc[tiz["timestamp"]<=ts].tail(1)
 return {"process_gate":"NOT_EVALUABLE"} if row.empty else row.iloc[0].drop(labels=["timestamp"],errors="ignore").to_dict()

def _decision_ready_tiz(t,optional_tiz):
 state=str(t.get("process_gate") or t.get("status") or "NOT_EVALUABLE").upper()
 if state in {"PASS","READY","AVAILABLE"}: return dict(t)
 if optional_tiz and state=="NOT_EVALUABLE": return {**t,"process_gate":"AVAILABLE","tiz_verified":False}
 return dict(t)

def _pick_context(df,ts):
 row=df.loc[df["timestamp"]<=ts].tail(1)
 return {} if row.empty else row.iloc[0].drop(labels=["timestamp"],errors="ignore").to_dict()

def build_events(*,market_context,murphy,nison,risk,execution,tiz,year,optional_tiz):
 timestamps=sorted(set(murphy["timestamp"])&set(nison["timestamp"])&set(risk["timestamp"])&set(execution["timestamp"]))
 records=[]
 for ts in timestamps:
  if ts.year!=year: continue
  m=murphy.loc[murphy["timestamp"]==ts].iloc[0]; n=nison.loc[nison["timestamp"]==ts].iloc[0]; r=risk.loc[risk["timestamp"]==ts].iloc[0]; e=execution.loc[execution["timestamp"]==ts].iloc[0]
  t=_optional_tiz(ts,tiz); td=_decision_ready_tiz(t,optional_tiz)
  result=assemble_decision_event(decision_brain_module=decision_brain,row=_pick_context(market_context,ts),query_as_of=str(ts),murphy_evidence=m.drop(labels=["timestamp"],errors="ignore").to_dict(),nison_evidence=n.drop(labels=["timestamp"],errors="ignore").to_dict(),tiz_evidence=td,risk_evidence=r.drop(labels=["timestamp"],errors="ignore").to_dict(),historical_evidence=None,source_rule_ids=[str(m["source_rule_id"]),str(n["source_rule_id"])],entry_price=float(e["entry_price"]),atr=float(e["atr"]),mode="oos_evaluation",provenance={"producer":"full_decision_brain_historical_event_producer_v1","evaluation_year":year,"optional_tiz":optional_tiz})
  records.append({"timestamp":ts,"evaluation_year":year,"status":result.get("status"),"direction":result.get("decision",{}).get("decision",{}).get("final"),"execution_status":result.get("execution_plan",{}).get("status"),"entry_price":result.get("execution_plan",{}).get("entry_price"),"stop_loss":result.get("execution_plan",{}).get("stop_loss"),"take_profit":result.get("execution_plan",{}).get("take_profit"),"risk_pass":r.get("risk_status"),"tiz_verified":bool(t.get("tiz_verified",False)),"tiz_status":t.get("process_gate",t.get("status","NOT_EVALUABLE")),"nison_confirmation":n.get("confirmation"),"nison_contradiction":bool(n.get("contradiction",False)),"murphy_direction":m.get("direction"),"murphy_status":m.get("status"),"source_rule_ids":json.dumps([str(m["source_rule_id"]),str(n["source_rule_id"])]),"reason":result.get("reason") or result.get("decision",{}).get("decision",{}).get("reasons_against",[])})
 return pd.DataFrame(records)

def main()->int:
 p=argparse.ArgumentParser(); p.add_argument("--context",required=True,type=Path); p.add_argument("--murphy",required=True,type=Path); p.add_argument("--nison",required=True,type=Path); p.add_argument("--risk",required=True,type=Path); p.add_argument("--execution",required=True,type=Path); p.add_argument("--tiz",type=Path); p.add_argument("--year",required=True,type=int); p.add_argument("--output",required=True,type=Path); p.add_argument("--manifest",required=True,type=Path); p.add_argument("--optional-tiz",action="store_true"); a=p.parse_args()
 context=_read(a.context,REQUIRED_CONTEXT); murphy=_read(a.murphy,REQUIRED_MURPHY); nison=_read(a.nison,REQUIRED_NISON); risk=_read(a.risk,REQUIRED_RISK); execution=_read(a.execution,REQUIRED_EXECUTION); tiz=_read_tiz(a.tiz); events=build_events(market_context=context,murphy=murphy,nison=nison,risk=risk,execution=execution,tiz=tiz,year=a.year,optional_tiz=a.optional_tiz); a.output.parent.mkdir(parents=True,exist_ok=True); a.manifest.parent.mkdir(parents=True,exist_ok=True); events.to_csv(a.output,index=False); result={"status":"PASS","evaluation_year":a.year,"events":int(len(events)),"executable":int((events["status"]=="EXECUTABLE").sum()) if not events.empty else 0,"no_trade":int((events["status"]=="NO_TRADE").sum()) if not events.empty else 0,"not_evaluable":int((events["status"]=="NOT_EVALUABLE").sum()) if not events.empty else 0,"tiz_verified_events":int(events["tiz_verified"].fillna(False).astype(bool).sum()) if not events.empty else 0,"optional_tiz":bool(a.optional_tiz),"oos_tuning":False,"new_rule_semantics":False,"source_backed_components_only":True}; a.manifest.write_text(json.dumps(result,indent=2)); print(json.dumps(result,indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
