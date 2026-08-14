from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Optional, Sequence


@dataclass(frozen=True)
class PivotEvent:
    timestamp: datetime
    available_at: datetime
    pivot_type: str  # LOW/HIGH
    price: float


@dataclass(frozen=True)
class D1Bar:
    timestamp: datetime
    high: float
    low: float


@dataclass(frozen=True)
class Line:
    line_type: str  # LOW/HIGH
    direction: str  # UP/DOWN
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
    """Candidate operationalization for Murphy 0006/0007.

    This layer deliberately does not invent ATR, pip, percentage, lookback,
    3%, or 2-day thresholds. Market chronology uses pivot timestamps;
    availability is used only as the no-lookahead eligibility gate.
    """
    expected = {
        "MURPHY_0006": ("LOW", "UP", "HIGH"),
        "MURPHY_0007": ("HIGH", "DOWN", "LOW"),
    }
    if rule_id not in expected:
        return None

    expected_family, expected_direction, reaction_family = expected[rule_id]
    if (line.line_type, line.direction) != (expected_family, expected_direction):
        return None

    # Market chronology is event timestamp. Availability is a separate gate.
    ordered = sorted(pivots, key=lambda p: p.timestamp)
    eligible = [
        p for p in ordered
        if p.timestamp >= line.available_at
        and p.available_at >= line.available_at
    ]

    # The first eligible same-family pivot is the only third-touch candidate.
    touch_candidates = [p for p in eligible if p.pivot_type == expected_family]
    if not touch_candidates:
        return None
    touch = touch_candidates[0]

    touch_line = line_price_at(touch.timestamp)
    touch_bar = next((b for b in bars if b.timestamp == touch.timestamp), None)
    if touch_bar is None or not _range_intersects(touch_bar, touch_line):
        return None

    # Reaction must be a distinct later market event. Using >= here admits
    # same-timestamp touch/reaction pairs and breaks the canonical 2016-2024
    # reconciliation (15 = 8 for 0006 + 7 for 0007).
    reaction = next(
        (
            p for p in eligible
            if p.pivot_type == reaction_family
            and p.timestamp > touch.timestamp
            and p.available_at >= touch.available_at
        ),
        None,
    )
    if reaction is None:
        return None
    if not _reaction_is_away(rule_id, touch.price, reaction.price):
        return None

    interval_bars = [
        b for b in bars
        if touch.timestamp <= b.timestamp <= reaction.timestamp
    ]
    if not interval_bars:
        return None

    for b in interval_bars:
        if b.timestamp == touch.timestamp:
            # The touch bar is allowed to intersect the line by definition.
            continue
        lp = line_price_at(b.timestamp)
        if not _holds_without_break(b, lp, expected_direction):
            return None

    return Confirmation(
        rule_id=rule_id,
        third_touch=touch,
        reaction=reaction,
        confirmation_available_at=reaction.available_at,
    )
