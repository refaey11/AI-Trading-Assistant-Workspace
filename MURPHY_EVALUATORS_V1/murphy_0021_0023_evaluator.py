from __future__ import annotations
from typing import Dict, Any

VALID = {"PASS", "FAIL", "NOT_EVALUABLE", "CONFLICT"}


def evaluate_0021(row: Dict[str, Any]) -> Dict[str, Any]:
    """Murphy 0021: Volume confirms price action.

    Reuses the existing project operationalization: completed-bar close versus
    previous completed close plus the existing volume_direction feature.
    No new threshold or proxy is introduced.
    """
    close = row.get("close")
    prev_close = row.get("previous_close")
    vol_dir = row.get("volume_direction")
    available = close is not None and prev_close is not None and vol_dir in {"UP", "DOWN", "FLAT"}
    if not available:
        return {"rule_id": "MURPHY_0021", "status": "NOT_EVALUABLE", "directional_confirmation": "UNKNOWN",
                "reason": "Missing completed-bar price or volume evidence."}
    if close > prev_close and vol_dir == "UP":
        return {"rule_id": "MURPHY_0021", "status": "PASS", "directional_confirmation": "BULLISH",
                "reason": "Price direction and existing volume_direction were evaluated without adding a threshold."}
    if close < prev_close and vol_dir == "UP":
        return {"rule_id": "MURPHY_0021", "status": "PASS", "directional_confirmation": "BEARISH",
                "reason": "Price direction and existing volume_direction were evaluated without adding a threshold."}
    if close > prev_close or close < prev_close:
        return {"rule_id": "MURPHY_0021", "status": "FAIL", "directional_confirmation": "NONE",
                "reason": "Price moved but volume did not confirm under the existing volume_direction rule."}
    return {"rule_id": "MURPHY_0021", "status": "NOT_EVALUABLE", "directional_confirmation": "UNKNOWN",
            "reason": "Flat price is not confirmation."}


def evaluate_0022(row: Dict[str, Any]) -> Dict[str, Any]:
    """Price up + volume up + futures OI up."""
    close = row.get("close"); prev_close = row.get("previous_close")
    vol_dir = row.get("volume_direction"); oi_dir = row.get("oi_direction")
    available = (close is not None and prev_close is not None and
                 vol_dir in {"UP", "DOWN", "FLAT"} and oi_dir in {"UP", "DOWN", "FLAT"})
    if not available:
        return {"rule_id": "MURPHY_0022", "status": "NOT_EVALUABLE", "directional_confirmation": "UNKNOWN",
                "reason": "Missing completed-bar price, volume, or available futures-OI evidence."}
    ok = close > prev_close and vol_dir == "UP" and oi_dir == "UP"
    return {"rule_id": "MURPHY_0022", "status": "PASS" if ok else "FAIL",
            "directional_confirmation": "BULLISH" if ok else "NONE",
            "reason": "Requires price UP + volume UP + futures OI UP; no extra threshold added."}


def evaluate_0023(row: Dict[str, Any]) -> Dict[str, Any]:
    """Price down + volume up + futures OI up."""
    close = row.get("close"); prev_close = row.get("previous_close")
    vol_dir = row.get("volume_direction"); oi_dir = row.get("oi_direction")
    available = (close is not None and prev_close is not None and
                 vol_dir in {"UP", "DOWN", "FLAT"} and oi_dir in {"UP", "DOWN", "FLAT"})
    if not available:
        return {"rule_id": "MURPHY_0023", "status": "NOT_EVALUABLE", "directional_confirmation": "UNKNOWN",
                "reason": "Missing completed-bar price, volume, or available futures-OI evidence."}
    ok = close < prev_close and vol_dir == "UP" and oi_dir == "UP"
    return {"rule_id": "MURPHY_0023", "status": "PASS" if ok else "FAIL",
            "directional_confirmation": "BEARISH" if ok else "NONE",
            "reason": "Requires price DOWN + volume UP + futures OI UP; no extra threshold added."}
