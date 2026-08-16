"""Isolated Rule Factory V1.

Orchestration only: never changes canonical meaning, generates direction,
or silently tunes parameters.
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
    source_status: str = ""


def evaluate_rule(spec: RuleSpec, context: Dict[str, Any]) -> Dict[str, Any]:
    """Run promotion gates without confusing backtest-readiness with freeze."""
    canonical = spec.canonical_evaluator(context)
    if canonical.get("status") in {"BLOCKED", "NOT_EVALUABLE"}:
        return {"rule_id": spec.rule_id, "status": RuleStatus.BLOCKED.value,
                "reason": "canonical_not_evaluable", "canonical": canonical}
    if canonical.get("status") == "FAIL":
        return {"rule_id": spec.rule_id, "status": RuleStatus.FAIL.value,
                "reason": "canonical_failure", "canonical": canonical}

    # All registered gates run before promotion-state classification.
    # READY_FOR_BACKTEST is a research-state, never a freeze signal, but it
    # must not bypass tests, historical QA, lookahead, or OOS checks.
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

    if spec.source_status == "READY_FOR_BACKTEST":
        return {"rule_id": spec.rule_id, "status": RuleStatus.CANDIDATE.value,
                "reason": "ready_for_backtest_requires_promotion_gates", "canonical": canonical}

    return {"rule_id": spec.rule_id, "status": RuleStatus.FROZEN.value,
            "reason": "all_registered_promotion_gates_passed", "canonical": canonical}
