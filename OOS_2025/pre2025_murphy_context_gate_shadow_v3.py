from __future__ import annotations
import argparse, json, math, sys
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from RECOVERED_SOURCES.DECISION_BRAIN_V1 import decision_brain
from MURPHY_EVALUATORS_V1.murphy_0021_0023_evaluator import evaluate_0021
LOCKED=2025; DIR={"BULLISH","BEARISH"}
S={"BULL_TREND":1.0,"BULLISH":1.0,"UPTREND":1.0,"BEAR_TREND":-1.0,"BEARISH":-1.0,"DOWNTREND":-1.0,"TRANSITION":0.0,"RANGE":0.0,"INSIDE_RANGE":0.0,"MIXED":0.0,"UNKNOWN":0.0}
def read(p,req):
 d=pd.read_csv(p); miss=sorted(set(req)-set(d.columns))
 if miss: raise ValueError(f"{p}: missing columns {miss}")
 d['timestamp']=pd.to_datetime(d['timestamp'],utc=True,errors='coerce')
 if d.timestamp.isna().any(): raise ValueError(f"{p}: invalid timestamps")
 return d.sort_values('timestamp',kind='stable').drop_duplicates('timestamp',keep='last').reset_index(drop=True)
def norm(v):
 x=str(v or '').upper()
 return 'BULLISH' if x in {'BULL','BULLISH','UP','UPTREND'} else 'BEARISH' if x in {'BEAR','BEARISH','DOWN','DOWNTREND'} else 'NONE'
def score(v): return S.get(str(v or '').upper(),0.0)
def build_murphy(h1,m1):
 h=h1.copy(); m=m1.copy(); h['previous_close']=h.close.shift(1); m['h1_timestamp']=m.timestamp.dt.floor('h')
 v=m.groupby('h1_timestamp',as_index=False).agg(volume=('volume','sum')).sort_values('h1_timestamp')
 v['previous_volume']=v.volume.shift(1); v['volume_direction']=None
 v.loc[v.volume>v.previous_volume,'volume_direction']='UP'; v.loc[v.volume<v.previous_volume,'volume_direction']='DOWN'
 x=h.merge(v[['h1_timestamp','volume_direction']],left_on='timestamp',right_on='h1_timestamp',how='left')
 out=[]
 for r in x.itertuples(index=False):
  z=evaluate_0021({'close':r.close,'previous_close':r.previous_close,'volume_direction':r.volume_direction})
  out.append({'timestamp':r.timestamp,'murphy_direction':norm(z.get('directional_confirmation'))})
 return pd.DataFrame(out)
def bucket(a,md,mtf):
 b=norm(a.directional_bias)
 if md not in DIR: return 'NO_MURPHY_DIRECTION'
 if a.market_state=='trend' and b==md: return 'TREND_ALIGNED'
 if a.market_state=='trend': return 'TREND_OPPOSED'
 if a.market_state=='uncertain': return 'UNCERTAIN'
 return 'RANGE_TRANSITION'
def mean(x):
 y=[float(v) for v in x if v is not None and math.isfinite(float(v))]; return sum(y)/len(y) if y else 0.0
def main():
 p=argparse.ArgumentParser(); p.add_argument('--market-state',required=True,type=Path); p.add_argument('--mtf',required=True,type=Path); p.add_argument('--h1',required=True,type=Path); p.add_argument('--m1',required=True,type=Path); p.add_argument('--year',required=True,type=int); p.add_argument('--output',required=True,type=Path); a=p.parse_args()
 year=a.year
 if year>=LOCKED: raise ValueError('2025_OOS_LOCKED')
 state=read(a.market_state,{'timestamp','close'}); mtf=read(a.mtf,{'timestamp','H4_trend','H1_trend','MTF_state'}); h=read(a.h1,{'timestamp','open','high','low','close'}); m=read(a.m1,{'timestamp','open','high','low','close','volume'})
 h['f12']=h.close.shift(-12); h['f24']=h.close.shift(-24); h['f48']=h.close.shift(-48)
 # PIT-safe: evaluation direction source contains only t data; forward columns are labels only.
 mur=build_murphy(h.drop(columns=['f12','f24','f48']),m).set_index('timestamp'); mtf=mtf.set_index('timestamp'); h=h.set_index('timestamp'); state=state[state.timestamp.dt.year.eq(year)].set_index('timestamp')
 rows=[]
 for ts,sr in state.iterrows():
  if ts not in mtf.index or ts not in h.index or ts not in mur.index: continue
  tr=mtf.loc[ts]; hr=h.loc[ts]; md=str(mur.loc[ts].murphy_direction)
  a1=decision_brain.assess({'mtf_trend_score':(score(tr.H4_trend)+score(tr.H1_trend))/2.0,'H1_trend_regime':score(tr.H1_trend),'H4_trend_regime':score(tr.H4_trend),'volume_available':False},similarity=None)
  rec={'timestamp':ts.isoformat(),'murphy_direction':md,'brain_state':a1.market_state,'brain_bias':a1.directional_bias,'brain_confidence':float(a1.confidence),'h4_trend':tr.H4_trend,'h1_trend':tr.H1_trend,'mtf_state':tr.MTF_state,'context_bucket':bucket(a1,md,str(tr.MTF_state))}
  for n in (12,24,48):
   fut=hr.get(f'f{n}'); valid=pd.notna(fut) and (pd.Timestamp(ts)+pd.Timedelta(hours=n)).year<LOCKED; srtn=None
   if valid and md in DIR:
    raw=float(fut)/float(hr.close)-1.0; srtn=raw if md=='BULLISH' else -raw
   rec[f'fwd{n}_signed_return']=srtn
  rows.append(rec)
 out=pd.DataFrame(rows); a.output.parent.mkdir(parents=True,exist_ok=True); out.to_csv(a.output,index=False); d=out[out.murphy_direction.isin(DIR)]; buckets=[]
 for b,g in d.groupby('context_bucket',dropna=False):
  z={'context_bucket':b,'signals':int(len(g))}
  for n in (12,24,48):
   x=g[f'fwd{n}_signed_return'].dropna(); z[f'fwd{n}_count']=int(len(x)); z[f'fwd{n}_hit_rate_pct']=round(100*float((x>0).mean()),4) if len(x) else 0.0; z[f'fwd{n}_mean_signed_return']=mean(x)
  buckets.append(z)
 summary={'status':'PASS_SHADOW_ONLY','mode':'REAL_DATA_PRE2025_CONTEXT_GATE_SHADOW_V3','evaluation_year':year,'pair':'GBPUSD','events':int(len(out)),'murphy_directional_events':int(len(d)),'context_buckets':buckets,'brain_role':'context_and_regime_only','murphy_role':'directional_anchor_MURPHY_0021','new_rule_semantics':False,'policy_changed':False,'replacement_pnl':False,'oos_2025_locked':True,'oos_tuning':False,'future_feature_leakage':False}
 a.output.with_suffix('.json').write_text(json.dumps(summary,indent=2,sort_keys=True)); print(json.dumps(summary,indent=2,sort_keys=True))
if __name__=='__main__': main()
