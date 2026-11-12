from compatibility.knowledge_decision_handoff import build_handoff

BASE = {"mtf_trend_score": 0.6, "volume_available": True}


def test_aligned_passes_to_assessment_without_trade_command():
    out = build_handoff(BASE, {
        "alignment_state": "ALIGNED",
        "candidate_direction": "bullish",
        "contradiction_gate": "PASS",
        "process_gate": "PASS",
    })
    assert out["routing"] == "ASSESS"
    assert out["gates"]["hard_block"] is False
    assert out["knowledge_evidence"]["final_trade_decision"] is None


def test_nison_contradiction_routes_to_review():
    out = build_handoff(BASE, {
        "alignment_state": "NISON_CONTRADICTION",
        "candidate_direction": "bullish",
        "contradiction_gate": "CONTRADICTION",
        "process_gate": "PASS",
    })
    assert out["routing"] == "REVIEW"
    assert out["gates"]["contradiction"] is True
    assert out["gates"]["abstain"] is True


def test_tiz_process_fail_does_not_block_assessment():
    out = build_handoff(BASE, {
        "alignment_state": "PROCESS_BLOCKED",
        "process_gate": "FAIL",
    })
    assert out["routing"] == "ASSESS"
    assert out["gates"]["hard_block"] is False
    assert out["gates"]["tiz_decision_authority"] is False
    assert out["knowledge_evidence"]["process_gate"] == "FAIL"


def test_similarity_does_not_change_routing_or_create_trade_command():
    out = build_handoff(BASE, {
        "alignment_state": "PROCESS_BLOCKED",
        "process_gate": "FAIL",
    }, similarity={"predicted_return": 0.99})
    assert out["routing"] == "ASSESS"
    assert out["gates"]["hard_block"] is False
    assert out["knowledge_evidence"]["final_trade_decision"] is None
