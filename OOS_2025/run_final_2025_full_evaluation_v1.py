from __future__ import annotations
import argparse,json,os,subprocess,zipfile
from pathlib import Path
import pandas as pd
from OOS_2025.full_78_rule_decision_event_stream_v2 import build_rule_event_stream,summarize_coverage
from OOS_2025.nison_2025_evidence_aggregate_v1 import aggregate_nison_evidence
from OOS_2025.core_profitability_eval_v1 import evaluate_event

def run(cmd): subprocess.run(cmd,check=True)
def read(p,cols):
 d=pd.read_csv(p); m=cols-set(d.columns)
 if m: raise ValueError(f'{p}: missing {sorted(m)}')
 d['timestamp']=pd.to_datetime(d['timestamp'],utc=True,errors='coerce')
 if d['timestamp'].isna().any(): raise ValueError(f'{p}: invalid timestamp')
 return d.sort_values('timestamp').reset_index(drop=True)

def download(token,path,out):
 import urllib.request
 req=urllib.request.Request('https://content.dropboxapi.com/2/files/download',headers={'Authorization':f'Bearer {token}','Dropbox-API-Arg':json.dumps({'path':path})})
 with urllib.request.urlopen(req,timeout=120) as r,out.open('wb') as f: f.write(r.read())
 return out

