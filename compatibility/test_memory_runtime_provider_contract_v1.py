from compatibility.memory_runtime_provider_contract_v1 import query_existing_memory_runtime


def _provider(status):
    def _call(query_as_of, event):
        return {"status": status, "query_as_of": query_as_of}
    return _call


def test_all_source_backed_providers_are_packaged_as_evidence_only():
    providers = {
        "historical_context": _provider("WORKING"),
        "historical_outcome": _provider("WORKING"),
        "similarity": _provider("PASS"),
        "context_aware_retrieval": _provider("PASS"),
    }
    result = query_existing_memory_runtime(
        query_as_of="2024-12-31T12:00:00Z",
        event={"pair": "GBPUSD"},
        providers=providers,
    )
    assert result["status"] == "PASS"
    assert result["memory_role"] == "EVIDENCE_ONLY"
    assert result["memory_generated_direction"] is False
    assert result["final_trade_decision_generated"] is False
    assert result["historical_memory_used_for_direction"] is False
    assert result["2025_used_for_tuning"] is False


def test_missing_similarity_and_retrieval_are_not_fabricated():
    providers = {
        "historical_context": _provider("WORKING"),
        "historical_outcome": _provider("WORKING"),
        "similarity": None,
        "context_aware_retrieval": None,
    }
    result = query_existing_memory_runtime(
        query_as_of="2024-12-31T12:00:00Z",
        event={"pair": "GBPUSD"},
        providers=providers,
    )
    assert result["status"] == "NOT_READY"
    assert set(result["missing_providers"]) == {"similarity", "context_aware_retrieval"}
    assert result["memory_generated_direction"] is False


def test_2025_is_locked_before_provider_calls():
    called = {"count": 0}

    def provider(query_as_of, event):
        called["count"] += 1
        return {"status": "PASS"}

    providers = {name: provider for name in (
        "historical_context",
        "historical_outcome",
        "similarity",
        "context_aware_retrieval",
    )}
    result = query_existing_memory_runtime(
        query_as_of="2025-01-01T00:00:00Z",
        event={},
        providers=providers,
    )
    assert result == {"status": "NOT_EVALUABLE", "reason": "2025_OOS_LOCKED"}
    assert called["count"] == 0


def test_future_evidence_is_flagged():
    def good(query_as_of, event):
        return {"status": "PASS", "query_as_of": query_as_of}

    def future(query_as_of, event):
        return {"status": "PASS", "query_as_of": "2025-01-02T00:00:00Z"}

    providers = {
        "historical_context": good,
        "historical_outcome": good,
        "similarity": good,
        "context_aware_retrieval": future,
    }
    result = query_existing_memory_runtime(
        query_as_of="2024-12-31T12:00:00Z",
        event={},
        providers=providers,
    )
    assert result["status"] == "PASS"
    assert result["receipt"]["lookahead_violations"] == 1
