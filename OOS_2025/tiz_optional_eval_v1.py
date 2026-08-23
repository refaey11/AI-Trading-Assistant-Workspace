from __future__ import annotations

from typing import Any, Dict


ELIGIBLE_TIZ_STATES = {"PASS", "READY", "AVAILABLE"}


def evaluate_execution_eligibility(event: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluation-only gate that keeps TIZ optional without changing canonical mode."""
    if event.get("evaluation_mode") != "TIZ_OPTIONAL_EVAL":
        return {
            "execution_eligible": False,
            "reason": "WRONG_EVALUATION_MODE",
            "tiz_verified": False,
        }

    if not bool(event.get("nison_evidence_available")):
        return {
            "execution_eligible": False,
            "reason": "MISSING_NISON_EVIDENCE",
            "tiz_verified": False,
        }

    if not bool(event.get("risk_pass")):
        return {
            "execution_eligible": False,
            "reason": "RISK_FAIL",
            "tiz_verified": False,
        }

    tiz_state = str(event.get("tiz_status") or "NOT_EVALUABLE")
    if tiz_state in ELIGIBLE_TIZ_STATES:
        return {
            "execution_eligible": True,
            "reason": "TIZ_AVAILABLE",
            "tiz_verified": True,
        }

    return {
        "execution_eligible": True,
        "reason": "TIZ_UNAVAILABLE_UNVERIFIED",
        "tiz_verified": False,
    }
