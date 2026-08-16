"""Governance gate for the Murphy 0030 hybrid compatibility path.

This gate does not define Murphy semantics and does not choose a box-size
policy. It only prevents the evaluator from advancing while required
compatibility evidence is unresolved.
"""
from typing import Literal

GateStatus = Literal["PASS", "NOT_EVALUABLE", "BLOCKED"]


def evaluate_0030_compatibility_gate(
    *,
    source_contract: bool,
    engine_compatibility: bool,
    box_size_policy_approved: bool,
    availability_no_lookahead: bool,
    deterministic_replay: bool,
) -> GateStatus:
    """Return a fail-closed governance state for 0030.

    Every required dependency must be explicitly proven. This function never
    infers compatibility from profitability or historical outcomes.
    """
    if not source_contract:
        return "BLOCKED"

    if not box_size_policy_approved:
        return "NOT_EVALUABLE"

    if not engine_compatibility:
        return "NOT_EVALUABLE"

    if not availability_no_lookahead:
        return "NOT_EVALUABLE"

    if not deterministic_replay:
        return "NOT_EVALUABLE"

    return "PASS"
