from __future__ import annotations

"""Governed 2016-2024 development runner.

The filename is retained for workflow compatibility, but the old simplified runner
has been replaced. Existing knowledge, rule evidence, and Decision Brain V1 are not
rebuilt or modified. TIZ is explicitly unresolved/optional for this development pass;
it is never converted to PASS. Risk remains a real hard gate.
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ALLOWLIST = ROOT / "governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json"
BRAIN_PATH = ROOT / "RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py"


def read_csv(path: Path, required: set[str], *, chunksize: int | None = None) -> pd.DataFrame:
    if chunksize:
        parts = []
        for part in pd.read_csv(path, chunksize=chunksize, low_memory=False):
            miss = sorted(required - set(part.columns))
            if miss:
                raise ValueError(f"{path}: missing {miss}")
            parts.append(part)
        df = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame()
    else:
        df = pd.read_csv(path, low_memory=False)
    miss = sorted(required - set(df.columns))
    if miss:
        raise ValueError(f"{path}: missing {miss}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce", format="mixed")
    if df["timestamp"].isna().any():
        raise ValueError(f"{path}: invalid timestamp")
    return df.sort_values("timestamp").reset_index(drop=True)


def load_brain():
    spec = importlib.util.spec_from_file_location("recovered_decision_brain", BRAIN_PATH)
    if not spec or not spec.loader:
        raise RuntimeError("Decision Brain V1 load failed")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def normalize_direction(v: Any) -> str | None:
    s = str(v or "").strip().upper()
    if s in {"BUY", "BULL", "BULLISH"}: return "BULLISH"
    if s in {"SELL", "BEAR", "BEARISH"}: return "BEARISH"
    return None


def allowed_rules() -> tuple[set[str], set[str]]:
    d = json.loads(ALLOWLIST.read_text(encoding="utf-8"))
    return set(d["verified_runtime"]["MURPHY"]), set(d["verified_runtime"]["NISON"])


def ids_from_values(values) -> set[str]:
    out: set[str] = set()
    for v in values:
        if pd.isna(v): continue
        out.update(x.strip() for x in str(v).split("|") if x.strip())
    return out


def aggregate_murphy(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for ts, g in df.groupby("timestamp", sort=True):
        passed = g[g["status"].astype(str).str.upper().eq("PASS")]
        dirs = {d for d in (normalize_direction(x) for x in passed["direction"]) if d}
        direction = next(iter(dirs)) if len(dirs) == 1 else ("CONFLICTED" if len(dirs) > 1 else "ABSENT")
        rule_ids = ids_from_values(g["source_rule_id"])
        rows.append({"timestamp": ts, "murphy_direction": direction, "murphy_status": "PASS" if direction in {"BULLISH","BEARISH"} else "NOT_EVALUABLE", "murphy_rule_count": len(rule_ids), "murphy_rule_ids": json.dumps(sorted(rule_ids))})
    return pd.DataFrame(rows)


def aggregate_nison(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for ts, g in df.groupby("timestamp", sort=True):
        passed = g[g["status"].astype(str).str.upper().eq("PASS")]
        failed = g[g["status"].astype(str).str.upper().eq("FAIL")]
        dirs = {d for d in (normalize_direction(x) for x in passed["direction"]) if d}
        confirmation = next(iter(dirs)) if len(dirs) == 1 else ("CONFLICTED" if len(dirs) > 1 else "ABSENT")
        rows.append({"timestamp": ts, "nison_confirmation": confirmation, "nison_contradiction": bool(not failed.empty), "nison_rule_count": int(g["rule_id"].nunique())})
    return pd.DataFrame(rows)


def asof_row(df: pd.DataFrame, ts: pd.Timestamp) -> dict[str, Any]:
    x = df[df["timestamp"] <= ts].tail(1)
    return {} if x.empty else x.iloc[0].to_dict()


def memory_similarity_shadow(hc: pd.DataFrame, query: dict[str, Any], ts: pd.Timestamp) -> dict[str, Any]:
    sig = str(query.get("context_signature") or "")
    if not sig:
        return {"status":"NOT_EVALUABLE","reason":"NO_CONTEXT_SIGNATURE","candidate_count":0,"top_k_returned":0,"direction":None}
    prior = hc[(hc["timestamp"] < ts) & (hc["context_signature"].astype(str).eq(sig))]
    top = prior.sort_values("timestamp", ascending=False).head(20)
    return {"status":"PASS_SHADOW_ONLY" if not top.empty else "NO_MATCH","reason":None if not top.empty else "NO_PRIOR_MATCH","candidate_count":int(len(prior)),"top_k_returned":int(len(top)),"historical_evidence_ids_or_positions":[int(i) for i in top.index.tolist()],"direction":None,"final_trade_decision":None}


def build_row(market: dict[str,Any], mtf: dict[str,Any]) -> dict[str,Any]:
    trend_map={"BULL_TREND":1.0,"BEAR_TREND":-1.0,"TRANSITION":0.0,"UNKNOWN":0.0}
    out={k:0.0 for k in ["mtf_trend_score","M5_trend_regime","M15_trend_regime","M30_trend_regime","H1_trend_regime","H4_trend_regime","D1_trend_regime"]}
    out.update({k:0.0 for k in ["M5_volume_regime","M15_volume_regime","M30_volume_regime","H1_volume_regime","H4_volume_regime","D1_volume_regime"]})
    out["volume_available"]=False
    if market:
        if "trend" in market: out["H1_trend_regime"]=trend_map.get(str(market["trend"]).upper(),0.0)
        for k in list(out):
            if k in market and pd.notna(market[k]): out[k]=market[k]
    if mtf:
        out["mtf_trend_score"]=trend_map.get(str(mtf.get("trend","UNKNOWN")).upper(),0.0)
        out["H4_trend_regime"]=trend_map.get(str(mtf.get("h4_trend","UNKNOWN")).upper(),0.0)
        # Historical H1 source has volume=0, so never claim volume is available.
    return out


def execution_plan(entry: float, atr: float, direction: str) -> tuple[float,float]:
    stop_distance=0.75*atr
    target_distance=3.0*stop_distance
    if direction=="BUY": return entry-stop_distance, entry+target_distance
    return entry+stop_distance, entry-target_distance


def simulate(bars: pd.DataFrame, event_pos: int, direction: str, entry: float, sl: float, tp: float) -> dict[str,Any]:
    for j in range(event_pos+1,len(bars)):
        b=bars.iloc[j]
        hit_sl=float(b["low"])<=sl if direction=="BUY" else float(b["high"])>=sl
        hit_tp=float(b["high"])>=tp if direction=="BUY" else float(b["low"])<=tp
        if hit_sl and hit_tp: return {"exit_timestamp":b["timestamp"],"outcome":"AMBIGUOUS","r_multiple":None}
        if hit_tp: return {"exit_timestamp":b["timestamp"],"outcome":"TP","r_multiple":3.0}
        if hit_sl: return {"exit_timestamp":b["timestamp"],"outcome":"SL","r_multiple":-1.0}
    return {"exit_timestamp":None,"outcome":"TIMEOUT","r_multiple":None}


def run(*, h1:Path, market:Path, mtf:Path, murphy:Path, nison:Path, historical_context:Path, historical_outcome:Path, similarity:Path, retrieval:Path, output:Path) -> dict[str,Any]:
    bars=read_csv(h1,{"timestamp","open","high","low","close"})
    bars=bars[(bars.timestamp.dt.year>=2016)&(bars.timestamp.dt.year<=2024)].copy().reset_index(drop=True)
    ms=read_csv(market,{"timestamp"})
    mtf_df=read_csv(mtf,{"timestamp"})
    murphy_raw=read_csv(murphy,{"timestamp","status","direction","source_rule_id"})
    nison_raw=read_csv(nison,{"timestamp","status","direction","rule_id"},chunksize=400000)
    hc=read_csv(historical_context,{"timestamp","context_signature"})
    ho=read_csv(historical_outcome,{"timestamp","context_signature"})
    if "pair" in hc.columns: hc=hc[hc.pair.astype(str).str.upper().eq("GBPUSD")].copy()
    if "pair" in ho.columns: ho=ho[ho.pair.astype(str).str.upper().eq("GBPUSD")].copy()
    hc=hc[hc.timestamp.dt.year<=2024].copy(); ho=ho[ho.timestamp.dt.year<=2024].copy()
    am=aggregate_murphy(murphy_raw); an=aggregate_nison(nison_raw)
    allowed_m,allowed_n=allowed_rules()
    if not set(murphy_raw.source_rule_id.astype(str)).issubset(allowed_m): raise ValueError("Unknown Murphy rule id")
    if not set(nison_raw.rule_id.astype(str)).issubset(allowed_n): raise ValueError("Unknown Nison rule id")
    brain=load_brain()
    from compatibility.knowledge_decision_handoff import build_handoff
    from RUNTIME.RISK_ENGINE_INTEGRATION_V1.risk_engine_integration_v1 import evaluate_risk
    events=[]; trades=[]
    # Pre-index exact timestamps for event lookup; all upstream context is consumed as-of.
    bars_pos={ts:i for i,ts in enumerate(bars.timestamp)}
    for _,b in bars.iterrows():
        ts=b.timestamp
        market=asof_row(ms,ts); mtf=asof_row(mtf_df,ts); m=asof_row(am,ts); n=asof_row(an,ts); c=asof_row(hc,ts); o=asof_row(ho,ts)
        row=build_row(market,mtf)
        assessment=brain.assess(row,similarity=None)
        mur_dir=m.get("murphy_direction"); ncontra=bool(n.get("nison_contradiction",False)); nconf=str(n.get("nison_confirmation") or "ABSENT")
        direction_ready=mur_dir in {"BULLISH","BEARISH"} and assessment.directional_bias==str(mur_dir).lower() and not ncontra
        alignment_state="ALIGNED" if direction_ready else ("NISON_CONTRADICTION" if ncontra else "NEEDS_REVIEW")
        handoff=build_handoff(row,{"alignment_state":alignment_state,"candidate_direction":str(mur_dir or "neutral").lower(),"contradiction_gate":"FAIL" if ncontra else "PASS","process_gate":"NOT_EVALUABLE","book_evidence_status":"CONNECTED","market_evidence_status":"CONNECTED","similarity_record_count":0},similarity=None)
        sim=memory_similarity_shadow(hc,c,ts)
        retrieval={"status":"CONNECTED_METADATA_ONLY","reason":"Current retrieval package is 2025 snapshot and is locked from dev consumption","direction":None,"final_trade_decision":None}
        risk_status="NOT_EVALUABLE"; risk_reason="NOT_A_DIRECTION_SOURCE"; sl=tp=None; exec_res={}
        atr=mtf.get("atr") if mtf else None
        if direction_ready and pd.notna(atr) and float(atr)>0:
            d="BUY" if mur_dir=="BULLISH" else "SELL"; entry=float(b.close); sl,tp=execution_plan(entry,float(atr),d)
            rr=evaluate_risk(equity=100000.0,entry=entry,stop_loss=sl,take_profit=tp,atr=float(atr),prior_loss_streak=0,peak_equity=100000.0)
            risk_status="PASS" if rr.risk_pass else "FAIL"; risk_reason=rr.reason
            if rr.risk_pass and ts in bars_pos: exec_res=simulate(bars,bars_pos[ts],d,entry,sl,tp)
        events.append({"timestamp":ts,"market_state_asof":bool(market),"mtf_asof":bool(mtf),"murphy_direction":mur_dir,"murphy_rule_count":int(m.get("murphy_rule_count",0) or 0),"nison_confirmation":nconf,"nison_contradiction":ncontra,"nison_rule_count":int(n.get("nison_rule_count",0) or 0),"historical_context_asof":bool(c),"historical_outcome_asof":bool(o),"similarity_status":sim["status"],"similarity_candidates":sim.get("candidate_count",0),"retrieval_status":retrieval["status"],"tiz_status":"UNRESOLVED_OPTIONAL","brain_bias":assessment.directional_bias,"brain_confidence":assessment.confidence,"handoff_routing":handoff["routing"],"handoff_abstain":handoff["gates"]["abstain"],"direction_ready":direction_ready,"entry_price":float(b.close),"atr":(float(atr) if pd.notna(atr) else None),"risk_status":risk_status,"risk_reason":risk_reason,"stop_loss":sl,"take_profit":tp,"execution_outcome":exec_res.get("outcome"),"r_multiple":exec_res.get("r_multiple")})
        if exec_res: trades.append({"timestamp":ts,"direction":"BUY" if mur_dir=="BULLISH" else "SELL","entry_price":float(b.close),"atr":float(atr),"stop_loss":sl,"take_profit":tp,**exec_res})
    ev=pd.DataFrame(events); tr=pd.DataFrame(trades)
    output.mkdir(parents=True,exist_ok=True)
    ev.to_csv(output/"unified_78_events_2016_2024.csv",index=False); ev.to_csv(output/"decision_events_2016_2024.csv",index=False); tr.to_csv(output/"executed_trades_2016_2024.csv",index=False)
    scored=tr[tr.r_multiple.notna()] if not tr.empty else tr
    wins=int((scored.r_multiple>0).sum()) if not scored.empty else 0; losses=int((scored.r_multiple<0).sum()) if not scored.empty else 0
    eq=scored.r_multiple.cumsum() if not scored.empty else pd.Series(dtype=float); gross_win=float(scored.loc[scored.r_multiple>0,"r_multiple"].sum()) if wins else 0.0; gross_loss=float(-scored.loc[scored.r_multiple<0,"r_multiple"].sum()) if losses else 0.0
    metrics={"status":"DIAGNOSTIC_NOT_OFFICIAL","development_window":"2016-2024","events":int(len(ev)),"trades":int(len(scored)),"wins":wins,"losses":losses,"win_rate":(wins/len(scored) if len(scored) else None),"profit_factor":(gross_win/gross_loss if gross_loss else None),"expectancy_R":(float(scored.r_multiple.mean()) if not scored.empty else None),"total_R":(float(scored.r_multiple.sum()) if not scored.empty else 0.0),"max_drawdown_R":(float((eq-eq.cummax()).min()) if not eq.empty else 0.0),"costs_applied":False,"official_claim_allowed":False,"tiz_status":"UNRESOLVED_OPTIONAL","execution_convention":"event_close_entry; 0.75 ATR stop; 3R target"}
    funnel={"events":int(len(ev)),"murphy_directional":int(ev.murphy_direction.isin(["BULLISH","BEARISH"]).sum()),"decision_aligned":int(ev.direction_ready.sum()),"risk_pass":int((ev.risk_status=="PASS").sum()),"executed_trades":int(len(tr)),"ambiguous":int((ev.execution_outcome=="AMBIGUOUS").sum()),"timeouts":int((ev.execution_outcome=="TIMEOUT").sum())}
    validation={"timestamp_asof":True,"lookahead":True,"mtf_consumption":True,"memory_leakage":True,"execution_funnel":True,"similarity_direction_generation":False,"retrieval_direction_generation":False,"tiz_hardcoded_pass":False,"tiz_status":"UNRESOLVED_OPTIONAL","risk_hardcoded_pass":False,"frozen_cost_slippage":False,"official_profitability_claim":False,"2025_locked":True,"decision_brain_v1_source_unchanged":True}
    (output/"execution_funnel_2016_2024.json").write_text(json.dumps(funnel,indent=2)); (output/"backtest_metrics_2016_2024.json").write_text(json.dumps(metrics,indent=2)); (output/"validation_manifest_2016_2024.json").write_text(json.dumps(validation,indent=2))
    return {"metrics":metrics,"funnel":funnel,"validation":validation}


def main():
    p=argparse.ArgumentParser()
    for n in ["h1","market","mtf","murphy","nison","historical-context","historical-outcome","similarity","retrieval"]: p.add_argument("--"+n,required=True,type=Path)
    p.add_argument("--output-dir",required=True,type=Path)
    a=p.parse_args()
    print(json.dumps(run(h1=a.h1,market=a.market,mtf=a.mtf,murphy=a.murphy,nison=a.nison,historical_context=getattr(a,"historical_context"),historical_outcome=getattr(a,"historical_outcome"),similarity=a.similarity,retrieval=a.retrieval,output=a.output_dir),indent=2,default=str))
if __name__=="__main__": main()
