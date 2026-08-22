from __future__ import annotations
from typing import Dict, Any
from TRENDLINE_CONVERGENCE_V1.trendline_convergence_adapter import evaluate_convergence
from MURPHY_EVALUATORS_V1.murphy_0018_0019_evaluator import dispatch

def evaluate_rule(rule_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    if rule_id not in {'MURPHY_0018', 'MURPHY_0019'}:
        return {'rule_id':rule_id,'status':'NOT_EVALUABLE','reason':'Rule is not registered in this 0018/0019 runtime entry point.'}
    upper = payload.get('upper_line'); lower = payload.get('lower_line')
    if not isinstance(upper, dict) or not isinstance(lower, dict):
        return {'rule_id':rule_id,'status':'NOT_EVALUABLE','reason':'Missing upper_line/lower_line geometry payload.'}
    feature = evaluate_convergence(upper, lower)
    if feature.get('status') != 'PASS':
        return {'rule_id':rule_id,'status':'NOT_EVALUABLE','directional_confirmation':'UNKNOWN','reason':feature.get('reason','Convergence feature unavailable.')}
    return dispatch(rule_id, feature)
