"""Deterministic, evidence-only MTF structure producer V2.

This module consumes completed bars and already-confirmed pivot events.
It does NOT detect pivots, infer broker clocks, generate trade direction,
or populate legacy trend_regime / mtf_trend_score fields.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Iterable, Literal


PivotKind = Literal["HIGH", "LOW"]
StructureState = Literal[
    "BULLISH_STRUCTURE", "BEARISH_STRUCTURE", "RANGE_OR_MIXED",
    "INSUFFICIENT_PIVOT_HISTORY", "UNAVAILABLE"
]


@dataclass(frozen=True)
class Bar:
    index: int
    open: float
    high: float
    low: float
    close: float
    completed: bool = True


@dataclass(frozen=True)
class ConfirmedPivot:
    pivot_id: str
    kind: PivotKind
    price: float
    source_bar_index: int
    available_bar_index: int
    confirmation_status: str = "CONFIRMED"


@dataclass(frozen=True)
class StructureEvent:
    event_id: str
    event_type: str
    bar_index: int
    boundary_pivot_id: str
    boundary_price: float
    available_bar_index: int


def _validate(bars: list[Bar], pivots: list[ConfirmedPivot]) -> None:
    if not bars:
        raise ValueError("bars must not be empty")
    if [b.index for b in bars] != list(range(bars[0].index, bars[0].index + len(bars))):
        raise ValueError("bar indices must be contiguous and ordered")
    for b in bars:
        if not b.completed:
            raise ValueError("only completed bars are accepted")
        if not (b.low <= min(b.open, b.close) <= max(b.open, b.close) <= b.high):
            raise ValueError(f"invalid OHLC envelope at bar {b.index}")
    ids = [p.pivot_id for p in pivots]
    if len(ids) != len(set(ids)):
        raise ValueError("pivot_id values must be unique")
    bar_min, bar_max = bars[0].index, bars[-1].index
    for p in pivots:
        if p.kind not in ("HIGH", "LOW") or p.confirmation_status != "CONFIRMED":
            raise ValueError("only explicitly confirmed HIGH/LOW pivots are accepted")
        if p.available_bar_index < p.source_bar_index + 2:
            raise ValueError("pivot availability violates the declared two-bar confirmation delay")
        if p.available_bar_index < bar_min or p.available_bar_index > bar_max:
            raise ValueError("pivot availability must fall within supplied bar range")
        if p.source_bar_index > p.available_bar_index:
            raise ValueError("pivot source bar cannot follow availability")


def _state(available: list[ConfirmedPivot]) -> str:
    highs = sorted((p for p in available if p.kind == "HIGH"),
                   key=lambda p: (p.available_bar_index, p.source_bar_index, p.pivot_id))
    lows = sorted((p for p in available if p.kind == "LOW"),
                  key=lambda p: (p.available_bar_index, p.source_bar_index, p.pivot_id))
    if len(highs) < 2 or len(lows) < 2:
        return "INSUFFICIENT_PIVOT_HISTORY"
    h1, h2 = highs[-2], highs[-1]
    l1, l2 = lows[-2], lows[-1]
    if h2.price > h1.price and l2.price > l1.price:
        return "BULLISH_STRUCTURE"
    if h2.price < h1.price and l2.price < l1.price:
        return "BEARISH_STRUCTURE"
    return "RANGE_OR_MIXED"


def produce_structure_v2(
    bars: Iterable[Bar], pivots: Iterable[ConfirmedPivot], *,
    symbol: str, timeframe: str, producer_version: str = "2.0.0",
    schema_version: str = "mtf_v2.structure.v1",
    source_payload_hash: str = "UNSET",
    clock_policy_id: str = "UNVERIFIED",
) -> dict:
    """Return per-bar evidence. Bar indices are source-TF sequence positions.

    A pivot is usable for state only at/after available_bar_index. For a break
    event, the boundary pivot must have been available strictly before the
    break bar. This strict ordering prevents same-bar confirmation leakage.
    """
    bars, pivots = list(bars), list(pivots)
    _validate(bars, pivots)
    if not symbol or not timeframe:
        raise ValueError("symbol and timeframe are required")
    rows, events = [], []
    prior_state = "INSUFFICIENT_PIVOT_HISTORY"
    previous_close = None
    for bar in bars:
        before = [p for p in pivots if p.available_bar_index < bar.index]
        state_pivots = [p for p in pivots if p.available_bar_index <= bar.index]
        before_highs = sorted((p for p in before if p.kind == "HIGH"),
                              key=lambda p: (p.available_bar_index, p.source_bar_index, p.pivot_id))
        before_lows = sorted((p for p in before if p.kind == "LOW"),
                             key=lambda p: (p.available_bar_index, p.source_bar_index, p.pivot_id))
        event = None
        if prior_state == "BULLISH_STRUCTURE" and before_lows and previous_close is not None and previous_close >= before_lows[-1].price and bar.close < before_lows[-1].price:
            event = ("CHOCH_DOWN", before_lows[-1])
        elif prior_state == "BEARISH_STRUCTURE" and before_highs and previous_close is not None and previous_close <= before_highs[-1].price and bar.close > before_highs[-1].price:
            event = ("CHOCH_UP", before_highs[-1])
        elif prior_state == "BULLISH_STRUCTURE" and before_highs and previous_close is not None and previous_close <= before_highs[-1].price and bar.close > before_highs[-1].price:
            event = ("BOS_UP", before_highs[-1])
        elif prior_state == "BEARISH_STRUCTURE" and before_lows and previous_close is not None and previous_close >= before_lows[-1].price and bar.close < before_lows[-1].price:
            event = ("BOS_DOWN", before_lows[-1])
        if event:
            kind, pivot = event
            ev = StructureEvent(
                event_id=f"{symbol}:{timeframe}:{kind}:{bar.index}:{pivot.pivot_id}",
                event_type=kind, bar_index=bar.index,
                boundary_pivot_id=pivot.pivot_id, boundary_price=pivot.price,
                available_bar_index=bar.index,
            )
            events.append(asdict(ev))
        current_state = _state(state_pivots)
        rows.append({
            "symbol": symbol, "timeframe": timeframe, "bar_index": bar.index,
            "structure_state": current_state,
            "available_pivot_ids": [p.pivot_id for p in state_pivots],
            "event": events[-1] if event and events else None,
            "producer_version": producer_version, "schema_version": schema_version,
            "source_payload_hash": source_payload_hash,
            "clock_policy_id": clock_policy_id,
            "availability_status": "PROVENANCE_UNVALIDATED",
        })
        prior_state = current_state
        previous_close = bar.close
    return {
        "symbol": symbol, "timeframe": timeframe, "producer_version": producer_version,
        "schema_version": schema_version, "source_payload_hash": source_payload_hash,
        "clock_policy_id": clock_policy_id, "rows": rows, "events": events,
        "legacy_fields_written": False, "direction_generated": False,
    }


def aggregate_mtf_context(states_by_timeframe: dict[str, str]) -> dict:
    """Categorical conflict summary; no voting, weighting, or directional score."""
    values = list(states_by_timeframe.values())
    bullish = any(v == "BULLISH_STRUCTURE" for v in values)
    bearish = any(v == "BEARISH_STRUCTURE" for v in values)
    if bullish and bearish:
        status = "CONFLICTED"
    elif bullish:
        status = "CONSISTENT_BULLISH_STRUCTURE"
    elif bearish:
        status = "CONSISTENT_BEARISH_STRUCTURE"
    else:
        status = "INSUFFICIENT_OR_MIXED_EVIDENCE"
    return {"status": status, "timeframe_states": dict(states_by_timeframe),
            "directional_score": None, "majority_vote_used": False}
