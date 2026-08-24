from __future__ import annotations
import argparse,json,subprocess
from pathlib import Path
import pandas as pd
NISON_RULES=[f'NISON_{i:04d}' for i in range(1,45)]
MURPHY_RULES=['MURPHY_0003','MURPHY_0004','MURPHY_0006','MURPHY_0007','MURPHY_0018','MURPHY_0019','MURPHY_0021','MURPHY_0022','MURPHY_0023','MURPHY_0025','MURPHY_0026','MURPHY_0028','MURPHY_0029','MURPHY_0030','MURPHY_0031','MURPHY_0032','MURPHY_0033','MURPHY_0034','MURPHY_0035','MURPHY_0036','MURPHY_0037','MURPHY_0038','MURPHY_0039','MURPHY_0040','MURPHY_0041','MURPHY_0042','MURPHY_0043','MURPHY_0044','MURPHY_0045','MURPHY_0047','MURPHY_0048','MURPHY_0049','MURPHY_0050','MURPHY_0051']
def build_coverage(nison_csv,murphy_snapshot_json,output_json):
 n=pd.read_csv(nison_csv); n['timestamp']=pd.to_datetime(n['timestamp'],utc=True); rows=[]
 for rid in NISON_RULES:
  s=n[n['rule_id'].astype(str).eq(rid)]; c=s['status'].astype(str).value_counts(); a=int(s['available'].fillna(False).astype(bool).sum()) if 'available' in s.columns else int(c.get('PASS',0)+c.get('FAIL',0)); rows.append({'family':'NISON','rule_id':rid,'rows':int(len(s)),'available_rows':a,'available_rate':a/len(s) if len(s) else 0.0,'pass_rows':int(c.get('PASS',0)),'fail_rows':int(c.get('FAIL',0)),'not_evaluable_rows':int(c.get('NOT_EVALUABLE',0)),'coverage_status':'OBSERVED_2025_OUTPUT' if len(s) else 'NO_2025_OUTPUT'})
 m=json.loads(Path(murphy_snapshot_json).read_text()); ms=pd.DataFrame(m['rules']); ms['family']='MURPHY'; rows.extend(ms[['family','rule_id','rows','available_rows','available_rate','pass_rows','fail_rows','not_evaluable_rows','coverage_status']].to_dict('records'))
 out={'status':'OOS_COVERAGE_ONLY','rule_count':len(rows),'murphy_rules':len(MURPHY_RULES),'nison_rules':len(NISON_RULES),'observed_rules':sum(x['rows']>0 for x in rows),'rules_with_available_evidence':sum(x['available_rows']>0 for x in rows),'rules_with_full_available_rate':sum(x['available_rate']>=1 for x in rows),'no_2025_output_rules':sum(x['rows']==0 for x in rows),'rules':rows,'notes':['Murphy snapshot is reporting-only and is not used as fresh final evidence.','Missing evidence remains NOT_EVALUABLE.']}; Path(output_json).write_text(json.dumps(out,indent=2),encoding='utf-8')
def main():
 p=argparse.ArgumentParser(); p.add_argument('--nison-csv',required=True); p.add_argument('--murphy-snapshot',required=True); p.add_argument('--output',required=True); a=p.parse_args(); build_coverage(a.nison_csv,a.murphy_snapshot,a.output)
 h1=next(Path('/tmp').rglob('GBPUSD_H1_2016_2025_MASTER.csv'),None)
 if h1 is None: raise SystemExit('FINAL_EVAL_BLOCKED: H1 source not found in CI workspace')
 subprocess.run(['python','OOS_2025/run_final_2025_full_evaluation_v1.py','--h1',str(h1),'--nison',a.nison_csv,'--output-dir','artifacts/final_2025_evaluation','--year','2025'],check=True)
if __name__=='__main__': main()
