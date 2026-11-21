"""Synthetic semantic oracle for the MTF Pivot Detector V2 contract.

TEST-ONLY: no market-data ingestion, clock authentication, source-ID generation,
parameter selection, persistence, or Decision Brain integration.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Literal, Sequence

PivotKind = Literal["HIGH", "LOW"]
Status = Literal["CONFIRMED", "NOT_PIVOT", "NOT_EVALUABLE", "PENDING"]


@dataclass(frozen=True)
class SyntheticBar:
    source_bar_id: str
    high: float
    low: float
    completed: bool
    available_at: int


@dataclass(frozen=True)
class CandidateResult:
    source_index: int
    kind: PivotKind
    status: Status
    available_at: int | None
    reason: str


def _valid_bar(bar: SyntheticBar) -> bool:
    return (
        isinstance(bar.source_bar_id, str)
        and bool(bar.source_bar_id)
        and isinstance(bar.completed, bool)
        and isinstance(bar.available_at, int)
        and not isinstance(bar.available_at, bool)
        and isfinite(bar.high)
        and isfinite(bar.low)
        and bar.high >= bar.low
    )


def evaluate_candidate(
    bars: Sequence[SyntheticBar],
    index: int,
    left: int,
    right: int,
    *,
    continuity_verified: Sequence[bool],
    precision_verified: bool,
) -> tuple[CandidateResult, CandidateResult]:
    """Evaluate HIGH and LOW independently for one explicit synthetic L/R.

    continuity_verified[j] describes the source-sequence edge j -> j+1.
    False/missing evidence blocks the candidate; this oracle does not infer
    whether a gap is a weekend/session closure.
    """
    if left < 1 or right < 1:
        raise ValueError("L and R must be explicit positive integers")
    if not 0 <= index < len(bars):
        raise IndexError("candidate index outside supplied bars")
    if len(continuity_verified) != max(0, len(bars) - 1):
        raise ValueError("continuity evidence must cover every supplied edge")
    if any(not isinstance(v, bool) for v in continuity_verified):
        raise ValueError("continuity evidence must be explicit booleans")

    def result(kind: PivotKind, status: Status, reason: str,
               available_at: int | None = None) -> CandidateResult:
        return CandidateResult(index, kind, status, available_at, reason)

    start, end = index - left, index + right
    if start < 0:
        return (
            result("HIGH", "PENDING", "INSUFFICIENT_LEFT_CONTEXT"),
            result("LOW", "PENDING", "INSUFFICIENT_LEFT_CONTEXT"),
        )
    if end >= len(bars):
        return (
            result("HIGH", "PENDING", "INCOMPLETE_RIGHT_CONTEXT"),
            result("LOW", "PENDING", "INCOMPLETE_RIGHT_CONTEXT"),
        )

    window = bars[start:end + 1]
    if not all(_valid_bar(bar) and bar.completed for bar in window):
        return (
            result("HIGH", "NOT_EVALUABLE", "INVALID_OR_UNFINISHED_BAR"),
            result("LOW", "NOT_EVALUABLE", "INVALID_OR_UNFINISHED_BAR"),
        )
    if not precision_verified:
        return (
            result("HIGH", "NOT_EVALUABLE", "TRUSTED_PRECISION_MISSING"),
            result("LOW", "NOT_EVALUABLE", "TRUSTED_PRECISION_MISSING"),
        )
    if not all(continuity_verified[start:end]):
        return (
            result("HIGH", "NOT_EVALUABLE", "UNPROVEN_SEQUENCE_GAP"),
            result("LOW", "NOT_EVALUABLE", "UNPROVEN_SEQUENCE_GAP"),
        )

    candidate = bars[index]
    left_bars = bars[start:index]
    right_bars = bars[index + 1:end + 1]
    comparisons = left_bars + right_bars

    high_values = [bar.high for bar in comparisons]
    low_values = [bar.low for bar in comparisons]

    if any(candidate.high == value for value in high_values):
        high = result("HIGH", "NOT_EVALUABLE", "EQUAL_HIGH_PLATEAU")
    elif all(candidate.high > value for value in high_values):
        high = result("HIGH", "CONFIRMED", "STRICT_ISOLATED_HIGH",
                      bars[end].available_at)
    else:
        high = result("HIGH", "NOT_PIVOT", "HIGH_NOT_STRICT_EXTREMUM")

    if any(candidate.low == value for value in low_values):
        low = result("LOW", "NOT_EVALUABLE", "EQUAL_LOW_PLATEAU")
    elif all(candidate.low < value for value in low_values):
        low = result("LOW", "CONFIRMED", "STRICT_ISOLATED_LOW",
                     bars[end].available_at)
    else:
        low = result("LOW", "NOT_PIVOT", "LOW_NOT_STRICT_EXTREMUM")

    return high, low
