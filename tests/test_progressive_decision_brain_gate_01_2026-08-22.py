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


def test_gate01_aligned_murphy_plus_nison_reaches_brain_without_trade_command():
    out = run(
        MARKET_ROW,
        {
            "alignment_state": "ALIGNED",
            "candidate_direction": "BULLISH",
            "contradiction_gate": "PASS",
            "process_gate": "PASS",
            "book_evidence_status": "OK",
            "market_evidence_status": "OK",
        },
    )
    assert out["status"] == "ASSESSED"
    assert out["assessment"] is not None
    assert out["knowledge_evidence"]["candidate_direction"] == "BULLISH"
    assert out["knowledge_evidence"]["final_trade_decision"] is None


def test_gate01_nison_contradiction_survives_handoff():
    out = run(
        MARKET_ROW,
        {
            "alignment_state": "NISON_CONTRADICTION",
            "candidate_direction": "BULLISH",
            "contradiction_gate": "CONTRADICTION",
            "process_gate": "PASS",
        },
    )
    assert out["status"] == "REVIEW"
    assert out["assessment"] is None
    assert out["gates"]["contradiction"] is True
    assert out["gates"]["abstain"] is True


def test_gate01_nison_alone_cannot_create_direction():
    out = run(
        MARKET_ROW,
        {
            "alignment_state": "NEEDS_REVIEW",
            "candidate_direction": "BULLISH",
            "contradiction_gate": "PASS",
            "process_gate": "PASS",
            "book_evidence_status": "INSUFFICIENT",
        },
    )
    assert out["status"] == "REVIEW"
    assert out["assessment"] is None
    assert out["gates"]["abstain"] is True


def test_gate01_process_block_cannot_be_overridden_by_historical_memory():
    out = run(
        MARKET_ROW,
        {"alignment_state": "PROCESS_BLOCKED", "process_gate": "FAIL"},
        similarity={"predicted_return": 0.99},
    )
    assert out["status"] == "BLOCK"
    assert out["assessment"] is None
    assert out["gates"]["hard_block"] is True


def test_gate01_missing_alignment_fails_closed():
    out = run(MARKET_ROW, {})
    assert out["status"] == "REVIEW"
    assert out["assessment"] is None
    assert out["gates"]["abstain"] is True


def test_gate01_no_final_trade_command_can_emerge_from_handoff():
    out = run(
        MARKET_ROW,
        {
            "alignment_state": "ALIGNED",
            "candidate_direction": "BEARISH",
            "contradiction_gate": "PASS",
            "process_gate": "PASS",
        },
    )
    assert out["status"] == "ASSESSED"
    assert out["knowledge_evidence"]["final_trade_decision"] is None
