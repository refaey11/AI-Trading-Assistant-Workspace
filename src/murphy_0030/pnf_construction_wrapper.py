"""Murphy 0030 construction boundary.

This module is intentionally independent of the external P&F engine.
It resolves the D1 High/Low construction policy and freezes one box size
per input bar before any engine call. It does not make trading decisions.
"""
from dataclasses import dataclass
from typing import Literal, Optional

ColumnType = Literal["X", "O"]


@dataclass(frozen=True)
class PnFState:
    column: Optional[ColumnType]
    high: Optional[float]
    low: Optional[float]


@dataclass(frozen=True)
class ConstructionDecision:
    box_size: float
    price: float
    action: Literal["continue", "reverse", "none"]
    target_column: Optional[ColumnType]


def decide_high_low(
    *,
    high: float,
    low: float,
    state: PnFState,
    box_size: float,
    reversal_boxes: int = 3,
) -> ConstructionDecision:
    """Apply the project D1 High/Low priority policy deterministically.

    X column: High continuation is considered first; only if it does not
    continue is Low evaluated for reversal.
    O column: Low continuation is considered first; only if it does not
    continue is High evaluated for reversal.

    The function never claims to know the intraday order of High and Low.
    """
    if box_size <= 0:
        raise ValueError("box_size must be positive")
    if high < low:
        raise ValueError("high must be >= low")

    if state.column == "X" and state.high is not None:
        if high > state.high:
            return ConstructionDecision(box_size, high, "continue", "X")
        reversal_level = state.high - reversal_boxes * box_size
        if low <= reversal_level:
            return ConstructionDecision(box_size, low, "reverse", "O")
        return ConstructionDecision(box_size, low, "none", None)

    if state.column == "O" and state.low is not None:
        if low < state.low:
            return ConstructionDecision(box_size, low, "continue", "O")
        reversal_level = state.low + reversal_boxes * box_size
        if high >= reversal_level:
            return ConstructionDecision(box_size, high, "reverse", "X")
        return ConstructionDecision(box_size, high, "none", None)

    # Initial state: the caller/engine owns initial-column initialization.
    return ConstructionDecision(box_size, high, "none", None)


def freeze_box_size(price_reference: float, box_pct: float) -> float:
    """Compute one bar-level percentage box and return the frozen value."""
    if price_reference <= 0 or box_pct <= 0:
        raise ValueError("price_reference and box_pct must be positive")
    return price_reference * box_pct / 100.0
