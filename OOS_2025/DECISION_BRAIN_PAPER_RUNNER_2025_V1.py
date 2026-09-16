from __future__ import annotations
import argparse, importlib.util, json, re
from pathlib import Path
from typing import Any
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ALLOWLIST = ROOT / "governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json"
BRAIN_PATH = ROOT / "RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py"
STOP_ATR = 0.75
TARGET_R = 2.0
MAX_BARS = 48


def load_csv(path: Path, required: set[str], dup=False) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"{path}: missing columns {missing}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce", format="mixed")
    if df.timestamp.isna().any():
        raise ValueError(f"{path}: invalid timestamps")
    if not dup and df.timestamp.duplicated().any():
        raise ValueError(f"{path}: duplicate timestamps")
    return df.sort_values("timestamp").reset_index(drop=True)


def norm(v: Any) -> str | None:
    t = str(v or "").strip().upper()
    return {"BUY":"BULLISH","BULL":"BULLISH","BULLISH":"BULLISH","SELL":"BEARISH","BEAR":"BEARISH","BEARISH":"BEARISH"}.get(t)


def _num(v: Any) -> float | None:
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    try:
        return float(v)
    except Exception:
        d = norm(v)
        if d == "BULLISH": return 1.0
        if d == "BEARISH": return -1.0
        return None


