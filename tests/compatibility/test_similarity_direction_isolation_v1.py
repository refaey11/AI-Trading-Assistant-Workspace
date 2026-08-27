"""Regression tests proving Similarity memory cannot create or override direction."""
from compatibility.decision_brain_v1_handoff_adapter import assess_with_governance
import decision_brain


def _row():
    return {
        "mtf_trend_score": 1.0,
        "M5_trend_regime": 1.0,
        "M15_trend_regime": 1.0,
        "M30_trend_regime": 1.0,
        "H1_trend_regime": 1.0,
        "H4_trend_regime": 1.0,
        "D1_trend_regime": 1.0,
        "volume_available": True,
        "M5_volume_regime": 1.0,
        "M15_volume_regime": 1.0,
        "M30_volume_regime": 1.0,
        "H1_volume_regime": 1.0,
        "H4_volume_regime": 1.0,
        "D1_volume_regime": 1.0,
    }


def test_similarity_payload_cannot_reach_directional_engine():
    base = assess_with_governance(
        decision_brain,
        row=_row(),
        query_as_of="2024-12-31T00:00:00Z",
        historical_evidence={
            "retrieval_status": "PASS",
            "candidate_count": 2,
            "predicted_return": -0.50,
        },
    )

    hostile = assess_with_governance(
        decision_brain,
        row=_row(),
        query_as_of="2024-12-31T00:00:00Z",
        historical_evidence={
            "retrieval_status": "PASS",
            "candidate_count": 2,
            "predicted_return": -0.50,
            "similarity_predicted_return": -0.99,
            "direction": "bearish",
        },
    )

    assert base["status"] == "PASS"
    assert hostile["status"] == "PASS"
    assert base["assessment"]["directional_bias"] == hostile["assessment"]["directional_bias"]
    assert base["assessment"]["confidence"] == hostile["assessment"]["confidence"]
    assert hostile["governance"]["similarity_generated_direction"] is False
    assert hostile["governance"]["predicted_return_used_as_direction"] is False


def test_historical_payload_is_sanitized_before_handoff():
    result = assess_with_governance(
        decision_brain,
        row=_row(),
        query_as_of="2024-12-31T00:00:00Z",
        historical_evidence={
            "candidate_count": 3,
            "predicted_return": 0.75,
            "similarity_predicted_return": 0.90,
            "context_evidence": {"foo": "bar"},
        },
    )

    historical = result["historical_evidence"]
    assert historical["candidate_count"] == 3
    assert historical["predicted_return_used_as_direction"] is False
    assert "predicted_return" not in historical
    assert "similarity_predicted_return" not in historical
