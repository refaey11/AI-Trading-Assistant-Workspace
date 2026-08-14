from src.murphy_0006_0007.evidence_adapter import build_candidate, line_price


def test_line_price_is_geometry_only():
    value = line_price("2024-01-01", 1.20, "2024-01-03", 1.24, "2024-01-02")
    assert abs(value - 1.22) < 1e-12


def test_0006_low_up_candidate_never_returns_pass_fail():
    c = build_candidate(
        rule_id="MURPHY_0006",
        line_id="L1",
        line_type="LOW",
        direction="UP",
        anchor_1_timestamp="2024-01-01",
        anchor_1_price=1.20,
        anchor_2_timestamp="2024-01-03",
        anchor_2_price=1.22,
        line_availability_timestamp="2024-01-05",
        candidate_timestamp="2024-01-06",
        candidate_pivot_type="LOW",
        candidate_pivot_price=1.26,
        daily_high=1.28,
        daily_low=1.25,
    )
    assert c.evidence_status == "CANDIDATE_ONLY"
    assert c.daily_range_intersects_line is True


def test_0007_high_down_candidate():
    c = build_candidate(
        rule_id="MURPHY_0007",
        line_id="L2",
        line_type="HIGH",
        direction="DOWN",
        anchor_1_timestamp="2024-02-01",
        anchor_1_price=1.30,
        anchor_2_timestamp="2024-02-03",
        anchor_2_price=1.26,
        line_availability_timestamp="2024-02-05",
        candidate_timestamp="2024-02-08",
        candidate_pivot_type="HIGH",
        candidate_pivot_price=1.22,
        daily_high=1.24,
        daily_low=1.20,
    )
    assert c.evidence_status == "CANDIDATE_ONLY"
    assert c.rule_id == "MURPHY_0007"


def test_rule_family_mismatch_is_rejected():
    try:
        build_candidate(
            rule_id="MURPHY_0006",
            line_id="bad",
            line_type="HIGH",
            direction="DOWN",
            anchor_1_timestamp="2024-01-01",
            anchor_1_price=1.2,
            anchor_2_timestamp="2024-01-03",
            anchor_2_price=1.1,
            line_availability_timestamp="2024-01-04",
            candidate_timestamp="2024-01-05",
            candidate_pivot_type="HIGH",
            candidate_pivot_price=1.05,
            daily_high=1.06,
            daily_low=1.04,
        )
    except ValueError:
        return
    raise AssertionError("rule/line family mismatch must be rejected")
