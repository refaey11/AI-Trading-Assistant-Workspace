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


def test_tiz_process_fail_does_not_block_brain_assessment():
    out = run(MARKET_ROW, {"alignment_state":"PROCESS_BLOCKED","process_gate":"FAIL"})
    assert out["status"] == "ASSESSED"
    assert out["assessment"] is not None
    assert out["gates"]["tiz_decision_authority"] is False


def test_nison_contradiction_reviews_before_brain():
    out = run(MARKET_ROW, {"alignment_state":"ALIGNED","process_gate":"PASS","contradiction_gate":"CONTRADICTION"})
    assert out["status"] == "REVIEW"
    assert out["assessment"] is None


def test_aligned_evidence_reaches_assessment_without_trade_command():
    out = run(MARKET_ROW, {"alignment_state":"ALIGNED","process_gate":"PASS","contradiction_gate":"PASS","candidate_direction":"BULLISH"})
    assert out["status"] == "ASSESSED"
    assert out["assessment"].directional_bias in {"bullish","bearish","neutral","conflicted"}
    assert out["knowledge_evidence"]["final_trade_decision"] is None


def test_similarity_cannot_restore_tiz_gate_or_create_direction():
    out = run(MARKET_ROW, {"alignment_state":"PROCESS_BLOCKED","process_gate":"FAIL"}, {"predicted_return":0.99})
    assert out["status"] == "ASSESSED"
    assert out["assessment"] is not None
    assert out["knowledge_evidence"]["final_trade_decision"] is None


def test_similarity_is_directionally_inert_on_aligned_path():
    neutral_row = {
        "mtf_trend_score": 0.0,
        "M5_trend_regime": 0.0,
        "M15_trend_regime": 0.0,
        "M30_trend_regime": 0.0,
        "H1_trend_regime": 0.0,
        "H4_trend_regime": 0.0,
        "D1_trend_regime": 0.0,
        "volume_available": True,
        "M5_volume_regime": 0.0,
    }
    alignment = {"alignment_state":"ALIGNED","contradiction_gate":"PASS"}
    no_memory = run(neutral_row, alignment, None)
    bullish_memory = run(neutral_row, alignment, {"predicted_return":0.99, "direction":"BULLISH"})
    bearish_memory = run(neutral_row, alignment, {"predicted_return":-0.99, "direction":"BEARISH"})

    assert no_memory["status"] == bullish_memory["status"] == bearish_memory["status"] == "ASSESSED"
    assert no_memory["assessment"].directional_bias == "neutral"
    assert bullish_memory["assessment"].directional_bias == no_memory["assessment"].directional_bias
    assert bearish_memory["assessment"].directional_bias == no_memory["assessment"].directional_bias
    assert bullish_memory["assessment"].confidence == no_memory["assessment"].confidence
    assert bearish_memory["assessment"].confidence == no_memory["assessment"].confidence
    assert bullish_memory["knowledge_evidence"]["evidence_bundle"]["similarity"]["predicted_return"] == 0.99
    assert bearish_memory["knowledge_evidence"]["evidence_bundle"]["similarity"]["predicted_return"] == -0.99