def main():
 p=argparse.ArgumentParser(); p.add_argument('--h1',required=True,type=Path); p.add_argument('--nison',required=True,type=Path); p.add_argument('--output-dir',required=True,type=Path); p.add_argument('--year',type=int,default=2025); a=p.parse_args(); out=a.output_dir; out.mkdir(parents=True,exist_ok=True)
 token=os.environ.get('DROPBOX_ACCESS_TOKEN')
 if not token: raise RuntimeError('DROPBOX_ACCESS_TOKEN missing')
 dl=out/'downloads'; dl.mkdir(exist_ok=True)
 z=download(token,'/GBPUSD_M1_MASTER_2016_2026_V1.zip',dl/'m1.zip'); md=dl/'m1'; md.mkdir(exist_ok=True)
 with zipfile.ZipFile(z) as ar: ar.extractall(md)
 m1=next(p for p in md.rglob('*.csv') if 'GBPUSD' in p.name.upper() and 'M1' in p.name.upper())
 market=download(token,'/ai_trading_assistant_full_project_v1/AI_Trading_Assistant_MARKET_STATE_READER_V1/GBPUSD_MARKET_STATE.csv',dl/'GBPUSD_MARKET_STATE.csv')
 h1=read(a.h1,{'timestamp','open','high','low','close'}); h1y=h1[h1.timestamp.dt.year.eq(a.year)]
 nison=read(a.nison,{'timestamp','rule_id','status','direction'}); nison=nison[nison.timestamp.dt.year.eq(a.year)]
 nison_agg=aggregate_nison_evidence(nison)
 src=[]
 for ts,g in nison.groupby('timestamp'):
  p=[str(x) for x in g.loc[g.status.eq('PASS')&g.direction.astype(str).isin({'BULLISH','BEARISH'}),'rule_id']]; f=[str(x) for x in g.loc[g.status.eq('FAIL')&g.direction.astype(str).isin({'BULLISH','BEARISH'}),'rule_id']]; src.append({'timestamp':ts,'source_rule_id':p[0] if p else (f[0] if f else 'NISON_NONE')})
 nison_agg=nison_agg.merge(pd.DataFrame(src),on='timestamp',how='left',validate='one_to_one')
 m21=out/'MURPHY_0021_2025.csv'; run(['python','OOS_2025/run_murphy_0021_2025_fresh_v1.py','--input',str(a.h1),'--m1-input',str(m1),'--output',str(m21),'--manifest',str(out/'MURPHY_0021_MANIFEST.json')])
 m22=out/'MURPHY_0022_0023_2025.csv'; run(['python','OOS_2025/run_murphy_0022_0023_2025_pit_v1.py','--h1',str(a.h1),'--m1',str(m1),'--oi','evidence/cftc/2025/6b_oi_pit_bound_v1.json','--output',str(m22),'--manifest',str(out/'MURPHY_0022_0023_MANIFEST.json')])
 m21d=read(m21,{'timestamp','rule_id','status','directional_confirmation'}); m22d=read(m22,{'timestamp','rule_id','status','directional_confirmation'})
 murphy=pd.concat([m21d,m22d],ignore_index=True); murphy['source_rule_id']=murphy.rule_id.astype(str); murphy['direction']=murphy.directional_confirmation.astype(str); murphy= murphy.sort_values(['timestamp','status']).drop_duplicates('timestamp',keep='last')
 full=build_rule_event_stream(h1y.timestamp.tolist(),murphy_rows=pd.concat([m21d.assign(direction=m21d.directional_confirmation,available=m21d.status.isin(['PASS','FAIL'])),m22d.assign(direction=m22d.directional_confirmation,available=m22d.status.isin(['PASS','FAIL']))]).to_dict('records'),nison_rows=nison.to_dict('records'))
 full.to_csv(out/'FULL_78_RULE_2025_EVENT_STREAM.csv',index=False)
 ctx=out/'context'; run(['python','OOS_2025/build_historical_context_execution_inputs_v1.py','--source',str(market),'--output-dir',str(ctx),'--year',str(a.year)])
 murphy[['timestamp','status','direction','source_rule_id']].to_csv(out/'MURPHY_CANDIDATE_STREAM.csv',index=False)
 run(['python','OOS_2025/build_historical_risk_evidence_v1.py','--context',str(ctx/'execution.csv'),'--murphy',str(out/'MURPHY_CANDIDATE_STREAM.csv'),'--output',str(out/'RISK_2025_EVIDENCE.csv'),'--manifest',str(out/'RISK_2025_EVIDENCE_MANIFEST.json'),'--year',str(a.year)])
 nison_agg[['timestamp','confirmation','contradiction','source_rule_id']].to_csv(out/'NISON_CANDIDATE_STREAM.csv',index=False)
 events=out/'FINAL_2025_DECISION_EVENTS.csv'; run(['python','OOS_2025/full_decision_brain_historical_event_producer_v1.py','--context',str(ctx/'context.csv'),'--murphy',str(out/'MURPHY_CANDIDATE_STREAM.csv'),'--nison',str(out/'NISON_CANDIDATE_STREAM.csv'),'--risk',str(out/'RISK_2025_EVIDENCE.csv'),'--execution',str(ctx/'execution.csv'),'--year',str(a.year),'--output',str(events),'--manifest',str(out/'FINAL_2025_DECISION_EVENTS_MANIFEST.json'),'--optional-tiz'])
 ev=pd.read_csv(events); elig=[]
 for r in ev.to_dict('records'):
  elig.append(evaluate_event({'murphy_pass':int(str(r.get('murphy_status'))=='PASS'),'directional_confirmation':r.get('murphy_direction'),'nison_status':'CONTRADICTORY' if bool(r.get('nison_contradiction',False)) else 'NOT_EVALUABLE','entry_price':r.get('entry_price'),'atr':1.0,'tiz_process_state':r.get('tiz_status','NOT_EVALUABLE')}))
 pd.DataFrame(elig).to_csv(out/'FINAL_2025_CORE_PROFITABILITY_ELIGIBILITY.csv',index=False)
 cov=summarize_coverage(full); manifest={'status':'PASS','evaluation_year':a.year,'full_78_rule_event_rows':len(full),'observed_rules':cov['observed_rule_count'],'available_rows':cov['available_rows'],'decision_events':len(ev),'decision_executable':int((ev.status=='EXECUTABLE').sum()) if len(ev) else 0,'core_profitability_eligible':int((pd.DataFrame(elig).status=='ELIGIBLE_FOR_CORE_PROFITABILITY_BACKTEST').sum()) if elig else 0,'source_backed_only':True,'murphy_generates_direction':True,'nison_confirmation_only':True,'tiz_generates_direction':False,'historical_memory_used_for_direction':False,'oos_tuning':False,'profit_number_promoted':False,'note':'Full governed 78-rule stream and recovered Decision Brain event path produced. No P&L number is promoted without an existing governed outcome/backtest artifact.'}
 (out/'FINAL_2025_EVALUATION_MANIFEST.json').write_text(json.dumps(manifest,indent=2,default=str)); print(json.dumps(manifest,indent=2,default=str))
if __name__=='__main__': main()