def _canon(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


def _resolve_col(columns, aliases):
    exact = {_canon(c): c for c in columns}
    for a in aliases:
        if _canon(a) in exact:
            return exact[_canon(a)]
    return None


def _resolve_timeframe_col(columns, tf, kind):
    aliases = [
        f"{tf}_{kind}_regime", f"{tf}_{kind}", f"{kind}_regime_{tf}",
        f"{kind}_{tf}_regime", f"{kind}_{tf}", f"{tf}_regime_{kind}", f"{tf}_{kind}state"
    ]
    hit = _resolve_col(columns, aliases)
    if hit:
        return hit
    tfc, kc = _canon(tf), _canon(kind)
    candidates = []
    for c in columns:
        cc = _canon(c)
        if tfc in cc and kc in cc and ("regime" in cc or kind == "trend"):
            candidates.append(c)
    return sorted(candidates, key=lambda x: ("regime" not in _canon(x), len(str(x))))[0] if candidates else None


def brain_row(r: pd.Series) -> tuple[dict[str,Any], dict[str,str]]:
    """Resolve the recovered Brain's canonical inputs from the actual source schema.
    No 2025 values are inferred from outcomes or tuned; only deterministic field aliases
    and explicit bullish/bearish text-to-number normalization are used.
    """
    cols=list(r.index)
    out={
        "mtf_trend_score":0.0,
        "M5_trend_regime":0.0,"M15_trend_regime":0.0,"M30_trend_regime":0.0,
        "H1_trend_regime":0.0,"H4_trend_regime":0.0,"D1_trend_regime":0.0,
        "volume_available":False,
        "M5_volume_regime":0.0,"M15_volume_regime":0.0,"M30_volume_regime":0.0,
        "H1_volume_regime":0.0,"H4_volume_regime":0.0,"D1_volume_regime":0.0,
    }
    mapping={}
    score_col=_resolve_col(cols,["mtf_trend_score","mtf_score","multi_timeframe_trend_score","multi_tf_trend_score"])
    if score_col and pd.notna(r[score_col]):
        v=_num(r[score_col])
        if v is not None: out["mtf_trend_score"]=v; mapping["mtf_trend_score"]=score_col
    for tf in ["M5","M15","M30","H1","H4","D1"]:
        tc=_resolve_timeframe_col(cols,tf,"trend")
        if tc and pd.notna(r[tc]):
            v=_num(r[tc])
            if v is not None:
                out[f"{tf}_trend_regime"]=v; mapping[f"{tf}_trend_regime"]=tc
        vc=_resolve_timeframe_col(cols,tf,"volume")
        if vc and pd.notna(r[vc]):
            v=_num(r[vc])
            if v is not None:
                out[f"{tf}_volume_regime"]=v; mapping[f"{tf}_volume_regime"]=vc
    va=_resolve_col(cols,["volume_available","has_volume","volume_data_available"])
    if va and pd.notna(r[va]):
        out["volume_available"]=bool(r[va]); mapping["volume_available"]=va
    elif any(k.endswith("_volume_regime") for k in mapping):
        out["volume_available"]=True
    return out,mapping


def aggregate_murphy(df: pd.DataFrame) -> pd.DataFrame:
    rows=[]
    for ts,g in df.groupby("timestamp",sort=True):
        p=g[g.status.astype(str).str.upper().eq("PASS")]
        dirs=sorted({d for d in (norm(x) for x in p.direction) if d})
        ids=set()
        if "source_rule_id" in g:
            for v in g.source_rule_id.dropna():
                ids |= {x.strip() for x in str(v).split("|") if x.strip()}
        direction=dirs[0] if len(dirs)==1 else ("CONFLICTED" if len(dirs)>1 else "ABSENT")
        rows.append({"timestamp":ts,"murphy_direction":direction,"source_rule_ids":json.dumps(sorted(ids))})
    return pd.DataFrame(rows)


def aggregate_nison(df: pd.DataFrame) -> pd.DataFrame:
    rows=[]
    for ts,g in df.groupby("timestamp",sort=True):
        p=g[g.status.astype(str).str.upper().eq("PASS")]
        dirs=sorted({d for d in (norm(x) for x in p.direction) if d})
        confirmation=dirs[0] if len(dirs)==1 else ("CONFLICTED" if len(dirs)>1 else "ABSENT")
        rows.append({"timestamp":ts,"nison_confirmation":confirmation,"nison_passed_directions":json.dumps(dirs)})
    return pd.DataFrame(rows)


def brain_module():
    spec=importlib.util.spec_from_file_location("recovered_decision_brain",BRAIN_PATH)
    if not spec or not spec.loader:
        raise RuntimeError("Unable to load recovered Decision Brain V1")
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def simulate(bars, entry_i, side, entry, atr):
    risk=STOP_ATR*atr
    sl=entry-risk if side=="BUY" else entry+risk
    tp=entry+TARGET_R*risk if side=="BUY" else entry-TARGET_R*risk
    end=min(len(bars),entry_i+1+MAX_BARS)
    for j in range(entry_i+1,end):
        b=bars.iloc[j]
        hit_sl=float(b.low)<=sl if side=="BUY" else float(b.high)>=sl
        hit_tp=float(b.high)>=tp if side=="BUY" else float(b.low)<=tp
        if hit_sl and hit_tp:
            return {"outcome":"AMBIGUOUS","r_multiple":None,"exit_timestamp":b.timestamp,"stop_loss":sl,"take_profit":tp}
        if hit_tp:
            return {"outcome":"TP","r_multiple":TARGET_R,"exit_timestamp":b.timestamp,"stop_loss":sl,"take_profit":tp}
        if hit_sl:
            return {"outcome":"SL","r_multiple":-1.0,"exit_timestamp":b.timestamp,"stop_loss":sl,"take_profit":tp}
    return {"outcome":"TIMEOUT","r_multiple":None,"exit_timestamp":bars.iloc[end-1].timestamp if end>entry_i+1 else None,"stop_loss":sl,"take_profit":tp}


def run(h1:Path,murphy:Path,nison:Path,context:Path,out:Path)->dict:
    bars=load_csv(h1,{"timestamp","open","high","low","close"})
    m=load_csv(murphy,{"timestamp","status","direction"},True)
    n=load_csv(nison,{"timestamp","status","direction","rule_id"},True)
    c=load_csv(context,{"timestamp"})
    if "entry_price" not in c.columns:
        if "close" not in c.columns: raise ValueError("context missing entry_price/close")
        c["entry_price"]=c["close"]
    if "atr" not in c.columns:
        if "atr20" not in c.columns: raise ValueError("context missing atr/atr20")
        c["atr"]=c["atr20"]
    c=c[c.timestamp.dt.year==2025].copy()
    merged=c.merge(aggregate_murphy(m),on="timestamp",how="left").merge(aggregate_nison(n),on="timestamp",how="left")
    brain=brain_module(); events=[]; trades=[]; mapping_counts={}
    for _,r in merged.iterrows():
        md=norm(r.get("murphy_direction"))
        nd=r.get("nison_confirmation")
        passed=json.loads(r.get("nison_passed_directions") or "[]")
        contradiction=bool(md in {"BULLISH","BEARISH"} and any(x in {"BULLISH","BEARISH"} and x!=md for x in passed))
        brow,bmap=brain_row(r)
        for k,v in bmap.items(): mapping_counts[k]=mapping_counts.get(k,0)+1
        a=brain.assess(brow,similarity=None)
        raw_bias=a.directional_bias
        bias=norm(raw_bias)
        executable=(md in {"BULLISH","BEARISH"} and bias==md and not contradiction and pd.notna(r.entry_price) and pd.notna(r.atr) and float(r.atr)>0)
        events.append({"timestamp":r.timestamp,"murphy_direction":md,"nison_confirmation":nd,"nison_contradiction":contradiction,"brain_bias":bias,"brain_bias_raw":raw_bias,"brain_confidence":a.confidence,"decision":"EXECUTE" if executable else "NO_TRADE","source_rule_ids":r.get("source_rule_ids","[]")})
        if not executable: continue
        pos=bars.index[bars.timestamp.eq(r.timestamp)]
        if len(pos)==0 or int(pos[0])+1>=len(bars): continue
        i=int(pos[0])+1
        entry=float(bars.iloc[i].open)
        side="BUY" if md=="BULLISH" else "SELL"
        result=simulate(bars,i,side,entry,float(r.atr))
        trades.append({"signal_timestamp":r.timestamp,"entry_timestamp":bars.iloc[i].timestamp,"direction":side,"entry_price":entry,"atr":float(r.atr),**result})
    out.mkdir(parents=True,exist_ok=True)
    ev=pd.DataFrame(events)
    tr=pd.DataFrame(trades)
    ev.to_csv(out/"decision_events_2025.csv",index=False)
    tr.to_csv(out/"paper_trades_2025.csv",index=False)
    resolved=tr[tr.r_multiple.notna()] if not tr.empty else tr
    wins=int((resolved.r_multiple>0).sum()) if not resolved.empty else 0
    losses=int((resolved.r_multiple<0).sum()) if not resolved.empty else 0
    gw=float(resolved.loc[resolved.r_multiple>0,"r_multiple"].sum()) if not resolved.empty else 0
    gl=float(-resolved.loc[resolved.r_multiple<0,"r_multiple"].sum()) if not resolved.empty else 0
    eq=resolved.r_multiple.cumsum() if not resolved.empty else pd.Series(dtype=float)
    trend_mapped_rows=int(ev.shape[0]) if all(k in mapping_counts for k in ["M5_trend_regime","M15_trend_regime","M30_trend_regime","H1_trend_regime","H4_trend_regime","D1_trend_regime"]) else 0
    metrics={"status":"EVALUATION_ONLY","window":"2025-only","events":len(ev),"murphy_directional":int(ev.murphy_direction.isin(["BULLISH","BEARISH"]).sum()),"brain_directional":int(ev.brain_bias.isin(["BULLISH","BEARISH"]).sum()),"decision_aligned":int(((ev.murphy_direction==ev.brain_bias)&ev.murphy_direction.isin(["BULLISH","BEARISH"])).sum()),"nison_contradictions":int(ev.nison_contradiction.sum()),"executed":len(tr),"resolved":len(resolved),"wins":wins,"losses":losses,"win_rate":wins/len(resolved) if len(resolved) else None,"profit_factor":gw/gl if gl else None,"expectancy_R":float(resolved.r_multiple.mean()) if len(resolved) else None,"total_R":float(resolved.r_multiple.sum()) if len(resolved) else 0.0,"max_drawdown_R":float((eq-eq.cummax()).min()) if not eq.empty else 0.0,"stop_atr":STOP_ATR,"target_R":TARGET_R,"entry_policy":"next_h1_open","nison_absent_is_allowed":True,"nison_fail_is_not_contradiction":True,"future_data_used":False,"tuning_applied":False,"live_execution":False,"official_profitability_claim":False,"brain_input_mapping_counts":mapping_counts,"all_six_trend_regimes_mapped":bool(trend_mapped_rows)}
    (out/"metrics_2025.json").write_text(json.dumps(metrics,indent=2))
    return metrics


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--h1",type=Path,required=True)
    p.add_argument("--murphy",type=Path,required=True)
    p.add_argument("--nison",type=Path,required=True)
    p.add_argument("--context",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    print(json.dumps(run(a.h1,a.murphy,a.nison,a.context,a.out),indent=2))
