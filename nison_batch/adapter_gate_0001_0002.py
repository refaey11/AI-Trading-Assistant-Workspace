"""Source-bounded hard-geometry gate for Nison 0001/0002.

This module intentionally evaluates only the source-stated two-candle
polarity/body-containment clauses. Context and qualitative confirmation
clauses remain outside this gate and therefore cannot produce a production
PASS by themselves.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Candle:
    open: float
    close: float


def body_low(c: Candle) -> float:
    return min(c.open, c.close)


def body_high(c: Candle) -> float:
    return max(c.open, c.close)


def bullish(c: Candle) -> bool:
    return c.close > c.open


def bearish(c: Candle) -> bool:
    return c.close < c.open


def body_engulfs(engulfing: Candle, prior: Candle) -> bool:
    return body_low(engulfing) <= body_low(prior) and body_high(engulfing) >= body_high(prior)


def evaluate_hard_geometry(rule_id: str, prior: Candle, current: Candle) -> bool:
    """Return only the source-stated hard formation geometry.

    No trend, support/resistance, volume, strength, confirmation candle,
    threshold, lookback, or direction-generation logic is included.
    """
    if rule_id == "NISON_0001":
        return bearish(prior) and bullish(current) and body_engulfs(current, prior)
    if rule_id == "NISON_0002":
        return bullish(prior) and bearish(current) and body_engulfs(current, prior)
    raise ValueError(f"Unsupported rule_id: {rule_id}")
