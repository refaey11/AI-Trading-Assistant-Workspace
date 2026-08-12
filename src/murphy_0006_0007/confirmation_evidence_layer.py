"""Candidate-only confirmation evidence for Murphy 0006/0007.

This layer consumes existing geometry/pivot/OHLC observations and emits
candidate evidence only. It deliberately does not define a source-unapproved
successful-touch, reaction, or no-break predicate.
"""

from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class ConfirmationEvidence:
    rule_id: str
    line_id: str
    trendline_type: str
    direction: str
    anchor_count: int
    third_touch_candidate: bool
    reaction_candidate: bool
    no_break_observation: Optional[str]
    confirmation_available_timestamp: str
    status: str = "CANDIDATE_ONLY"


def build_confirmation_evidence(
    *,
    rule_id: str,
    line_id: str,
    trendline_type: str,
    direction: str,
    anchor_count: int,
    third_touch_candidate: bool,
    reaction_candidate: bool,
    no_break_observation: Optional[str],
    confirmation_available_timestamp: str,
) -> ConfirmationEvidence:
    expected = {
        "MURPHY_0006": ("LOW", "UP"),
        "MURPHY_0007": ("HIGH", "DOWN"),
    }
    if rule_id not in expected:
        raise ValueError("unsupported Murphy rule")
    if (trendline_type.upper(), direction.upper()) != expected[rule_id]:
        raise ValueError("rule/geometry mapping mismatch")
    if anchor_count < 2:
        raise ValueError("at least two anchors required")
    if not confirmation_available_timestamp:
        raise ValueError("confirmation availability timestamp is required")

    return ConfirmationEvidence(
        rule_id=rule_id,
        line_id=line_id,
        trendline_type=trendline_type.upper(),
        direction=direction.upper(),
        anchor_count=anchor_count,
        third_touch_candidate=bool(third_touch_candidate),
        reaction_candidate=bool(reaction_candidate),
        no_break_observation=no_break_observation,
        confirmation_available_timestamp=confirmation_available_timestamp,
    )


def to_dict(evidence: ConfirmationEvidence) -> Dict[str, Any]:
    return asdict(evidence)
