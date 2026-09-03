from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Event:
    timestamp: datetime
    price: float
    kind: str


@dataclass(frozen=True)
class Confirmation:
    rule_id: str
    third_touch: Event
    reaction: Event
    confirmation_available_at: datetime
    no_break_valid: bool = True


def _parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def build_confirmation(
    *,
    rule_id: str,
    line_type: str,
    direction: str,
    third_touch_timestamp: str,
    third_touch_price: float,
    reaction_timestamp: str,
    reaction_price: float,
    confirmation_available_at: str,
    no_break_valid: bool,
) -> Optional[Confirmation]:
    expected = {
        "MURPHY_0006": ("LOW", "UP"),
        "MURPHY_0007": ("HIGH", "DOWN"),
    }.get(rule_id)
    if expected is None or (line_type, direction) != expected:
        return None
    if not no_break_valid:
        return None
    third = Event(_parse_ts(third_touch_timestamp), float(third_touch_price), line_type)
    reaction_kind = "HIGH" if rule_id == "MURPHY_0006" else "LOW"
    reaction = Event(_parse_ts(reaction_timestamp), float(reaction_price), reaction_kind)
    available = _parse_ts(confirmation_available_at)
    if not (third.timestamp < reaction.timestamp <= available):
        return None
    return Confirmation(
        rule_id=rule_id,
        third_touch=third,
        reaction=reaction,
        confirmation_available_at=available,
        no_break_valid=True,
    )
