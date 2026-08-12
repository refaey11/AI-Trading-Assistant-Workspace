from src.murphy_0006_0007.confirmation_evidence_layer import build_confirmation_evidence


def test_0006_candidate_only():
    e = build_confirmation_evidence(
        rule_id="MURPHY_0006", line_id="L6", trendline_type="LOW",
        direction="UP", anchor_count=2, third_touch_candidate=True,
        reaction_candidate=True, no_break_observation="RANGE_HOLD",
        confirmation_available_timestamp="2024-01-10T00:00:00",
    )
    assert e.status == "CANDIDATE_ONLY"
    assert e.rule_id == "MURPHY_0006"


def test_0007_candidate_only():
    e = build_confirmation_evidence(
        rule_id="MURPHY_0007", line_id="L7", trendline_type="HIGH",
        direction="DOWN", anchor_count=2, third_touch_candidate=True,
        reaction_candidate=False, no_break_observation=None,
        confirmation_available_timestamp="2024-02-10T00:00:00",
    )
    assert e.status == "CANDIDATE_ONLY"
    assert e.direction == "DOWN"


def test_mapping_mismatch_rejected():
    try:
        build_confirmation_evidence(
            rule_id="MURPHY_0006", line_id="bad", trendline_type="HIGH",
            direction="DOWN", anchor_count=2, third_touch_candidate=True,
            reaction_candidate=True, no_break_observation=None,
            confirmation_available_timestamp="2024-01-10T00:00:00",
        )
    except ValueError as exc:
        assert "mapping mismatch" in str(exc)
    else:
        raise AssertionError("mapping mismatch must be rejected")


def test_two_anchors_required():
    try:
        build_confirmation_evidence(
            rule_id="MURPHY_0006", line_id="bad", trendline_type="LOW",
            direction="UP", anchor_count=1, third_touch_candidate=False,
            reaction_candidate=False, no_break_observation=None,
            confirmation_available_timestamp="2024-01-10T00:00:00",
        )
    except ValueError as exc:
        assert "two anchors" in str(exc)
    else:
        raise AssertionError("less than two anchors must be rejected")
