from __future__ import annotations

from typing import Any, Dict

SL_ATR = 0.75
TP_R = 2.0


def build_optional_oos_execution_plan(event: Dict[str, Any]) -> Dict[str, Any]:
    """Build an evaluation-only execution plan with TIZ as optional metadata.

    Direction, Risk pass, entry, and ATR determine this adapter's result.
    TIZ is echoed for audit only; it cannot block or alter the plan.
    """
    if event.get("evaluation_mode") != "TIZ_OPTIONAL_EVAL":
        return {"status": "NOT_EXECUTABLE", "reason": "WRONG_EVALUATION_MODE"}

    action = event.get("final_action")
    if action not in {"BUY", "SELL"}:
        return {"status": "NOT_EXECUTABLE", "reason": "invalid_or_missing_direction"}

    if event.get("risk_pass") is not True:
        return {"status": "NOT_EXECUTABLE", "reason": "risk_gate_not_passed"}

    entry = event.get("entry_price")
    atr = event.get("atr")
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
        "tiz_metadata_status": str(event.get("tiz_process_state") or "NOT_EVALUABLE").upper(),
        "tiz_decision_authority": False,
        "evaluation_mode": "TIZ_OPTIONAL_EVAL",
    }
