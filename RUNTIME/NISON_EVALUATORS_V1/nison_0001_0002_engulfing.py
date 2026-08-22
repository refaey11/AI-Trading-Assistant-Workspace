from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class Candle:
    open: float
    high: float
    low: float
    close: float


def _body(c: Candle):
    return (min(c.open, c.close), max(c.open, c.close))


def _real_body_engulfs(previous: Candle, current: Candle) -> bool:
    prev_lo, prev_hi = _body(previous)
    cur_lo, cur_hi = _body(current)
    return cur_lo <= prev_lo and cur_hi >= prev_hi and cur_hi > cur_lo


def _evaluate(
    rule_id: str,
    candles: List[Candle],
    trend: str,
    confirmation: Dict[str, Any],
    *,
    volume_high: Optional[bool] = None,
    location: Optional[str] = None,
) -> Dict[str, Any]:
    if len(candles) < 2:
        return {"status": "NOT_EVALUABLE", "rule_id": rule_id, "reason": "need two candles"}

    previous, current = candles[-2], candles[-1]

    if rule_id == "CANDLE_RULE_0001":
        if trend != "Downtrend":
            return {"status": "FAIL", "rule_id": rule_id, "reason": "required prior trend not satisfied"}
        if not (previous.close < previous.open and current.close > current.open):
            return {"status": "FAIL", "rule_id": rule_id, "reason": "candle polarity not satisfied"}
        if not _real_body_engulfs(previous, current):
            return {"status": "FAIL", "rule_id": rule_id, "reason": "second real body does not engulf first real body"}
        confirmed = bool(confirmation.get("strong_bullish_candle")) or bool(
            confirmation.get("break_above_engulfing_high")
        )
        direction = "BUY_CANDIDATE"
        entry_trigger = "Break Above High"
        stop_loss_rule = "Below Low"

    elif rule_id == "CANDLE_RULE_0002":
        if trend != "Uptrend":
            return {"status": "FAIL", "rule_id": rule_id, "reason": "required prior trend not satisfied"}
        if not (previous.close > previous.open and current.close < current.open):
            return {"status": "FAIL", "rule_id": rule_id, "reason": "candle polarity not satisfied"}
        if not _real_body_engulfs(previous, current):
            return {"status": "FAIL", "rule_id": rule_id, "reason": "second real body does not engulf first real body"}
        confirmed = bool(confirmation.get("strong_bearish_candle")) or bool(
            confirmation.get("break_below_engulfing_low")
        )
        direction = "SELL_CANDIDATE"
        entry_trigger = "Break Below Low"
        stop_loss_rule = "Above High"

    else:
        return {"status": "NOT_EVALUABLE", "rule_id": rule_id, "reason": "unsupported rule"}

    if not confirmed:
        return {"status": "FAIL", "rule_id": rule_id, "reason": "confirmation required by source contract"}

    return {
        "status": "PASS",
        "rule_id": rule_id,
        "direction": direction,
        "entry_trigger": entry_trigger,
        "stop_loss_rule": stop_loss_rule,
        "preferred_evidence": {
            "volume_high": volume_high,
            "location": location,
        },
        "provenance": {
            "source": "Steve Nison C101/C102",
            "lookahead": "none",
            "numeric_thresholds_invented": False,
        },
    }


def evaluate_candle_rule_0001(
    candles: List[Candle], trend: str, confirmation: Dict[str, Any], *, volume_high: Optional[bool] = None,
    location: Optional[str] = None,
) -> Dict[str, Any]:
    return _evaluate("CANDLE_RULE_0001", candles, trend, confirmation, volume_high=volume_high, location=location)


def evaluate_candle_rule_0002(
    candles: List[Candle], trend: str, confirmation: Dict[str, Any], *, volume_high: Optional[bool] = None,
    location: Optional[str] = None,
) -> Dict[str, Any]:
    return _evaluate("CANDLE_RULE_0002", candles, trend, confirmation, volume_high=volume_high, location=location)
