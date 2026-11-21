"""Synthetic-only reference oracle for approved MTF V2 event lifecycle policy.

Isolated from the structure producer and Decision Brain. Consumes synthetic
closes and already-confirmed synthetic pivots; authenticates no provenance.
"""
from dataclasses import dataclass
from typing import Literal, Iterable


@dataclass(frozen=True)
class SyntheticPivot:
    pivot_id: str
    kind: Literal["HIGH", "LOW"]
    price: float
    source_index: int
    available_index: int


@dataclass(frozen=True)
class SyntheticEvent:
    event_id: str
    pivot_id: str
    direction: Literal["UP", "DOWN"]
    bar_index: int
    boundary_price: float


def evaluate_event_lifecycle(
    closes: Iterable[float],
    pivots: Iterable[SyntheticPivot],
    *,
    start_index: int = 0,
) -> list[SyntheticEvent]:
    """Apply re-arm, no-age-expiry, and latest-same-kind supersession rules.

    Pivots become eligible strictly after available_index. HIGH boundaries
    generate UP crossings; LOW boundaries generate DOWN crossings. Only close
    values are consumed, so wick-only movement cannot create an event.
    """
    closes = list(closes)
    pivots = list(pivots)
    if not closes:
        return []
    if isinstance(start_index, bool) or not isinstance(start_index, int):
        raise ValueError("start_index must be an integer")
    if len({p.pivot_id for p in pivots}) != len(pivots):
        raise ValueError("synthetic pivot IDs must be unique")
    for p in pivots:
        if p.kind not in ("HIGH", "LOW"):
            raise ValueError("pivot kind must be HIGH or LOW")
        if not isinstance(p.price, (int, float)) or isinstance(p.price, bool):
            raise ValueError("pivot price must be numeric and not boolean")
        if p.source_index > p.available_index:
            raise ValueError("pivot source cannot follow its availability")
    if any(not isinstance(c, (int, float)) or isinstance(c, bool) for c in closes):
        raise ValueError("closes must be numeric and not boolean")

    ordered = sorted(pivots, key=lambda p: (p.available_index, p.source_index, p.pivot_id))
    cursor = 0
    active: dict[str, SyntheticPivot] = {}
    armed: dict[str, bool] = {}
    events: list[SyntheticEvent] = []
    previous_close = None

    for offset, close in enumerate(closes):
        bar_index = start_index + offset
        while cursor < len(ordered) and ordered[cursor].available_index < bar_index:
            pivot = ordered[cursor]
            active[pivot.kind] = pivot
            armed[pivot.pivot_id] = True
            cursor += 1

        for kind, direction in (("HIGH", "UP"), ("LOW", "DOWN")):
            pivot = active.get(kind)
            if pivot is None:
                continue
            if kind == "HIGH":
                pre_break_side = close <= pivot.price
                crossed = previous_close is not None and previous_close <= pivot.price and close > pivot.price
            else:
                pre_break_side = close >= pivot.price
                crossed = previous_close is not None and previous_close >= pivot.price and close < pivot.price

            if pre_break_side:
                armed[pivot.pivot_id] = True
            elif crossed and armed.get(pivot.pivot_id, True):
                events.append(SyntheticEvent(
                    event_id=f"synthetic:{pivot.pivot_id}:{direction}:{bar_index}",
                    pivot_id=pivot.pivot_id,
                    direction=direction,
                    bar_index=bar_index,
                    boundary_price=pivot.price,
                ))
                armed[pivot.pivot_id] = False
        previous_close = close

    return events
