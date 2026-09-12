#!/usr/bin/env python3
"""Strict audit-only scan for source-backed Murphy historical evidence.

Expected IDs are read from the frozen Decision Brain allowlist. A historical
reference is counted only when the ID occurs in a structured data file
(CSV/JSON/JSONL) located in an evidence/backtest/historical/data/development
path. Governance, runtime code, documentation, and this audit directory are
excluded to avoid false positives. This script never creates evidence.
"""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path

TEXT_EXT={'.csv','.json','.jsonl'}
EXCLUDE_PARTS={'.git','.venv','node_modules','__pycache__','.github','EDGE_DISCOVERY','governance'}
HIST_HINTS=('evidence','backtest','historical','history','data','development','dev_')
ID_RE=re.compile(r'MURPHY_(\d{4})')

def load_ids(path:Path):
    d=json.loads(path.read_text(encoding='utf-8'))
    if isinstance(d.get('content'),dict): d=d['content']
    ids=d.get('verified_runtime',{}).get('MURPHY',[])
    ids=sorted(set(ids))
    if len(ids)!=34: raise SystemExit(f'FAIL: expected 34 Murphy IDs, got {len(ids)}')
    return ids

def allowed_file(p:Path):
    if p.suffix.lower() not in TEXT_EXT: return False
    parts={x.lower() for x in p.parts}
    if parts & {x.lower() for x in EXCLUDE_PARTS}: return False
    s=str(p).lower()
    return any(h in s for h in HIST_HINTS)

def contains_id(p:Path, rid:str):
    try: raw=p.read_text(encoding='utf-8',errors='ignore')
    except Exception: return False
    if p.suffix.lower()=='.csv':
        try:
            rows=csv.reader(raw.splitlines())
            for row in rows:
                if rid in row or any(rid in cell for cell in row): return True
        except Exception: pass
    elif p.suffix.lower() in {'.json','.jsonl'}:
        return rid in raw
    return False

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',required=True); ap.add_argument('--allowlist',required=True); ap.add_argument('--out',required=True)
    a=ap.parse_args(); root=Path(a.root); ids=load_ids(root/a.allowlist)
    files=[p for p in root.rglob('*') if p.is_file() and allowed_file(p)]
    rows=[]
    for rid in ids:
        refs=sorted(str(p.relative_to(root)) for p in files if contains_id(p,rid))
        rows.append({'rule_id':rid,'status':'HISTORICAL_REFERENCED' if refs else 'NOT_EVALUABLE_CANDIDATE','historical_refs':refs,'historical_ref_count':len(refs)})
    hist=[r for r in rows if r['historical_ref_count']]
    out={'schema_version':'MURPHY_34_SOURCE_SCAN_V2','expected_count':34,'historical_referenced_count':len(hist),'not_evaluable_candidate_count':34-len(hist),'rows':rows,'governance':{'dev_window':'2016-2024','oos_locked':'2025','synthetic_evidence_allowed':False,'semantic_changes_allowed':False,'audit_only':True}}
    Path(a.out).write_text(json.dumps(out,indent=2,sort_keys=True),encoding='utf-8')
    print(json.dumps(out['governance']))
    for r in rows: print(r['rule_id'],r['status'],r['historical_ref_count'])
    print('SUMMARY',out['historical_referenced_count'],out['not_evaluable_candidate_count'])

if __name__=='__main__': main()
