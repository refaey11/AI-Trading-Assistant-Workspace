#!/usr/bin/env python3
"""Build the Gate 3C input bundle for one timestamped event.

The Murphy fan-in is deliberately checked at this boundary. A partial fan-in
must never be represented as a successful Gate 3C event.
"""
from __future__ import annotations
import argparse, csv, json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
MURPHY_IDS=("MURPHY_0003","MURPHY_0004","MURPHY_0006","MURPHY_0007","MURPHY_0018","MURPHY_0019","MURPHY_0021","MURPHY_0022","MURPHY_0023","MURPHY_0025","MURPHY_0026","MURPHY_0028","MURPHY_0029","MURPHY_0030","MURPHY_0031","MURPHY_0032","MURPHY_0033","MURPHY_0034","MURPHY_0035","MURPHY_0036","MURPHY_0037","MURPHY_0038","MURPHY_0039","MURPHY_0040","MURPHY_0041","MURPHY_0042","MURPHY_0043","MURPHY_0044","MURPHY_0045","MURPHY_0047","MURPHY_0048","MURPHY_0049","MURPHY_0050","MURPHY_0051")
def murphy_coverage(rule_ids:Iterable[object])->dict[str,Any]:
 expected=set(MURPHY_IDS); observed={str(x) for x in rule_ids if x is not None}; missing=sorted(expected-observed); unknown=sorted(observed-expected); return {"rule_ids":sorted(observed&expected),"rule_count":len(observed&expected),"missing_rule_ids":missing,"unknown_rule_ids":unknown,"complete":not missing and not unknown}
def _utc_timestamp(value:str)->datetime:return datetime.fromisoformat(value.replace("Z","+00:00")).astimezone(timezone.utc)
def _read_murphy_rows(root:Path,target:datetime)->list[dict[str,str]]:
 rows=[]
 for path in sorted(root.rglob("*.csv")):
  with path.open(encoding="utf-8",newline="") as h:
   reader=csv.DictReader(h)
   if not reader.fieldnames: continue
   col="source_rule_id" if "source_rule_id" in reader.fieldnames else "rule_id"
   if col not in reader.fieldnames or "timestamp" not in reader.fieldnames: continue
   for row in reader:
    if row.get("timestamp") and _utc_timestamp(row["timestamp"])==target: rows.append({**row,"source_rule_id":str(row[col]),"source_path":str(path)})
 return rows
def build_bundle(timestamp:str,murphy_root:Path)->dict[str,Any]:
 target=_utc_timestamp(timestamp); rows=_read_murphy_rows(murphy_root,target); coverage=murphy_coverage(r["source_rule_id"] for r in rows)
 if not coverage["complete"]: raise RuntimeError("BLOCKED_MURPHY_34_INCOMPLETE")
 return {"timestamp":target.isoformat().replace("+00:00","Z"),"murphy":{"rows":rows,**coverage},"provenance":{"murphy_root":str(murphy_root),"murphy_row_count":len(rows),"missing_rule_ids":coverage["missing_rule_ids"],"unknown_rule_ids":coverage["unknown_rule_ids"],"complete":coverage["complete"]}}
def main()->None:
 p=argparse.ArgumentParser(); p.add_argument("--timestamp",required=True); p.add_argument("--murphy-root",required=True,type=Path); p.add_argument("--output",required=True,type=Path)
 for name in ("h1","market-state","nison","mtf-root","historical-context-root","historical-outcome-root","similarity-root","retrieval-root"): p.add_argument(f"--{name}")
 a=p.parse_args(); out=build_bundle(a.timestamp,a.murphy_root); a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
if __name__=="__main__": main()
