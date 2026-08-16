"""Batch audit for Murphy rules 0013-0020.

This deliberately audits wiring readiness only. It does not claim a rule is
production-ready and never substitutes missing source semantics with guesses.
"""
from typing import Any, Dict

from .murphy_0013_0020_shared_primitive_adapter_v1 import RULE_PRIMITIVE_MAP


def audit_rules_0013_0020(primitive_results: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    report: Dict[str, Dict[str, Any]] = {}
    for rule_id, required in RULE_PRIMITIVE_MAP.items():
        blocked = [
            primitive
            for primitive in required
            if primitive_results.get(primitive, {}).get("status")
            in {"NOT_EVALUABLE", "NOT_CONFIRMED"}
        ]
        report[rule_id] = {
            "status": "READY_FOR_RULE_EVALUATION" if not blocked else "PARTIAL",
            "required_primitives": required,
            "blocked_primitives": blocked,
        }
    return report
