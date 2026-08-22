from __future__ import annotations
from typing import Any, Dict
import importlib

_eval_mod = importlib.import_module("rules.murphy.0033.evaluator_candidate_v1")
Input = _eval_mod.Input
evaluate = _eval_mod.evaluate


def evaluate_0033(payload: Dict[str, Any]) -> Dict[str, Any]:
    required = ("reversal_candle", "short_term_trend", "oscillator_d", "candle_direction")
    if any(k not in payload for k in required):
        return {"rule_id": "MURPHY_0033", "status": "NOT_EVALUABLE", "directional_confirmation": "UNKNOWN"}
    evidence = evaluate(Input(
        reversal_candle=payload.get("reversal_candle"),
        short_term_trend=payload.get("short_term_trend"),
        oscillator_d=payload.get("oscillator_d"),
        candle_direction=payload.get("candle_direction"),
    ))
    return {
        "rule_id": "MURPHY_0033",
        "status": evidence.state,
        "directional_confirmation": evidence.direction,
        "reason": evidence.reason,
    }
