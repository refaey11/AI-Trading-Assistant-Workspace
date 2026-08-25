from __future__ import annotations
import argparse,json,sys
from pathlib import Path
from typing import Any
import pandas as pd

# Ensure repository root is importable when CircleCI invokes this script from OOS_2025.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from RECOVERED_SOURCES.DECISION_BRAIN_V1 import decision_brain
from OOS_2025.full_decision_brain_assembler_v1 import assemble_decision_event
from OOS_2025.governed_rule_fan_in_v1 import build_lossless_rule_groups, legacy_selected_row
REQUIRED_CONTEXT={"timestamp"}; REQUIRED_MURPHY={"timestamp","status","direction","source_rule_id"}; REQUIRED_NISON={"timestamp","confirmation","contradiction","source_rule_id"}; REQUIRED_RISK={"timestamp","risk_status"}; REQUIRED_EXECUTION={"timestamp","entry_price","atr"}; REQUIRED_TIZ={"timestamp","process_gate"}

def _read(path:Path,required:set[str],*,preserve_rule_rows:bool=False)->pd.DataFrame:
 df=pd.read_csv(path); missing=required-set(df.columns)
 if missing: raise ValueError(f"{path}: missing required columns: {sorted(missing)}")
 df["timestamp"]=pd.to_datetime(df["timestamp"],utc=True,errors="coerce")
 if df["timestamp"].isna().any(): raise ValueError(f"{path}: invalid timestamps")
 df=df.sort_values("timestamp",kind="stable")
 if not preserve_rule_rows:
  df=df.drop_duplicates("timestamp",keep="last")
 return df

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

def _governed_source_rule_ids(murphy_id: Any, nison_id: Any) -> list[str]:
    """Return only real frozen rule IDs; never pass synthetic NISON_NONE."""
    out=[]
    for value in (murphy_id, nison_id):
        rid=str(value or "").strip()
        if not rid or rid == "NISON_NONE":
            continue
        out.append(rid)
    return out

def build_events(*,market_context,murphy,nison,risk,execution,tiz,year,optional_tiz):
 timestamps=sorted(set(murphy["timestamp"])&set(nison["timestamp"])&set(risk["timestamp"])&set(execution["timestamp"]))
 murphy_groups=build_lossless_rule_groups(murphy)
 nison_groups=build_lossless_rule_groups(nison)
 records=[]
 for ts in timestamps:
  if ts.year!=year: continue
  m_rows=murphy_groups.get(ts,[]); n_rows=nison_groups.get(ts,[])
  m=legacy_selected_row(m_rows); n=legacy_selected_row(n_rows)
  r=risk.loc[risk["timestamp"]==ts].iloc[0]; e=execution.loc[execution["timestamp"]==ts].iloc[0]
  t=_optional_tiz(ts,tiz); td=_decision_ready_tiz(t,optional_tiz)
  source_rule_ids=_governed_source_rule_ids(m.get("source_rule_id"), n.get("source_rule_id"))
  result=assemble_decision_event(decision_brain_module=decision_brain,row=_pick_context(market_context,ts),query_as_of=str(ts),murphy_evidence=m,nison_evidence=n,tiz_evidence=td,risk_evidence=r.drop(labels=["timestamp"],errors="ignore").to_dict(),historical_evidence=None,source_rule_ids=source_rule_ids,entry_price=float(e["entry_price"]),atr=float(e["atr"]),mode="oos_evaluation",provenance={"producer":"full_decision_brain_historical_event_producer_v1","evaluation_year":year,"optional_tiz":optional_tiz,"nison_source_rule_sentinel_omitted":not bool(n.get("source_rule_id")),"fan_in_mode":"LOSSLESS_PROVENANCE_LEGACY_DECISION_COMPAT","murphy_rule_ids_preserved":[str(x.get("source_rule_id")) for x in m_rows],"nison_rule_ids_preserved":[str(x.get("source_rule_id")) for x in n_rows]})
  records.append({"timestamp":ts,"evaluation_year":year,"status":result.get("status"),"direction":result.get("decision",{}).get("decision",{}).get("final"),"execution_status":result.get("execution_plan",{}).get("status"),"entry_price":result.get("execution_plan",{}).get("entry_price"),"stop_loss":result.get("execution_plan",{}).get("stop_loss"),"take_profit":result.get("execution_plan",{}).get("take_profit"),"risk_pass":r.get("risk_status"),"tiz_verified":bool(t.get("tiz_verified",False)),"tiz_status":t.get("process_gate",t.get("status","NOT_EVALUABLE")),"nison_confirmation":n.get("confirmation"),"nison_contradiction":bool(n.get("contradiction",False)),"murphy_direction":m.get("direction"),"murphy_status":m.get("status"),"source_rule_ids":json.dumps(source_rule_ids),"murphy_rule_count":len(m_rows),"nison_rule_count":len(n_rows),"murphy_rule_ids":json.dumps([str(x.get("source_rule_id")) for x in m_rows]),"nison_rule_ids":json.dumps([str(x.get("source_rule_id")) for x in n_rows]),"reason":result.get("reason") or result.get("decision",{}).get("decision",{}).get("reasons_against",[])})
 return pd.DataFrame(records)

def main()->int:
 p=argparse.ArgumentParser(); p.add_argument("--context",required=True,type=Path); p.add_argument("--murphy",required=True,type=Path); p.add_argument("--nison",required=True,type=Path); p.add_argument("--risk",required=True,type=Path); p.add_argument("--execution",required=True,type=Path); p.add_argument("--tiz",type=Path); p.add_argument("--year",required=True,type=int); p.add_argument("--output",required=True,type=Path); p.add_argument("--manifest",required=True,type=Path); p.add_argument("--optional-tiz",action="store_true"); a=p.parse_args()
 context=_read(a.context,REQUIRED_CONTEXT); murphy=_read(a.murphy,REQUIRED_MURPHY,preserve_rule_rows=True); nison=_read(a.nison,REQUIRED_NISON,preserve_rule_rows=True); risk=_read(a.risk,REQUIRED_RISK); execution=_read(a.execution,REQUIRED_EXECUTION); tiz=_read_tiz(a.tiz); events=build_events(market_context=context,murphy=murphy,nison=nison,risk=risk,execution=execution,tiz=tiz,year=a.year,optional_tiz=a.optional_tiz); a.output.parent.mkdir(parents=True,exist_ok=True); a.manifest.parent.mkdir(parents=True,exist_ok=True); events.to_csv(a.output,index=False); result={"status":"PASS","evaluation_year":a.year,"events":int(len(events)),"executable":int((events["status"]=="EXECUTABLE").sum()) if not events.empty else 0,"no_trade":int((events["status"]=="NO_TRADE").sum()) if not events.empty else 0,"not_evaluable":int((events["status"]=="NOT_EVALUABLE").sum()) if not events.empty else 0,"tiz_verified_events":int(events["tiz_verified"].fillna(False).astype(bool).sum()) if not events.empty else 0,"optional_tiz":bool(a.optional_tiz),"oos_tuning":False,"new_rule_semantics":False,"source_backed_components_only":True,"fan_in_mode":"LOSSLESS_PROVENANCE_LEGACY_DECISION_COMPAT","rule_rows_preserved":True}; a.manifest.write_text(json.dumps(result,indent=2)); print(json.dumps(result,indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
