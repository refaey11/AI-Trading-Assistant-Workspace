from scripts.build_murphy_0006_0007_confirmation_evidence import transform


def row(rule_id, line_type, direction):
    return {
        "rule_id": rule_id,
        "line_id": "L1",
        "line_type": line_type,
        "direction": direction,
        "anchor_1_timestamp": "2024-01-01",
        "anchor_1_price": "1.20",
        "anchor_2_timestamp": "2024-01-03",
        "anchor_2_price": "1.24",
        "line_availability_timestamp": "2024-01-03",
        "candidate_timestamp": "2024-01-08",
        "candidate_pivot_type": line_type,
        "candidate_pivot_price": "1.26",
    }


def test_0006_normalizes_to_candidate_only():
    out = transform([row("MURPHY_0006", "LOW", "UP")])[0]
    assert out["trendline_type"] == "LOW"
    assert out["direction"] == "UP"
    assert out["status"] == "CANDIDATE_ONLY"
    assert out["third_touch_candidate"] == "CANDIDATE_ONLY"
    assert out["reaction_candidate"] == "CANDIDATE_ONLY"
    assert out["no_break_observation"] == "NOT_BOUND"


def test_0007_normalizes_to_candidate_only():
    out = transform([row("MURPHY_0007", "HIGH", "DOWN")])[0]
    assert out["trendline_type"] == "HIGH"
    assert out["direction"] == "DOWN"
    assert out["status"] == "CANDIDATE_ONLY"


def test_mapping_mismatch_is_rejected():
    try:
        transform([row("MURPHY_0006", "HIGH", "DOWN")])
    except ValueError as exc:
        assert "mismatch" in str(exc)
    else:
        raise AssertionError("expected mapping mismatch")
