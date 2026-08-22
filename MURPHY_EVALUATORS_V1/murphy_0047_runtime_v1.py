from __future__ import annotations
from typing import Any, Dict

PASS = "PASS"
FAIL = "FAIL"
NOT_EVALUABLE = "NOT_EVALUABLE"


def evaluate_0047(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Murphy 0047: new index high without A/D confirmation.

    Inputs are explicit normalized evidence fields produced by the canonical
    0047 replay pipeline. No new threshold, timeframe, proxy, or lookahead
    logic is introduced here.
    """
    required = ("index_new_high", "ad_fails_high")
    if any(k not in payload or payload.get(k) is None for k in required):
        return {
            "rule_id": "MURPHY_0047",
            "status": NOT_EVALUABLE,
            "directional_confirmation": "UNKNOWN",
            "reason": "Required 0047 divergence evidence unavailable.",
        }

    ok = bool(payload["index_new_high"]) and bool(payload["ad_fails_high"])
    return {
        "rule_id": "MURPHY_0047",
        "status": PASS if ok else FAIL,
        "directional_confirmation": "BEARISH" if ok else "NONE",
        "reason": (
            "New index high without A/D confirmation."
            if ok else
            "Required 0047 divergence condition not satisfied."
        ),
    }
