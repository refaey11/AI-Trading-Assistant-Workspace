from __future__ import annotations

from typing import Any, Dict

SL_ATR = 0.75
TP_R = 2.0


ELIGIBLE_TIZ_STATES = {"READY", "PASS", "AVAILABLE"}


def build_execution_plan(event: Dict[str, Any]) -> Dict[str, Any]:
    """Build a mechanical plan without making TIZ a market-direction source.

    TIZ is process evidence. When it is unavailable/non-evaluable, the plan may
    still be evaluated/executed provided Risk has authoritatively passed. The
    returned record explicitly marks TIZ as unverified so this is never hidden.
    """
    action = event.get("final_action")
    entry = event.get("entry_price")
    atr = event.get("atr")
    risk_pass = event.get("risk_pass")
    tiz_state = str(event.get("tiz_process_state") or "NOT_EVALUABLE").upper()

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

    tiz_verified = tiz_state in ELIGIBLE_TIZ_STATES
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
        "tiz_verified": tiz_verified,
        "tiz_state": tiz_state,
        "tiz_unverified": not tiz_verified,
        "tiz_generated_direction": False,
        "risk_remains_hard_gate": True,
    }
