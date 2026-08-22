from __future__ import annotations
from typing import Dict, Any
from .murphy_0008_runtime import evaluate_0008


def evaluate_rule(rule_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    if rule_id != "MURPHY_0008":
        return {"rule_id": rule_id, "status": "NOT_EVALUABLE", "reason": "Rule not registered in 0008 entry point."}
    return evaluate_0008(payload)
