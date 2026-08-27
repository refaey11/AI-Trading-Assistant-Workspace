from compatibility.memory_shadow_bridge_v1 import build_shadow_historical_evidence


def evidence():
    return {
        "historical_context": {"status": "OK", "evidence_time_range": {"latest": "2024-06-01T00:00:00Z"}},
        "historical_outcome": {"status": "OK", "evidence_time_range": {"latest": "2024-06-01T00:00:00Z"}},
        "similarity": {"status": "OK", "retrieval_status": "OK", "evidence_time_range": {"latest": "2024-06-01T00:00:00Z"}},
        "context_aware_retrieval": {"status": "OK", "evidence_time_range": {"latest": "2024-06-01T00:00:00Z"}},
    }


def test_pre_2025_shadow_passes_and_is_evidence_only():
    result = build_shadow_historical_evidence(
        query_as_of="2024-06-15T12:00:00Z",
        **evidence(),
        murphy_direction="BULLISH",
    )
    assert result["status"] == "PASS"
    package = result["historical_evidence"]
    assert package["memory_role"] == "EVIDENCE_ONLY"
    assert package["governance"]["direction"] is None
    assert package["governance"]["final_trade_decision"] is None
    assert package["consumption"]["downstream_direction_changed"] is False


def test_2025_is_locked():
    result = build_shadow_historical_evidence(
        query_as_of="2025-01-01T00:00:00Z",
        **evidence(),
    )
    assert result["status"] == "NOT_EVALUABLE"
    assert result["reason"] == "2025_OOS_LOCKED"


def test_future_evidence_fails_closed():
    payloads = evidence()
    payloads["similarity"]["evidence_time_range"]["latest"] = "2025-02-01T00:00:00Z"
    result = build_shadow_historical_evidence(
        query_as_of="2024-12-01T00:00:00Z",
        **payloads,
    )
    assert result["status"] == "NOT_EVALUABLE"
    assert result["reason"] == "FUTURE_OR_OOS_EVIDENCE"


def test_no_memory_source_can_be_sole_decision_maker():
    result = build_shadow_historical_evidence(
        query_as_of="2023-08-01T00:00:00Z",
        **evidence(),
        murphy_direction="BEARISH",
    )
    package = result["historical_evidence"]
    assert package["governance"]["similarity_is_sole_decision_maker"] is False
    assert package["governance"]["predicted_return_used_as_direction"] is False
