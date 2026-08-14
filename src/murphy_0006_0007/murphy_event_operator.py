from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Sequence, Optional, Callable

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

    # Market events are ordered by event timestamp. Availability is only an
    # eligibility/no-lookahead gate.
    ordered = sorted(pivots, key=lambda p: p.timestamp)
    eligible = [
        p for p in ordered
        if p.timestamp >= line.available_at and p.available_at >= line.available_at
    ]

    # The first eligible same-family pivot is the only third-touch candidate.
    # If it fails the touch test, do not skip it and manufacture a later touch.
    touch = next((p for p in eligible if p.pivot_type == expected_family), None)
    if touch is None:
        return None

    touch_line = line_price_at(touch.timestamp)
    touch_bar = next((b for b in bars if b.timestamp == touch.timestamp), None)
    if touch_bar is None or not _range_intersects(touch_bar, touch_line):
        return None

    # Reaction is the next opposite-family event strictly after the touch.
    reaction = next(
        (
            p for p in eligible
            if p.pivot_type == reaction_family
            and p.timestamp > touch.timestamp
            and p.available_at >= touch.available_at
        ),
        None,
    )
    if reaction is None or not _reaction_is_away(rule_id, touch.price, reaction.price):
        return None

    interval_bars = [b for b in bars if touch.timestamp <= b.timestamp <= reaction.timestamp]
    if not interval_bars:
        return None

    for bar in interval_bars:
        lp = line_price_at(bar.timestamp)
        if bar.timestamp == touch.timestamp:
            continue
        if not _holds_without_break(bar, lp, expected_direction):
            return None

    return Confirmation(rule_id, touch, reaction, reaction.available_at)
