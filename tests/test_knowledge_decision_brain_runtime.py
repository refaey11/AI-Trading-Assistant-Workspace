from compatibility.run_knowledge_decision_brain import run

MARKET_ROW = {
    "mtf_trend_score": 0.8,
    "M5_trend_regime": 1,
    "M15_trend_regime": 1,
    "M30_trend_regime": 1,
    "H1_trend_regime": 1,
    "H4_trend_regime": 1,
    "D1_trend_regime": 1,
    "volume_available": True,
    "M5_volume_regime": 0.5,
}

def test_process_fail_blocks_before_brain():
    out = run(MARKET_ROW, {"alignment_state":"ALIGNED","process_gate":"FAIL"})
    assert out["status"] == "BLOCK"
    assert out["assessment"] is None

def test_nison_contradiction_reviews_before_brain():
    out = run(MARKET_ROW, {"alignment_state":"ALIGNED","process_gate":"PASS","contradiction_gate":"CONTRADICTION"})
    assert out["status"] == "REVIEW"
    assert out["assessment"] is None

def test_aligned_evidence_reaches_assessment_without_trade_command():
    out = run(MARKET_ROW, {"alignment_state":"ALIGNED","process_gate":"PASS","contradiction_gate":"PASS","candidate_direction":"BULLISH"})
    assert out["status"] == "ASSESSED"
    assert out["assessment"].directional_bias in {"bullish","bearish","neutral","conflicted"}
    assert out["knowledge_evidence"]["final_trade_decision"] is None

def test_similarity_cannot_override_process_block():
    out = run(MARKET_ROW, {"alignment_state":"PROCESS_BLOCKED","process_gate":"FAIL"}, {"predicted_return":0.99})
    assert out["status"] == "BLOCK"
    assert out["assessment"] is None
