from typing import Any, Dict

from nison_0001_0002_engulfing import (
    Candle as EngulfingCandle,
    evaluate_candle_rule_0001,
    evaluate_candle_rule_0002,
)
from nison_0003_0010_runtime import evaluate_rule as evaluate_0003_0010


def _to_engulfing_candles(payload: Dict[str, Any]):
    """Normalize router payload candles to the 0001/0002 evaluator contract."""
    return [
        candle if isinstance(candle, EngulfingCandle)
        else EngulfingCandle(
            open=candle["open"],
            high=candle["high"],
            low=candle["low"],
            close=candle["close"],
        )
        for candle in payload.get("candles", [])
    ]


def evaluate_rule(rule_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    if rule_id == "CANDLE_RULE_0001":
        return evaluate_candle_rule_0001(
            _to_engulfing_candles(payload),
            payload.get("context", {}).get("trend", ""),
            payload.get("confirmation", {}),
            volume_high=payload.get("context", {}).get("volume_high"),
            location=payload.get("context", {}).get("location"),
        )
    if rule_id == "CANDLE_RULE_0002":
        return evaluate_candle_rule_0002(
            _to_engulfing_candles(payload),
            payload.get("context", {}).get("trend", ""),
            payload.get("confirmation", {}),
            volume_high=payload.get("context", {}).get("volume_high"),
            location=payload.get("context", {}).get("location"),
        )
    return evaluate_0003_0010(rule_id, payload)
