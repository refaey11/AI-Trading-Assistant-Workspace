from compatibility.decision_brain_v1_handoff_adapter import assess_with_governance


class _Brain:
    @staticmethod
    def assess(row, similarity=None):
        class A:
            directional_bias = "bullish"
            confidence = 0.8
            evidence = []
            contradictions = []
            market_state = "trend"
            no_trade_reasons = []
        return A()


def test_memory_is_consumed_as_non_directional_evidence():
    memory = {
        "sources": {
            "historical_context": {"available": True, "candidate_count": 5},
            "historical_outcome": {"available": True, "candidate_count": 7},
            "similarity": {"available": True, "candidate_count": 3},
            "context_aware_retrieval": {"available": True, "candidate_count": 2},
        },
        "governance": {"memory_role": "EVIDENCE_ONLY"},
    }
    result = assess_with_governance(
        _Brain,
        row={"close": 1.25},
        query_as_of="2024-12-31T12:00:00Z",
        mode="development",
        murphy_evidence={},
        nison_evidence={},
        tiz_evidence={"process_gate": "PASS"},
        risk_evidence={"risk_status": "PASS"},
        historical_evidence=memory,
    )
    assert result["status"] == "PASS"
    assert result["assessment"]["directional_bias"] == "bullish"
    assert result["governance"]["historical_memory_consumed_downstream"] is True
    assert result["governance"]["historical_memory_used_for_direction"] is False
    assert result["governance"]["similarity_generated_direction"] is False


def test_2025_remains_locked_even_with_memory():
    result = assess_with_governance(
        _Brain,
        row={},
        query_as_of="2025-01-02T00:00:00Z",
        mode="development",
        historical_evidence={"sources": {"historical_context": {"available": True}}},
    )
    assert result["status"] == "NOT_EVALUABLE"
    assert result["reason"] == "2025_OOS_LOCKED"
