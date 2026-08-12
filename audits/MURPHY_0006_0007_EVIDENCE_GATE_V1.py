from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional


def _not_evaluable(rule_id: str, reason: str) -> Dict[str, Any]:
    return {
        "rule_id": rule_id,
        "status": "NOT_EVALUABLE",
        "direction": "NONE",
        "reason": reason,
    }


def evaluate_0006_0007_evidence_gate(
    *,
    rule_id: str,
    line_type: Optional[str],
    direction: Optional[str],
    line_availability_timestamp: Optional[datetime],
    third_touch_timestamp: Optional[datetime],
    third_touch_price: Optional[float],
    third_touch_detected: Optional[bool],
    reaction_detected: Optional[bool],
    no_break_valid: Optional[bool],
    confirmation_timestamp: Optional[datetime],
) -> Dict[str, Any]:
    """Source-safe gate for Murphy 0006/0007 evidence.

    This adapter intentionally does NOT infer touch tolerance, reaction magnitude,
    or break thresholds from raw bars. Those operators remain source/project-open.

    PASS is possible only when an upstream approved evidence producer has already
    supplied explicit event flags/timestamps satisfying the qualitative Murphy
    contract. Missing/unknown evidence returns NOT_EVALUABLE.
    """
    if rule_id not in {"MURPHY_0006", "MURPHY_0007"}:
        return _not_evaluable(rule_id, "unsupported_rule_id")

    expected = {
        "MURPHY_0006": ("LOW", "UP", "BULLISH"),
        "MURPHY_0007": ("HIGH", "DOWN", "BEARISH"),
    }[rule_id]

    expected_line_type, expected_direction, decision_direction = expected

    if line_type != expected_line_type or direction != expected_direction:
        return _not_evaluable(rule_id, "line_family_or_direction_mismatch")

    required = {
        "line_availability_timestamp": line_availability_timestamp,
        "third_touch_timestamp": third_touch_timestamp,
        "third_touch_price": third_touch_price,
        "third_touch_detected": third_touch_detected,
        "reaction_detected": reaction_detected,
        "no_break_valid": no_break_valid,
        "confirmation_timestamp": confirmation_timestamp,
    }
    if any(value is None for value in required.values()):
        return _not_evaluable(rule_id, "required_confirmation_evidence_missing")

    # bool(None) is prevented above; explicit false means the required condition
    # was evaluated and did not hold.
    if not third_touch_detected:
        return {
            "rule_id": rule_id,
            "status": "FAIL",
            "direction": "NONE",
            "reason": "third_touch_not_confirmed",
        }

    if not reaction_detected:
        return {
            "rule_id": rule_id,
            "status": "FAIL",
            "direction": "NONE",
            "reason": "reaction_not_confirmed",
        }

    if not no_break_valid:
        return {
            "rule_id": rule_id,
            "status": "FAIL",
            "direction": "NONE",
            "reason": "line_hold_no_break_not_confirmed",
        }

    if third_touch_timestamp < line_availability_timestamp:
        return _not_evaluable(rule_id, "touch_before_line_availability")

    if confirmation_timestamp < third_touch_timestamp:
        return _not_evaluable(rule_id, "confirmation_before_third_touch")

    return {
        "rule_id": rule_id,
        "status": "PASS",
        "direction": decision_direction,
        "third_touch_timestamp": third_touch_timestamp.isoformat(),
        "third_touch_price": third_touch_price,
        "confirmation_timestamp": confirmation_timestamp.isoformat(),
        "line_availability_timestamp": line_availability_timestamp.isoformat(),
    }
