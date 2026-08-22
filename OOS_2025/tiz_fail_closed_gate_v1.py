from __future__ import annotations

from typing import Any, Dict


def evaluate_tiz_gate(evidence: Dict[str, Any]) -> Dict[str, Any]:
    """Apply the existing TIZ boundary without inventing psychology semantics.

    TIZ is process/execution discipline only. It never creates direction.
    Missing or non-authoritative evidence remains NOT_EVALUABLE and is treated
    as a hard no-trade gate for execution purposes.
    """
    state = evidence.get("tiz_process_state")
    authoritative = evidence.get("authoritative")
    direction = evidence.get("direction", "NEUTRAL")

    # TIZ must remain direction-neutral.
    if direction not in {None, "NEUTRAL"}:
        return {
            "status": "BLOCKED",
            "process_state": "NOT_EVALUABLE",
            "execution_allowed": False,
            "reason": "tiz_direction_must_be_neutral",
        }

    if state == "NOT_EVALUABLE" or authoritative is not True:
        return {
            "status": "NOT_EVALUABLE",
            "process_state": "NOT_EVALUABLE",
            "execution_allowed": False,
            "reason": "missing_or_non_authoritative_tiz_evidence",
        }

    if state in {"READY", "PASS", "AVAILABLE"}:
        return {
            "status": "PASS",
            "process_state": state,
            "execution_allowed": True,
            "reason": "authoritative_tiz_gate_available",
        }

    return {
        "status": "NOT_EVALUABLE",
        "process_state": "NOT_EVALUABLE",
        "execution_allowed": False,
        "reason": "unsupported_tiz_state",
    }
