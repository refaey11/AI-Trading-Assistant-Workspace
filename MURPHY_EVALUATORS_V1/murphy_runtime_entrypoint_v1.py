from __future__ import annotations
from typing import Dict, Any
from MURPHY_EVALUATORS_V1.murphy_0003_0004_runtime_v2 import evaluate_0003, evaluate_0004
from MURPHY_EVALUATORS_V1.murphy_0006_0007_runtime_v1 import evaluate_0006, evaluate_0007
from MURPHY_EVALUATORS_V1.murphy_0021_0023_evaluator import evaluate_0021, evaluate_0022, evaluate_0023
from MURPHY_EVALUATORS_V1.murphy_0025_0026_runtime_v1 import evaluate_0025, evaluate_0026
from MURPHY_EVALUATORS_V1.murphy_0028_0029_evaluator import evaluate_0028
from MURPHY_EVALUATORS_V1.murphy_0029_runtime_adapter import evaluate_0029
from MURPHY_EVALUATORS_V1.murphy_0030_0032_runtime_v1 import evaluate_0030, evaluate_0031, evaluate_0032
from MURPHY_EVALUATORS_V1.murphy_0033_runtime_v1 import evaluate_0033
from MURPHY_EVALUATORS_V1.murphy_0047_runtime_v1 import evaluate_0047
from MURPHY_EVALUATORS_V1.murphy_0048_0049_runtime_v1 import evaluate_0048, evaluate_0049
from MURPHY_EVALUATORS_V1.murphy_0050_evaluator import evaluate_0050
from MURPHY_EVALUATORS_V1.murphy_0051_runtime_v1 import evaluate_0051
from TRENDLINE_CONVERGENCE_V1.trendline_convergence_adapter import evaluate_convergence
from MURPHY_EVALUATORS_V1.murphy_0018_0019_evaluator import dispatch


def evaluate_rule(rule_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    if rule_id == 'MURPHY_0003':
        return evaluate_0003(payload.get('current_reaction_peak'), payload.get('prior_reaction_peak'), payload.get('current_reaction_trough'), payload.get('prior_reaction_trough'))
    if rule_id == 'MURPHY_0004':
        return evaluate_0004(payload.get('current_reaction_peak'), payload.get('prior_reaction_peak'), payload.get('current_reaction_trough'), payload.get('prior_reaction_trough'))
    if rule_id == 'MURPHY_0006':
        return evaluate_0006(payload.get('events'), payload.get('line_price_at'))
    if rule_id == 'MURPHY_0007':
        return evaluate_0007(payload.get('events'), payload.get('line_price_at'))
    if rule_id == 'MURPHY_0021':
        return evaluate_0021(payload)
    if rule_id == 'MURPHY_0022':
        return evaluate_0022(payload)
    if rule_id == 'MURPHY_0023':
        return evaluate_0023(payload)
    if rule_id == 'MURPHY_0025':
        return evaluate_0025(payload)
    if rule_id == 'MURPHY_0026':
        return evaluate_0026(payload)
    if rule_id == 'MURPHY_0028':
        return evaluate_0028(payload)
    if rule_id == 'MURPHY_0029':
        return evaluate_0029(payload)
    if rule_id == 'MURPHY_0030':
        return evaluate_0030(payload)
    if rule_id == 'MURPHY_0031':
        return evaluate_0031(payload)
    if rule_id == 'MURPHY_0032':
        return evaluate_0032(payload)
    if rule_id == 'MURPHY_0033':
        return evaluate_0033(payload)
    if rule_id == 'MURPHY_0047':
        return evaluate_0047(payload)
    if rule_id == 'MURPHY_0048':
        return evaluate_0048(payload)
    if rule_id == 'MURPHY_0049':
        return evaluate_0049(payload)
    if rule_id == 'MURPHY_0050':
        return evaluate_0050(payload)
    if rule_id == 'MURPHY_0051':
        return evaluate_0051(payload)
    if rule_id not in {'MURPHY_0018', 'MURPHY_0019'}:
        return {'rule_id':rule_id,'status':'NOT_EVALUABLE','reason':'Rule is not registered in this runtime entry point.'}
    upper = payload.get('upper_line'); lower = payload.get('lower_line')
    if not isinstance(upper, dict) or not isinstance(lower, dict):
        return {'rule_id':rule_id,'status':'NOT_EVALUABLE','directional_confirmation':'UNKNOWN','reason':'Missing upper_line/lower_line geometry payload.'}
    feature = evaluate_convergence(upper, lower)
    if feature.get('status') != 'PASS':
        return {'rule_id':rule_id,'status':'NOT_EVALUABLE','directional_confirmation':'UNKNOWN','reason':feature.get('reason','Convergence feature unavailable.')}
    return dispatch(rule_id, feature)
