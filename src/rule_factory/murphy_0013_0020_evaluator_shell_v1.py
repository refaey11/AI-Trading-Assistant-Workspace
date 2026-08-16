"""Evaluator shell for Murphy 0013-0020.

This layer performs prerequisite gating only. It intentionally does not
invent pattern semantics, tolerances, thresholds, or source interpretations.
"""
from typing import Any, Dict

from .murphy_0013_0020_shared_primitive_adapter_v1 import RULE_PRIMITIVE_MAP


def evaluate_rule_shell(rule_id: str, primitive_results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    required = RULE_PRIMITIVE_MAP.get(rule_id)
    if required is None:
        return {"status": "UNKNOWN_RULE", "rule_id": rule_id}

    blocked = [
        primitive for primitive in required
        if primitive_results.get(primitive, {}).get("status")
        in {"NOT_EVALUABLE", "NOT_CONFIRMED"}
    ]

    if blocked:
        return {
            "status": "PARTIAL",
            "rule_id": rule_id,
            "blocked_primitives": blocked,
            "reason": "prerequisite_contract_missing_or_unconfirmed",
        }

    return {
        "status": "READY_FOR_RULE_SEMANTICS",
        "rule_id": rule_id,
        "required_primitives": required,
    }


def evaluate_ready_batch(primitive_results: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {
        rule_id: evaluate_rule_shell(rule_id, primitive_results)
        for rule_id in ("0013", "0014", "0018", "0019", "0020")
    }
