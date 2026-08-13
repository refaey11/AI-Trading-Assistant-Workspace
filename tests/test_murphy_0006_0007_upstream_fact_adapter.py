from src.murphy_0006_0007.evidence_adapter import build_candidate
from src.murphy_0006_0007.upstream_fact_adapter import derive_candidate_facts


def _candidate(*, rule_id, line_type, direction, pivot_type, intersects, reaction):
    if intersects:
        daily_high, daily_low = (1.35, 1.30) if direction == "UP" else (1.10, 1.05)
    else:
        daily_high, daily_low = (1.30, 1.20) if direction == "UP" else (1.30, 1.20)

    return build_candidate(
        rule_id=rule_id,
        line_id="L1",
        line_type=line_type,
        direction=direction,
        anchor_1_timestamp="2024-01-01",
        anchor_1_price=1.20,
        anchor_2_timestamp="2024-01-03",
        anchor_2_price=1.24 if direction == "UP" else 1.16,
        line_availability_timestamp="2024-01-05",
        candidate_timestamp="2024-01-08",
        candidate_pivot_type=pivot_type,
        candidate_pivot_price=1.25,
        daily_high=daily_high,
        daily_low=daily_low,
        reaction_candidate_timestamp="2024-01-10",
        reaction_candidate_type="HIGH" if direction == "UP" else "LOW",
        reaction_directionally_consistent=reaction,
        no_break_observation="OBSERVATION_ONLY",
    )


def test_0006_existing_range_intersection_becomes_touch_candidate():
    facts = derive_candidate_facts(
        _candidate(
            rule_id="MURPHY_0006", line_type="LOW", direction="UP",
            pivot_type="LOW", intersects=True, reaction=True,
        )
    )
    assert facts.third_touch is True
    assert facts.reaction_bounce is True
    assert facts.no_break is None
    assert facts.confirmation_available_timestamp is None
    assert facts.status == "CANDIDATE_FACTS_ONLY"


def test_0007_non_intersection_is_not_touch():
    facts = derive_candidate_facts(
        _candidate(
            rule_id="MURPHY_0007", line_type="HIGH", direction="DOWN",
            pivot_type="HIGH", intersects=False, reaction=True,
        )
    )
    assert facts.third_touch is False
    assert facts.no_break is None


def test_no_break_and_confirmation_time_are_never_fabricated():
    facts = derive_candidate_facts(
        _candidate(
            rule_id="MURPHY_0006", line_type="LOW", direction="UP",
            pivot_type="LOW", intersects=True, reaction=True,
        )
    )
    assert facts.no_break is None
    assert facts.confirmation_available_timestamp is None
