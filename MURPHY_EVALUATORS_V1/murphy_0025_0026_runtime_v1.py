from __future__ import annotations
from typing import Any, Dict

PASS = "PASS"
FAIL = "FAIL"
NOT_EVALUABLE = "NOT_EVALUABLE"


def evaluate_0025(payload: Dict[str, Any]) -> Dict[str, Any]:
    current_high = payload.get("current_high")
    preceding_4w_high = payload.get("preceding_4w_high")
    if current_high is None or preceding_4w_high is None:
        return {"rule_id": "MURPHY_0025", "status": NOT_EVALUABLE, "directional_confirmation": "UNKNOWN"}
    ok = current_high >= preceding_4w_high
    return {"rule_id": "MURPHY_0025", "status": PASS if ok else FAIL,
            "directional_confirmation": "BULLISH" if ok else "NONE"}


def evaluate_0026(payload: Dict[str, Any]) -> Dict[str, Any]:
    current_low = payload.get("current_low")
    preceding_4w_low = payload.get("preceding_4w_low")
    if current_low is None or preceding_4w_low is None:
        return {"rule_id": "MURPHY_0026", "status": NOT_EVALUABLE, "directional_confirmation": "UNKNOWN"}
    ok = current_low <= preceding_4w_low
    return {"rule_id": "MURPHY_0026", "status": PASS if ok else FAIL,
            "directional_confirmation": "BEARISH" if ok else "NONE"}
