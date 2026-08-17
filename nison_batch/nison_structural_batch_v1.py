"""Nison structural batch evaluator V1.

Source-bounded structural layer only. It deliberately returns NOT_EVALUABLE
when a canonical qualitative comparator or context contract is missing.
Nison output is confirmation evidence; this module never creates a trade.
"""
from dataclasses import dataclass
from typing import Literal, Optional, Sequence

Status = Literal["PASS", "FAIL", "NOT_EVALUABLE"]
Direction = Literal["bullish", "bearish"]

@dataclass(frozen=True)
class Candle:
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    @property
    def bullish(self) -> bool: return self.close > self.open
    @property
    def bearish(self) -> bool: return self.close < self.open
    @property
    def body(self) -> float: return abs(self.close - self.open)

@dataclass(frozen=True)
class Evidence:
    rule_id: str
    status: Status
    direction: Optional[Direction]
    availability_timestamp: Optional[str]
    reason: str
    unresolved: tuple[str, ...] = ()


def window_up(c1: Candle, c2: Candle) -> bool:
    return c2.low > c1.high


def window_down(c1: Candle, c2: Candle) -> bool:
    return c2.high < c1.low


def evaluate_0034(c1: Optional[Candle], c2: Optional[Candle]) -> Evidence:
    """Separating Lines structural evaluator.

    Source-backed checks: opposite colors and equal opens; continuation
    interpretation is not inferred here. Availability is c2 close.
    """
    if c1 is None or c2 is None:
        return Evidence("CANDLE_RULE_0034", "NOT_EVALUABLE", None, None, "Missing candle input")
    if not (c1.bearish and c2.bullish):
        return Evidence("CANDLE_RULE_0034", "FAIL", None, c2.timestamp, "Required bearish then bullish colors not present")
    if c1.open != c2.open:
        return Evidence("CANDLE_RULE_0034", "FAIL", None, c2.timestamp, "Opens are not exactly equal")
    return Evidence("CANDLE_RULE_0034", "PASS", None, c2.timestamp, "Structural Separating Lines conditions satisfied")


def evaluate_0038(c1: Optional[Candle], c2: Optional[Candle]) -> Evidence:
    """Windows structural evaluator; no future closure or session inference."""
    if c1 is None or c2 is None:
        return Evidence("CANDLE_RULE_0038", "NOT_EVALUABLE", None, None, "Missing candle input")
    if window_up(c1, c2):
        return Evidence("CANDLE_RULE_0038", "PASS", "bullish", c2.timestamp, "Rising Window")
    if window_down(c1, c2):
        return Evidence("CANDLE_RULE_0038", "PASS", "bearish", c2.timestamp, "Falling Window")
    return Evidence("CANDLE_RULE_0038", "FAIL", None, c2.timestamp, "No Window between consecutive candles")


def evaluate_0021_three_mountains(peaks: Optional[Sequence[float]]) -> Evidence:
    """Three Mountains structural layer.

    Nison permits three attempts/tests of a high and does not require the
    three peaks to be exactly equal. No equality tolerance is invented.
    Final bearish candle confirmation is intentionally a separate evidence
    layer and is therefore NOT_EVALUABLE here unless supplied explicitly.
    """
    if peaks is None or len(peaks) != 3:
        return Evidence("CANDLE_RULE_0021", "NOT_EVALUABLE", None, None, "Exactly three source-defined peak events required")
    if not all(p is not None for p in peaks):
        return Evidence("CANDLE_RULE_0021", "NOT_EVALUABLE", None, None, "Missing peak value")
    return Evidence("CANDLE_RULE_0021", "PASS", "bearish", None, "Three high tests/attempts structurally present", ("final bearish candle confirmation",))


def evaluate_0023_three_buddha_tops(peaks: Optional[Sequence[float]]) -> Evidence:
    if peaks is None or len(peaks) != 3:
        return Evidence("CANDLE_RULE_0023", "NOT_EVALUABLE", None, None, "Exactly three peak events required")
    if not (peaks[1] > peaks[0] and peaks[1] > peaks[2]):
        return Evidence("CANDLE_RULE_0023", "FAIL", None, None, "Central mountain is not the highest")
    return Evidence("CANDLE_RULE_0023", "PASS", "bearish", None, "Central mountain is highest", ("confirmation/invalidation contract",))


def evaluate_0024_three_buddha_bottoms(troughs: Optional[Sequence[float]]) -> Evidence:
    if troughs is None or len(troughs) != 3:
        return Evidence("CANDLE_RULE_0024", "NOT_EVALUABLE", None, None, "Exactly three trough events required")
    if not (troughs[1] < troughs[0] and troughs[1] < troughs[2]):
        return Evidence("CANDLE_RULE_0024", "FAIL", None, None, "Central river is not the lowest")
    return Evidence("CANDLE_RULE_0024", "PASS", "bullish", None, "Central river is lowest", ("confirmation/invalidation contract",))
