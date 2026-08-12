"""Source-safe evidence adapter for Murphy 0006/0007.

This module intentionally produces candidate evidence only. It does not
implement a successful-touch, reaction, or no-break PASS/FAIL predicate.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class EvidenceCandidate:
    rule_id: str
    line_id: str
    line_type: str
    direction: str
    anchor_1_timestamp: str
    anchor_1_price: float
    anchor_2_timestamp: str
    anchor_2_price: float
    line_availability_timestamp: str
    candidate_timestamp: str
    candidate_pivot_type: str
    candidate_pivot_price: float
    line_price_at_candidate: Optional[float]
    signed_distance: Optional[float]
    absolute_distance: Optional[float]
    daily_high: Optional[float]
    daily_low: Optional[float]
    daily_range_intersects_line: Optional[bool]
    reaction_candidate_timestamp: Optional[str]
    reaction_candidate_type: Optional[str]
    reaction_directionally_consistent: Optional[bool]
    no_break_observation: Optional[str]
    evidence_status: str = "CANDIDATE_ONLY"


def line_price(anchor_1_timestamp: str, anchor_1_price: float,
               anchor_2_timestamp: str, anchor_2_price: float,
               timestamp: str) -> float:
    """Calculate the mathematical line value at `timestamp`.

    Timestamps must be ISO-8601 dates/times. This is geometry only; it does
    not decide whether the price touched the line.
    """
    t1 = datetime.fromisoformat(anchor_1_timestamp).timestamp()
    t2 = datetime.fromisoformat(anchor_2_timestamp).timestamp()
    tx = datetime.fromisoformat(timestamp).timestamp()
    if t2 == t1:
        raise ValueError("anchor timestamps must differ")
    slope = (anchor_2_price - anchor_1_price) / (t2 - t1)
    return anchor_1_price + slope * (tx - t1)


def build_candidate(*, rule_id: str, line_id: str, line_type: str,
                    direction: str, anchor_1_timestamp: str,
                    anchor_1_price: float, anchor_2_timestamp: str,
                    anchor_2_price: float, line_availability_timestamp: str,
                    candidate_timestamp: str, candidate_pivot_type: str,
                    candidate_pivot_price: float, daily_high: Optional[float],
                    daily_low: Optional[float],
                    reaction_candidate_timestamp: Optional[str] = None,
                    reaction_candidate_type: Optional[str] = None,
                    reaction_directionally_consistent: Optional[bool] = None,
                    no_break_observation: Optional[str] = None) -> EvidenceCandidate:
    """Create candidate evidence without applying any touch threshold."""
    if rule_id not in {"MURPHY_0006", "MURPHY_0007"}:
        raise ValueError("unsupported Murphy rule")
    if line_type not in {"LOW", "HIGH"} or direction not in {"UP", "DOWN"}:
        raise ValueError("unsupported line family")
    expected = {"MURPHY_0006": ("LOW", "UP"),
                "MURPHY_0007": ("HIGH", "DOWN")}[rule_id]
    if (line_type, direction) != expected:
        raise ValueError("rule/line family mismatch")

    lp = line_price(anchor_1_timestamp, anchor_1_price,
                    anchor_2_timestamp, anchor_2_price, candidate_timestamp)
    signed = candidate_pivot_price - lp
    absolute = abs(signed)
    intersects = None
    if daily_high is not None and daily_low is not None:
        lo, hi = sorted((daily_low, daily_high))
        intersects = lo <= lp <= hi

    return EvidenceCandidate(
        rule_id=rule_id,
        line_id=line_id,
        line_type=line_type,
        direction=direction,
        anchor_1_timestamp=anchor_1_timestamp,
        anchor_1_price=anchor_1_price,
        anchor_2_timestamp=anchor_2_timestamp,
        anchor_2_price=anchor_2_price,
        line_availability_timestamp=line_availability_timestamp,
        candidate_timestamp=candidate_timestamp,
        candidate_pivot_type=candidate_pivot_type,
        candidate_pivot_price=candidate_pivot_price,
        line_price_at_candidate=lp,
        signed_distance=signed,
        absolute_distance=absolute,
        daily_high=daily_high,
        daily_low=daily_low,
        daily_range_intersects_line=intersects,
        reaction_candidate_timestamp=reaction_candidate_timestamp,
        reaction_candidate_type=reaction_candidate_type,
        reaction_directionally_consistent=reaction_directionally_consistent,
        no_break_observation=no_break_observation,
    )


def to_dict(candidate: EvidenceCandidate) -> Dict[str, Any]:
    return asdict(candidate)
