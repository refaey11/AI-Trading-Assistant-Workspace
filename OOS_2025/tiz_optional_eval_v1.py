from __future__ import annotations

from typing import Any, Dict


def evaluate_execution_eligibility(event: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate Nison/Risk eligibility; TIZ is metadata only.

    TIZ state is echoed for traceability and never changes eligibility.
    """
    if event.get("evaluation_mode") != "TIZ_OPTIONAL_EVAL":
        return {
            "execution_eligible": False,
            "reason": "WRONG_EVALUATION_MODE",
            "tiz_decision_authority": False,
        }

    if not bool(event.get("nison_evidence_available")):
        return {
            "execution_eligible": False,
            "reason": "MISSING_NISON_EVIDENCE",
            "tiz_decision_authority": False,
        }

    if not bool(event.get("risk_pass")):
        return {
            "execution_eligible": False,
            "reason": "RISK_FAIL",
            "tiz_decision_authority": False,
        }

    tiz_state = str(event.get("tiz_status") or "NOT_EVALUABLE").upper().strip()
    return {
        "execution_eligible": True,
        "reason": "NISON_AND_RISK_PASS",
        "tiz_metadata_status": tiz_state,
        "tiz_decision_authority": False,
    }
