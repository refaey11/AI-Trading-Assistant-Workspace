from __future__ import annotations
from typing import Dict, Any

def _eval(rule_id, row, sign, label):
    c=row.get('converging'); us=row.get('upper_slope'); ls=row.get('lower_slope')
    if c is None or us is None or ls is None:
        return {'rule_id':rule_id,'status':'NOT_EVALUABLE','directional_confirmation':'UNKNOWN','reason':'Missing derived convergence or slope evidence.'}
    if not isinstance(c,bool):
        return {'rule_id':rule_id,'status':'NOT_EVALUABLE','directional_confirmation':'UNKNOWN','reason':'Convergence evidence is invalid.'}
    ok=c and (us < 0 and ls < 0 if sign < 0 else us > 0 and ls > 0)
    return {'rule_id':rule_id,'status':'PASS' if ok else 'FAIL','directional_confirmation':label if ok else 'NONE',
            'reason':'Exact Mapping: converging upper/lower boundaries plus required exact slope signs; no thresholds added.'}

def evaluate_0018(row): return _eval('MURPHY_0018',row,-1,'BULLISH_STRUCTURE')
def evaluate_0019(row): return _eval('MURPHY_0019',row,1,'BEARISH_STRUCTURE')
