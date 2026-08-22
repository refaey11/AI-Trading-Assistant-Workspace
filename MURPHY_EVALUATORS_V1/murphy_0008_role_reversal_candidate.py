from __future__ import annotations
from typing import Any, Dict


def _missing(*values: Any) -> bool:
    return any(v is None for v in values)


def evaluate_0008_candidate(event: Dict[str, Any]) -> Dict[str, Any]:
    """Candidate-only 0008 role-reversal evaluator.

    This implementation intentionally uses the project's current candidate
    event fields and is NOT Production Frozen. It detects a support-to-
    resistance sequence only when explicit timestamps/evidence are supplied.
    """
    role = event.get("role")
    direction = event.get("direction")
    breakout_ts = event.get("breakout_timestamp")
    retest_ts = event.get("retest_timestamp")
    role_reversal_ts = event.get("role_reversal_timestamp")
    level_price = event.get("level_price")

    if _missing(role, direction, breakout_ts, level_price):
        return {"rule_id": "MURPHY_0008", "status": "NOT_EVALUABLE", "reason": "Missing PF-H1/PF-B1 evidence."}
    if role != "SUPPORT" or direction != "DOWNSIDE":
        return {"rule_id": "MURPHY_0008", "status": "FAIL", "directional_confirmation": "NONE"}
    if retest_ts is None or role_reversal_ts is None:
        return {"rule_id": "MURPHY_0008", "status": "NOT_EVALUABLE", "reason": "Retest/role-reversal evidence unavailable."}
    if retest_ts <= breakout_ts or role_reversal_ts <= retest_ts:
        return {"rule_id": "MURPHY_0008", "status": "NOT_EVALUABLE", "reason": "Invalid event chronology."}
    return {
        "rule_id": "MURPHY_0008",
        "status": "CANDIDATE_PASS",
        "directional_confirmation": "BEARISH",
        "governance_state": "CANDIDATE_NOT_PRODUCTION_FROZEN",
    }
