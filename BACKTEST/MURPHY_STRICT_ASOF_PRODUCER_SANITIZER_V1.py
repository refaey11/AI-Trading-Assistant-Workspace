"""Diagnostic-only strict-as-of producer sanitizer for Murphy 34 recovery."""
from __future__ import annotations
import csv,json,re
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path('artifacts/murphy_34_workspace_audit'); INPUT=ROOT/'MURPHY_PRODUCER_FAMILY_INVENTORY_V1.csv'; OUT=ROOT/'MURPHY_STRICT_ASOF_PRODUCER_SANITIZER_V1.json'
def norm(s): return re.sub(r'[^a-z0-9]+','_',s.lower()).strip('_')
def dt(s):
    if not s:return None
    try:
        x=datetime.fromisoformat(s.strip().replace('Z','+00:00'))
        return (x if x.tzinfo else x.replace(tzinfo=timezone.utc)).astimezone(timezone.utc)
    except:return None
def pick(r,*keys):
    m={norm(k):v for k,v in r.items()}
    for k in keys:
        if m.get(norm(k)) not in (None,''): return m[norm(k)]
    return ''
def main():
    rows=list(csv.DictReader(INPUT.open(newline='',encoding='utf-8-sig'))); counts={'rows':len(rows),'in_window':0,'passed_strict_asof':0,'reject_2025':0,'reject_equal_or_later':0,'missing_availability':0,'unverified':0}
    fam={}
    for r in rows:
        f=pick(r,'producer_family','family','producer_family_name') or 'UNKNOWN'; d=dt(pick(r,'decision_timestamp','bar_timestamp','signal_timestamp','event_timestamp')); a=dt(pick(r,'availability_timestamp','available_at','producer_availability_timestamp')); st='UNVERIFIED'; reason='missing_or_invalid_decision_timestamp'
        if d and datetime(2016,1,1,tzinfo=timezone.utc)<=d<datetime(2025,1,1,tzinfo=timezone.utc):
            counts['in_window']+=1
            if not a: counts['missing_availability']+=1; reason='missing_or_invalid_availability_timestamp'
            elif a>=datetime(2025,1,1,tzinfo=timezone.utc): counts['reject_2025']+=1; st='REJECT'; reason='availability_timestamp_in_2025'
            elif a>=d: counts['reject_equal_or_later']+=1; st='REJECT'; reason='availability_not_strictly_prior'
            else: counts['passed_strict_asof']+=1; st='PASS'; reason='strictly_prior'
        elif d: st='OUTSIDE_2016_2024'; reason='decision_timestamp_outside_locked_window'
        fam.setdefault(f,{'rows':0,'PASS':0,'REJECT':0,'UNVERIFIED':0,'OUTSIDE_2016_2024':0}); fam[f]['rows']+=1; fam[f][st]=fam[f].get(st,0)+1
    OUT.write_text(json.dumps({'policy':{'window':'2016-01-01 through 2024-12-31','strict_asof':'availability_timestamp < decision_timestamp','exclude_2025':True,'imputation':False},'counts':counts,'family_counts':fam},indent=2),encoding='utf-8'); print(json.dumps({'counts':counts,'family_counts':fam},indent=2))
if __name__=='__main__':main()
