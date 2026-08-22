from compatibility.memory_evidence_package_v1 import build_memory_evidence_package


def evidence():
    return {
        "historical_context": {"status": "OK", "coverage": 1.0},
        "historical_outcome": {"status": "OK", "eligible_cases": 17},
        "similarity": {"status": "OK", "candidate_count": 20},
    }


def test_development_package_passes_pre_oos_and_is_non_directional():
    result = build_memory_evidence_package(
        query_as_of="2024-12-31T23:00:00Z",
        **evidence(),
        provenance={"source": "verified_memory_layers"},
    )
    assert result.status == "PASS"
    assert result.package["memory_role"] == "EVIDENCE_ONLY"
    assert result.package["direction"] is None
    assert result.package["final_trade_decision"] is None
    assert result.package["similarity_is_sole_decision_maker"] is False


def test_development_2025_is_locked():
    result = build_memory_evidence_package(
        query_as_of="2025-01-01T00:00:00Z",
        **evidence(),
    )
    assert result.status == "NOT_EVALUABLE"
    assert result.reason == "2025_OOS_LOCKED"


def test_oos_2025_is_explicit_and_still_non_directional():
    result = build_memory_evidence_package(
        query_as_of="2025-01-01T00:00:00Z",
        mode="oos_evaluation",
        **evidence(),
    )
    assert result.status == "PASS"
    assert result.package["mode"] == "oos_evaluation"
    assert result.package["direction"] is None
    assert result.package["final_trade_decision"] is None


def test_future_data_is_forbidden_even_in_oos_mode():
    result = build_memory_evidence_package(
        query_as_of="2026-01-01T00:00:00Z",
        mode="oos_evaluation",
        **evidence(),
    )
    assert result.status == "NOT_EVALUABLE"
    assert result.reason == "FUTURE_DATA_FORBIDDEN"


def test_invalid_evidence_fails_closed():
    result = build_memory_evidence_package(
        query_as_of="2024-12-31T23:00:00Z",
        historical_context=None,
        historical_outcome={},
        similarity={},
    )
    assert result.status == "NOT_EVALUABLE"
    assert result.reason == "INVALID_HISTORICAL_CONTEXT_EVIDENCE"
