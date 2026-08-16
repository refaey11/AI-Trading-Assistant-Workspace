"""Isolated Rule Factory V1.

This is an orchestration layer only. It must not alter canonical rule meaning,
generate trading direction, or silently tune parameters.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict, Any


class RuleStatus(str, Enum):
    FROZEN = "FROZEN"
    CANDIDATE = "CANDIDATE"
    BLOCKED = "BLOCKED"
    FAIL = "FAIL"


@dataclass(frozen=True)
class RuleSpec:
    rule_id: str
    canonical_evaluator: Callable[[Dict[str, Any]], Dict[str, Any]]
    tests: Callable[[Dict[str, Any]], bool]
    historical_qa: Callable[[Dict[str, Any]], bool]
    lookahead_gate: Callable[[Dict[str, Any]], bool]
    oos_gate: Callable[[Dict[str, Any]], bool]


def evaluate_rule(spec: RuleSpec, context: Dict[str, Any]) -> Dict[str, Any]:
    """Run gates in order and stop safely on the first failed gate."""
    canonical = spec.canonical_evaluator(context)
    if canonical.get("status") in {"BLOCKED", "NOT_EVALUABLE"}:
        return {"rule_id": spec.rule_id, "status": RuleStatus.BLOCKED.value,
                "reason": "canonical_not_evaluable", "canonical": canonical}
    if canonical.get("status") == "FAIL":
        return {"rule_id": spec.rule_id, "status": RuleStatus.FAIL.value,
                "reason": "canonical_failure", "canonical": canonical}
    if not spec.tests(context):
        return {"rule_id": spec.rule_id, "status": RuleStatus.FAIL.value,
                "reason": "tests_failed", "canonical": canonical}
    if not spec.historical_qa(context):
        return {"rule_id": spec.rule_id, "status": RuleStatus.CANDIDATE.value,
                "reason": "historical_qa_pending", "canonical": canonical}
    if not spec.lookahead_gate(context):
        return {"rule_id": spec.rule_id, "status": RuleStatus.BLOCKED.value,
                "reason": "lookahead_gate_failed", "canonical": canonical}
    if not spec.oos_gate(context):
        return {"rule_id": spec.rule_id, "status": RuleStatus.BLOCKED.value,
                "reason": "oos_gate_failed", "canonical": canonical}
    return {"rule_id": spec.rule_id, "status": RuleStatus.FROZEN.value,
            "reason": "all_registered_gates_passed", "canonical": canonical}
