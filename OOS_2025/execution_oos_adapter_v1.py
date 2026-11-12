from __future__ import annotations

from typing import Any, Dict

SL_ATR = 0.75
TP_R = 2.0


def build_execution_plan(event: Dict[str, Any]) -> Dict[str, Any]:
    """Convert an approved decision into a mechanical evaluation execution plan.

    This adapter does not create direction. It consumes an already-approved
    BUY/SELL decision, authoritative Risk pass, entry price, and ATR. TIZ is
    deliberately not an input to execution eligibility.
    """
    action = event.get("final_action")
    entry = event.get("entry_price")
    atr = event.get("atr")
    risk_pass = event.get("risk_pass")

    if action not in {"BUY", "SELL"}:
        return {"status": "NOT_EXECUTABLE", "reason": "invalid_or_missing_direction"}
    if risk_pass is not True:
        return {"status": "NOT_EXECUTABLE", "reason": "risk_gate_not_passed"}
    if not isinstance(entry, (int, float)) or not isinstance(atr, (int, float)):
        return {"status": "NOT_EXECUTABLE", "reason": "missing_entry_or_atr"}
    if entry <= 0 or atr <= 0:
        return {"status": "NOT_EXECUTABLE", "reason": "invalid_entry_or_atr"}

    risk_distance = SL_ATR * atr
    reward_distance = risk_distance * TP_R

    if action == "BUY":
        stop_loss = entry - risk_distance
        take_profit = entry + reward_distance
    else:
        stop_loss = entry + risk_distance
        take_profit = entry - reward_distance

    return {
        "status": "EXECUTABLE",
        "direction": action,
        "entry_price": float(entry),
        "atr": float(atr),
        "sl_atr": SL_ATR,
        "tp_r": TP_R,
        "stop_loss": float(stop_loss),
        "take_profit": float(take_profit),
        "risk_distance": float(risk_distance),
        "reward_distance": float(reward_distance),
        "tiz_decision_authority": False,
    }
