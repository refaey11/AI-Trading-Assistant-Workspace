from __future__ import annotations
from typing import Dict, Any


def evaluate_0048(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Murphy TRIN rule 0048: 10-day TRIN MA above 1.20 -> oversold/extreme selling."""
    value = payload.get("trin_ma10")
    if value is None:
        return {"rule_id": "MURPHY_0048", "status": "NOT_EVALUABLE", "reason": "Missing trin_ma10 evidence."}
    try:
        passed = float(value) > 1.20
    except (TypeError, ValueError):
        return {"rule_id": "MURPHY_0048", "status": "NOT_EVALUABLE", "reason": "Invalid trin_ma10 evidence."}
    return {
        "rule_id": "MURPHY_0048",
        "status": "PASS" if passed else "FAIL",
        "signal": "OVERSOLD" if passed else "NONE",
        "operator": "trin_ma10 > 1.20",
    }


def evaluate_0049(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Murphy TRIN rule 0049: TRIN below 0.70 -> excessive buying/overbought."""
    value = payload.get("trin")
    if value is None:
        return {"rule_id": "MURPHY_0049", "status": "NOT_EVALUABLE", "reason": "Missing trin evidence."}
    try:
        passed = float(value) < 0.70
    except (TypeError, ValueError):
        return {"rule_id": "MURPHY_0049", "status": "NOT_EVALUABLE", "reason": "Invalid trin evidence."}
    return {
        "rule_id": "MURPHY_0049",
        "status": "PASS" if passed else "FAIL",
        "signal": "OVERBOUGHT" if passed else "NONE",
        "operator": "trin < 0.70",
    }
