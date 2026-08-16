"""Candidate end-to-end evaluator for Murphy 0013.

Combines the existing 0013 structural evaluator with the candidate B1
operator. This is not production-frozen and does not alter the canonical
geometry engine.
"""
from typing import Any, Dict, Sequence

from .murphy_structural_evaluators_v1 import evaluate_0013
from .murphy_0013_b1_candidate_v1 import evaluate_0013_b1_candidate


def evaluate_0013_rule_candidate(
    upper: Dict[str, Any],
    lower: Dict[str, Any],
    decision_time: Any,
    boundary: float | None,
    boundary_available: bool,
    closes: Sequence[float],
    direction: str,
    close_available_timestamps: Sequence[Any] | None = None,
) -> Dict[str, Any]:
    structural = evaluate_0013(upper, lower, decision_time)
    if structural.get("status") != "CONFIRMED":
        return {"status": structural.get("status"), "stage": "STRUCTURAL", "detail": structural}

    b1 = evaluate_0013_b1_candidate(
        boundary,
        boundary_available,
        closes,
        direction,
        close_available_timestamps,
        decision_time,
    )
    if b1.get("status") != "DECISIVE_BREAK_CONFIRMED":
        return {"status": b1.get("status"), "stage": "B1", "detail": b1}

    return {
        "status": "CONFIRMED",
        "stage": "RULE_CANDIDATE",
        "structural": structural,
        "b1": b1,
    }
