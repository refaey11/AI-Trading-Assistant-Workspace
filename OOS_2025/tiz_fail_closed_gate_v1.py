from __future__ import annotations

from typing import Any, Dict


def evaluate_tiz_gate(evidence: Dict[str, Any]) -> Dict[str, Any]:
    """Legacy-compatible TIZ observer; it has no execution or decision authority.

    The function name is retained for import compatibility only. Its output is
    diagnostic metadata and must never be used to allow, block, or size a trade.
    """
    state = str(
        evidence.get("tiz_process_state")
        or evidence.get("process_state")
        or evidence.get("status")
        or "NOT_EVALUABLE"
    ).upper().strip()
    direction = evidence.get("direction", "NEUTRAL")
    return {
        "status": "METADATA_ONLY",
        "process_state": state,
        "reported_direction": direction,
        "direction_field_valid": direction in {None, "NEUTRAL"},
        "decision_authority": False,
        "execution_effect": False,
        "risk_effect": False,
        "reason": "TIZ_RETAINED_FOR_OPTIONAL_AUDIT_ONLY",
    }
