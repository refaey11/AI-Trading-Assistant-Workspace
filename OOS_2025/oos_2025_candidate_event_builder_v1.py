#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import pandas as pd

CANDIDATES={
 'C1_HIGH_STRONG_BEARISH_MTF':lambda d:(d.volatility_state=='HIGH')&(d.mtf_context=='strong_bearish'),
 'C2_HIGH_H4_BEARISH':lambda d:(d.volatility_state=='HIGH')&(d.H4_trend_regime==-1),
 'C3_SELL_HIGH':lambda d:(d.direction=='SELL')&(d.volatility_state=='HIGH'),
}

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--murphy',required=True); ap.add_argument('--h1',required=True); ap.add_argument('--market-state',required=True); ap.add_argument('--mtf',required=True); ap.add_argument('--out-dir',required=True); a=ap.parse_args()
 out=Path(a.out_dir); out.mkdir(parents=True,exist_ok=True)
 mur=pd.read_csv(a.murphy,low_memory=False); h1=pd.read_csv(a.h1,low_memory=False); ms=pd.read_csv(a.market_state,low_memory=False); mtf=pd.read_csv(a.mtf,low_memory=False)
 for df,col in [(mur,'timestamp'),(h1,'timestamp'),(ms,'timestamp'),(mtf,'timestamp')]: df[col]=pd.to_datetime(df[col],utc=True,errors='coerce',format='mixed')
 if any(df.timestamp.isna().any() for df in [mur,h1,ms,mtf]): raise SystemExit('FAIL_CLOSED_INVALID_TIMESTAMP')
 if set(mur.timestamp.dt.year.astype(int))-{2025}: raise SystemExit('FAIL_CLOSED_MURPHY_NOT_2025_ONLY')
 mur['status']=mur.get('status','').astype(str).str.upper(); mur['direction']=mur.get('direction',mur.get('directional_confirmation','')).astype(str).str.upper()
 mur=mur[mur.status=='PASS'].copy()
 mur=mur[mur.direction.isin(['BUY','SELL','BULLISH','BEARISH'])].copy()
 mur['direction']=mur.direction.replace({'BULLISH':'BUY','BEARISH':'SELL'})
 # strict as-of: only completed context strictly before the Murphy event.
 ms=ms.sort_values('timestamp'); mtf=mtf.sort_values('timestamp'); mur=mur.sort_values('timestamp')
 if 'ATR20' not in ms.columns: raise SystemExit('FAIL_CLOSED_MARKET_STATE_MISSING_ATR20')
 if 'volatility_state' not in ms.columns: raise SystemExit('FAIL_CLOSED_MARKET_STATE_MISSING_VOLATILITY_STATE')
 ctxcols=[c for c in ['timestamp','ATR20','volatility_state','trend','location'] if c in ms.columns]
 x=pd.merge_asof(mur,ms[ctxcols].sort_values('timestamp'),on='timestamp',direction='backward',allow_exact_matches=False)
 mtfcols=[c for c in ['timestamp','mtf_context','H4_trend_regime','mtf_trend_score'] if c in mtf.columns]
 if set(['mtf_context','H4_trend_regime'])-set(mtf.columns): raise SystemExit('FAIL_CLOSED_MTF_REQUIRED_FIELDS')
 x=pd.merge_asof(x,mtf[mtfcols].sort_values('timestamp'),on='timestamp',direction='backward',allow_exact_matches=False)
 x['ATR20']=pd.to_numeric(x.ATR20,errors='coerce'); x=x.dropna(subset=['ATR20','volatility_state','mtf_context','H4_trend_regime']).copy()
 x['volatility_state']=x.volatility_state.astype(str).str.upper(); x['mtf_context']=x.mtf_context.astype(str).str.lower(); x['H4_trend_regime']=pd.to_numeric(x.H4_trend_regime,errors='coerce')
 # H1 execution: entry is next H1 open after the event; no same-bar fill.
 h1=h1.sort_values('timestamp').reset_index(drop=True)
 need={'open','high','low'}-set(h1.columns)
 if need: raise SystemExit(f'FAIL_CLOSED_H1_MISSING:{sorted(need)}')
 h1['open']=pd.to_numeric(h1.open,errors='coerce'); h1['high']=pd.to_numeric(h1.high,errors='coerce'); h1['low']=pd.to_numeric(h1.low,errors='coerce')
 ts=h1.timestamp.astype('int64').to_numpy()
 rows=[]
 for r in x.itertuples(index=False):
  j=int(pd.Series(ts).searchsorted(r.timestamp.value,side='right'))
  if j>=len(h1): continue
  entry=h1.iloc[j].open; atr=float(r.ATR20)
  if pd.isna(entry) or atr<=0: continue
  stop_dist=.75*atr; target_dist=2*stop_dist
  if r.direction=='BUY': sl=entry-stop_dist; tp=entry+target_dist
  else: sl=entry+stop_dist; tp=entry-target_dist
  result=None; exit_time=None; net=None
  for k in range(j,len(h1)):
   b=h1.iloc[k]; hi,lo=float(b.high),float(b.low)
   hit_sl=(lo<=sl) if r.direction=='BUY' else (hi>=sl)
   hit_tp=(hi>=tp) if r.direction=='BUY' else (lo<=tp)
   if hit_sl and hit_tp: result='AMBIGUOUS'; exit_time=b.timestamp; net=None; break
   if hit_tp: result='TP'; exit_time=b.timestamp; net=2.0; break
   if hit_sl: result='SL'; exit_time=b.timestamp; net=-1.0; break
  rows.append({'event_time':r.timestamp,'direction':r.direction,'source_rule_id':getattr(r,'source_rule_id',''),'volatility_state':r.volatility_state,'mtf_context':r.mtf_context,'H4_trend_regime':r.H4_trend_regime,'entry_time':h1.iloc[j].timestamp,'entry_price':entry,'ATR20_asof':atr,'exit_time':exit_time,'outcome':result or 'OPEN','net_R':net})
 ev=pd.DataFrame(rows)
 if ev.empty: raise SystemExit('FAIL_CLOSED_NO_2025_EVENTS_AFTER_ASOF_EXECUTION_GATES')
 ev['event_time']=pd.to_datetime(ev.event_time,utc=True); assert set(ev.event_time.dt.year)=={2025}
 ev.to_csv(out/'oos_2025_candidate_events.csv',index=False)
 stats=[]
 for cid,fn in CANDIDATES.items():
  g=ev[fn(ev)].copy(); r=pd.to_numeric(g.net_R,errors='coerce').dropna(); wins=r[r>0].sum(); losses=-r[r<0].sum();
  stats.append({'candidate_id':cid,'events':len(g),'evaluated':len(r),'TP':int((g.outcome=='TP').sum()),'SL':int((g.outcome=='SL').sum()),'ambiguous':int((g.outcome=='AMBIGUOUS').sum()),'open':int((g.outcome=='OPEN').sum()),'win_rate':float((r>0).mean()) if len(r) else None,'expectancy_R':float(r.mean()) if len(r) else None,'profit_factor':float(wins/losses) if losses else None,'total_net_R':float(r.sum()) if len(r) else 0.0})
 pd.DataFrame(stats).to_csv(out/'oos_2025_candidate_results.csv',index=False)
 manifest={'status':'OOS_2025_EVALUATION_ONLY','window':'2025-only','candidate_set_frozen':True,'tuning_applied':False,'threshold_sweep':False,'future_data_used':False,'strict_asof_context':True,'entry_next_h1_open':True,'stop_atr':0.75,'target_R':2.0,'official_profitability_claim_allowed':False,'canonical_three_book_mode':False,'note':'Evaluation-only candidate evidence; not canonical Decision Brain profitability.'}
 (out/'oos_2025_candidate_manifest.json').write_text(json.dumps(manifest,indent=2))
 print(pd.DataFrame(stats).to_string(index=False)); print(json.dumps(manifest,indent=2))
if __name__=='__main__': main()
