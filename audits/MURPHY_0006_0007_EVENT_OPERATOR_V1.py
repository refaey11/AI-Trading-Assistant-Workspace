from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Optional, Sequence

@dataclass(frozen=True)
class PivotEvent:
    timestamp: datetime
    available_at: datetime
    pivot_type: str
    price: float

@dataclass(frozen=True)
class D1Bar:
    timestamp: datetime
    high: float
    low: float

@dataclass(frozen=True)
class Line:
    line_type: str
    direction: str
    available_at: datetime

@dataclass(frozen=True)
class Confirmation:
    rule_id: str
    third_touch: PivotEvent
    reaction: PivotEvent
    confirmation_available_at: datetime


def _range_intersects(bar: D1Bar, line_price: float) -> bool:
    return bar.low <= line_price <= bar.high


def _holds_without_break(bar: D1Bar, line_price: float, direction: str) -> bool:
    if direction == "UP":
        return bar.low >= line_price
    if direction == "DOWN":
        return bar.high <= line_price
    raise ValueError("unsupported direction")


def _reaction_is_away(rule_id: str, touch_price: float, reaction_price: float) -> bool:
    if rule_id == "MURPHY_0006":
        return reaction_price > touch_price
    if rule_id == "MURPHY_0007":
        return reaction_price < touch_price
    raise ValueError("unsupported rule_id")


def evaluate_event_chain(
    rule_id: str,
    line: Line,
    line_price_at: Callable[[datetime], float],
    pivots: Sequence[PivotEvent],
    bars: Sequence[D1Bar],
) -> Optional[Confirmation]:
    expected = {
        "MURPHY_0006": ("LOW", "UP", "HIGH"),
        "MURPHY_0007": ("HIGH", "DOWN", "LOW"),
    }
    if rule_id not in expected:
        return None

    expected_family, expected_direction, reaction_family = expected[rule_id]
    if (line.line_type, line.direction) != (expected_family, expected_direction):
        return None

    ordered = sorted(pivots, key=lambda p: p.available_at)
    eligible = [p for p in ordered if p.available_at >= line.available_at]

    for i, touch in enumerate(eligible):
        if touch.pivot_type != expected_family:
            continue
        touch_line = line_price_at(touch.timestamp)
        touch_bar = next((b for b in bars if b.timestamp == touch.timestamp), None)
        if touch_bar is None or not _range_intersects(touch_bar, touch_line):
            continue

        reaction = next(
            (p for p in eligible[i + 1:]
             if p.pivot_type == reaction_family and p.available_at >= touch.available_at),
            None,
        )
        if reaction is None or not _reaction_is_away(rule_id, touch.price, reaction.price):
            continue

        interval_bars = [b for b in bars if touch.timestamp <= b.timestamp <= reaction.timestamp]
        if not interval_bars:
            continue

        if any(
            b.timestamp != touch.timestamp
            and not _holds_without_break(b, line_price_at(b.timestamp), expected_direction)
            for b in interval_bars
        ):
            continue

        return Confirmation(rule_id, touch, reaction, reaction.available_at)

    return None
