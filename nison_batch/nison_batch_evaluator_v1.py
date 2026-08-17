from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Optional

@dataclass(frozen=True)
class Result:
    rule_id: str
    state: str
    side: Optional[str] = None
    reason: str = ""

# Evaluators consume canonical Market Reader primitives. No candle thresholds
# are invented here; qualitative comparators are injected or the rule remains
# NOT_EVALUABLE.

def abandoned_baby(prev, middle, curr, *, is_doji: Callable, gap_up: Callable, gap_down: Callable) -> Result:
    if not (is_doji(middle) and gap_up(prev, middle) and gap_down(middle, curr)):
        return Result("CANDLE_RULE_0012", "FAIL")
    return Result("CANDLE_RULE_0012", "PASS", None, "pattern structure detected; direction is resolved from surrounding context")

def separating_lines(prev, curr, *, equal_open: Callable) -> Result:
    if equal_open(prev, curr) and prev["close"] < prev["open"] and curr["close"] > curr["open"]:
        return Result("CANDLE_RULE_0034", "PASS", "bullish")
    if equal_open(prev, curr) and prev["close"] > prev["open"] and curr["close"] < curr["open"]:
        return Result("CANDLE_RULE_0034", "PASS", "bearish")
    return Result("CANDLE_RULE_0034", "FAIL")

def tasuki_gap(a, b, c, *, gap_up: Callable, gap_down: Callable, closes_gap: Callable) -> Result:
    if gap_up(a, b) and c["open"] < b["open"] and closes_gap(b, c):
        return Result("CANDLE_RULE_0035", "PASS", "bullish")
    if gap_down(a, b) and c["open"] > b["open"] and closes_gap(b, c):
        return Result("CANDLE_RULE_0035", "PASS", "bearish")
    return Result("CANDLE_RULE_0035", "FAIL")

def windows(a, b, *, gap_up: Callable, gap_down: Callable) -> Result:
    if gap_up(a, b): return Result("CANDLE_RULE_0038", "PASS", "bullish")
    if gap_down(a, b): return Result("CANDLE_RULE_0038", "PASS", "bearish")
    return Result("CANDLE_RULE_0038", "FAIL")

def three_mountains(*, structure_ok: Optional[bool]) -> Result:
    if structure_ok is None:
        return Result("CANDLE_RULE_0021", "NOT_EVALUABLE", reason="source-locked peak/equality comparator required")
    return Result("CANDLE_RULE_0021", "PASS" if structure_ok else "FAIL")

def three_buddha_tops(*, structure_ok: Optional[bool]) -> Result:
    if structure_ok is None:
        return Result("CANDLE_RULE_0023", "NOT_EVALUABLE", reason="source-locked shoulder/head comparator required")
    return Result("CANDLE_RULE_0023", "PASS" if structure_ok else "FAIL", "bearish" if structure_ok else None)

def three_buddha_bottoms(*, structure_ok: Optional[bool]) -> Result:
    if structure_ok is None:
        return Result("CANDLE_RULE_0024", "NOT_EVALUABLE", reason="source-locked shoulder/head comparator required")
    return Result("CANDLE_RULE_0024", "PASS" if structure_ok else "FAIL", "bullish" if structure_ok else None)
