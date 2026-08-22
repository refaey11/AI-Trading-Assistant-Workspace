from __future__ import annotations
from typing import Any, Dict


def _missing(*values: Any) -> bool:
    return any(v is None for v in values)


def evaluate_0008_candidate(row: Dict[str, Any]) -> Dict[str, Any]:
    """Source-faithful 0008 candidate using existing PF-H1/PF-B1 event data.

    This is intentionally a governance candidate, not a production-frozen
    evaluator. It recognizes the decisive-break stage only from an already
    available PF-H1 level and a completed-bar PF-B1 breakout event. The later
    rally/retest role-reversal stage is NOT_EVALUABLE unless already supplied
    by an approved downstream producer.
    """
    role = row.get("role")
    breakout_timestamp = row.get("breakout_timestamp")
    breakout_close = row.get("breakout_close")
    level_price = row.get("level_price")
    level_available_at = row.get("level_available_at")
    retest_confirmed = row.get("retest_confirmed")
    role_reversal_confirmed = row.get("role_reversal_confirmed")

    if _missing(role, breakout_timestamp, breakout_close, level_price, level_available_at):
        return {"rule_id": "MURPHY_0008", "status": "NOT_EVALUABLE", "stage": "BREAKOUT"}

    if role != "SUPPORT":
        return {"rule_id": "MURPHY_0008", "status": "FAIL", "stage": "BREAKOUT", "directional_confirmation": "NONE"}

    # PF-B1 candidate data already encodes the first completed-bar close
    # beyond an available horizontal boundary. No external numeric threshold
    # or ATR/percentage/pip filter is introduced here.
    if str(row.get("direction", "")).upper() != "DOWNSIDE":
        return {"rule_id": "MURPHY_0008", "status": "FAIL", "stage": "BREAKOUT", "directional_confirmation": "NONE"}

    # 0008 requires the later rally/retest role-reversal stage as well.
    if retest_confirmed is None or role_reversal_confirmed is None:
        return {
            "rule_id": "MURPHY_0008",
            "status": "NOT_EVALUABLE",
            "stage": "BREAKOUT_CONFIRMED_RETEST_MISSING",
            "directional_confirmation": "UNKNOWN",
        }

    ok = bool(retest_confirmed) and bool(role_reversal_confirmed)
    return {
        "rule_id": "MURPHY_0008",
        "status": "PASS" if ok else "FAIL",
        "stage": "ROLE_REVERSAL",
        "directional_confirmation": "BEARISH" if ok else "NONE",
    }
