from typing import Any, Dict

from nison_0001_0002_engulfing import (
    evaluate_candle_rule_0001,
    evaluate_candle_rule_0002,
)
from nison_0003_0010_runtime import evaluate_rule as evaluate_0003_0010


def evaluate_rule(rule_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    if rule_id == "CANDLE_RULE_0001":
        return evaluate_candle_rule_0001(
            payload.get("candles", []),
            payload.get("context", {}).get("trend", ""),
            payload.get("confirmation", {}),
            volume_high=payload.get("context", {}).get("volume_high"),
            location=payload.get("context", {}).get("location"),
        )
    if rule_id == "CANDLE_RULE_0002":
        return evaluate_candle_rule_0002(
            payload.get("candles", []),
            payload.get("context", {}).get("trend", ""),
            payload.get("confirmation", {}),
            volume_high=payload.get("context", {}).get("volume_high"),
            location=payload.get("context", {}).get("location"),
        )
    return evaluate_0003_0010(rule_id, payload)
