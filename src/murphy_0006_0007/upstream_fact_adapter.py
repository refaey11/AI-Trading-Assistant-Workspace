"""Conservative adapter from existing candidate evidence to upstream facts.

This module does not invent a touch tolerance, reaction magnitude, break
threshold, lookback, or timeframe. It only promotes already-recorded
observations into explicit candidate facts. Production confirmation remains
blocked until an approved no-break operator exists.
"""

from dataclasses import dataclass
from typing import Optional

from .evidence_adapter import EvidenceCandidate


@dataclass(frozen=True)
class UpstreamFacts:
    rule_id: str
    line_id: str
    third_touch: Optional[bool]
    reaction_bounce: Optional[bool]
    no_break: Optional[bool]
    confirmation_available_timestamp: Optional[str]
    status: str = "CANDIDATE_FACTS_ONLY"


def derive_candidate_facts(candidate: EvidenceCandidate) -> UpstreamFacts:
    """Promote only existing observations; never infer a production break rule.

    Third-touch candidate requires the existing same-family pivot observation
    plus daily-range/line intersection. Reaction candidate requires the
    existing directional-consistency observation. No-break and the successful
    confirmation availability timestamp are intentionally left unknown because
    the project has no approved 0006/0007 production predicates for them.
    """
    same_family = candidate.candidate_pivot_type.upper() == candidate.line_type.upper()

    if candidate.daily_range_intersects_line is None:
        third_touch: Optional[bool] = None
    else:
        third_touch = bool(same_family and candidate.daily_range_intersects_line)

    reaction_bounce = candidate.reaction_directionally_consistent

    return UpstreamFacts(
        rule_id=candidate.rule_id,
        line_id=candidate.line_id,
        third_touch=third_touch,
        reaction_bounce=reaction_bounce,
        no_break=None,
        confirmation_available_timestamp=None,
    )
