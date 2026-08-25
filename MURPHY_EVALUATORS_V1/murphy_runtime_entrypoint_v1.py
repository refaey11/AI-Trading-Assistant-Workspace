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
from MURPHY_EVALUATORS_V1.murphy_0034_0045_recovered_v1 import (
    wave2, wave3, wave4, fib_zone, cycle_period, system_discipline,
    psar_regime, adx_regime, capital_reserve, single_market_exposure,
    market_risk, total_margin,
)
from MURPHY_EVALUATORS_V1.murphy_0047_runtime_v1 import evaluate_0047
from MURPHY_EVALUATORS_V1.murphy_0048_0049_runtime_v1 import evaluate_0048, evaluate_0049
from MURPHY_EVALUATORS_V1.murphy_0050_evaluator import evaluate_0050
from MURPHY_EVALUATORS_V1.murphy_0051_runtime_v1 import evaluate_0051
from TRENDLINE_CONVERGENCE_V1.trendline_convergence_adapter import evaluate_convergence
from MURPHY_EVALUATORS_V1.murphy_0018_0019_evaluator import dispatch


def _result(rule_id: str, result: Any) -> Dict[str, Any]:
    return {"rule_id": rule_id, "status": result.state, "reason": result.reason}


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
    if rule_id == 'MURPHY_0034':
        return _result(rule_id, wave2(payload.get('wave1_high'), payload.get('wave1_low'), payload.get('wave2_extreme')))
    if rule_id == 'MURPHY_0035':
        return _result(rule_id, wave3(payload.get('length1'), payload.get('length3'), payload.get('length5')))
    if rule_id == 'MURPHY_0036':
        return _result(rule_id, wave4(payload.get('wave1_low'), payload.get('wave1_high'), payload.get('wave4_price')))
    if rule_id == 'MURPHY_0037':
        return _result(rule_id, fib_zone(payload.get('retracement_pct')))
    if rule_id == 'MURPHY_0038':
        return _result(rule_id, cycle_period(payload.get('previous_trough'), payload.get('current_trough')))
    if rule_id == 'MURPHY_0039':
        return _result(rule_id, system_discipline(payload.get('system_defined'), payload.get('regime_checked')))
    if rule_id == 'MURPHY_0040':
        return _result(rule_id, psar_regime(payload.get('trending')))
    if rule_id == 'MURPHY_0041':
        return _result(rule_id, adx_regime(payload.get('adx'), payload.get('threshold')))
    if rule_id == 'MURPHY_0042':
        return _result(rule_id, capital_reserve(payload.get('invested_pct')))
    if rule_id == 'MURPHY_0043':
        return _result(rule_id, single_market_exposure(payload.get('exposure_pct')))
    if rule_id == 'MURPHY_0044':
        return _result(rule_id, market_risk(payload.get('risk_pct')))
    if rule_id == 'MURPHY_0045':
        return _result(rule_id, total_margin(payload.get('margin_pct')))
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
