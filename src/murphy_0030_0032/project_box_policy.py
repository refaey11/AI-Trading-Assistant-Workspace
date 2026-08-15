"""Project Box Policy V1 for Murphy 0030-0032.

This is a project operationalization, not a verbatim Murphy/Tower formula.
It uses a pre-declared three-calendar-year calibration window and daily
log-return standard deviation to produce a percentage box size.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import log, sqrt
from datetime import date
from typing import Sequence


@dataclass(frozen=True)
class BoxPolicyResult:
    calibration_start: date
    calibration_end: date
    observations: int
    daily_log_return_std: float
    box_pct: float
    status: str


def compute_three_year_box_pct(
    closes: Sequence[float],
    calibration_start: date,
    calibration_end: date,
) -> BoxPolicyResult:
    """Compute the proposed percentage box from a fixed calibration block.

    `closes` must contain only completed daily closes from the declared
    calibration interval, in chronological order. No future evaluation data
    may be passed to this function.
    """
    if len(closes) < 2:
        raise ValueError("at least two closes are required")
    if calibration_end <= calibration_start:
        raise ValueError("calibration_end must be after calibration_start")
    if any(x <= 0 for x in closes):
        raise ValueError("closes must be positive")

    returns = [log(closes[i] / closes[i - 1]) for i in range(1, len(closes))]
    mean = sum(returns) / len(returns)
    variance = sum((r - mean) ** 2 for r in returns) / (len(returns) - 1)
    std = sqrt(variance)
    return BoxPolicyResult(
        calibration_start=calibration_start,
        calibration_end=calibration_end,
        observations=len(returns),
        daily_log_return_std=std,
        box_pct=std * 100.0,
        status="PROPOSAL_PENDING_VALIDATION",
    )
