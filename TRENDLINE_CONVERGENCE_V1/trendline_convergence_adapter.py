from __future__ import annotations
from typing import Dict, Any
from datetime import datetime

def _parse(ts):
    return datetime.fromisoformat(str(ts).replace('Z', '+00:00'))

def _value(line, t):
    t1 = _parse(line['point_1_timestamp']); t2 = _parse(line['point_2_timestamp'])
    p1 = float(line['point_1_price']); p2 = float(line['point_2_price'])
    dt = (t2 - t1).total_seconds()
    if dt <= 0:
        return None
    return p1 + (p2 - p1) * ((_parse(t) - t1).total_seconds() / dt)

def evaluate_convergence(upper: Dict[str, Any], lower: Dict[str, Any]) -> Dict[str, Any]:
    required = ['line_type','point_1_timestamp','point_1_price','point_2_timestamp','point_2_price','availability_timestamp']
    if any(upper.get(k) is None for k in required) or any(lower.get(k) is None for k in required):
        return {'status':'NOT_EVALUABLE','trendlines_converging':None,'reason':'Missing confirmed two-point trendline evidence.'}
    if upper['line_type'] != 'HIGH' or lower['line_type'] != 'LOW':
        return {'status':'NOT_EVALUABLE','trendlines_converging':None,'reason':'Expected HIGH upper line and LOW lower line.'}
    try:
        a = max(_parse(upper['availability_timestamp']), _parse(lower['availability_timestamp']))
        ua = _value(upper, a); la = _value(lower, a)
        su = float(upper.get('slope_price_per_second', upper.get('slope_price_per_time')))
        sl = float(lower.get('slope_price_per_second', lower.get('slope_price_per_time')))
        gap = ua - la
        if gap <= 0:
            return {'status':'NOT_EVALUABLE','trendlines_converging':None,'reason':'No valid positive upper-over-lower gap at common availability.'}
        return {
            'status':'PASS',
            'trendlines_converging': (su - sl) < 0,
            'upper_slope': su,
            'lower_slope': sl,
            'availability_timestamp': a.isoformat(),
            'reason':'Exact gap-rate sign from confirmed geometry; no tolerance or threshold added.'
        }
    except Exception as e:
        return {'status':'NOT_EVALUABLE','trendlines_converging':None,'reason':f'Geometry unavailable: {type(e).__name__}.'}
