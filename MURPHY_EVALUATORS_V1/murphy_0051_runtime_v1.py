from __future__ import annotations
from typing import Dict, Any

REQUIRED_FIELDS = (
    'direction',
    'stance',
    'position_size',
    'acceptable_loss',
    'profit_objective',
    'entry',
    'order_type',
    'stop_loss',
)


def evaluate_0051(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        return {
            'rule_id': 'MURPHY_0051',
            'status': 'NOT_EVALUABLE',
            'reason': 'Required trade-plan field status is unavailable.'
        }

    unknown = [k for k in REQUIRED_FIELDS if k not in payload]
    if unknown:
        return {
            'rule_id': 'MURPHY_0051',
            'status': 'NOT_EVALUABLE',
            'reason': 'Required field status unknown/unavailable.',
            'missing_status_fields': unknown,
        }

    missing = [
        k for k in REQUIRED_FIELDS
        if payload.get(k) is None or (isinstance(payload.get(k), str) and not payload.get(k).strip())
    ]
    if missing:
        return {
            'rule_id': 'MURPHY_0051',
            'status': 'FAIL',
            'reason': 'At least one required plan field is explicitly missing/empty.',
            'missing_fields': missing,
        }

    return {
        'rule_id': 'MURPHY_0051',
        'status': 'PASS',
        'gate': 'PLAN_COMPLETE',
        'direction_generation': False,
    }
