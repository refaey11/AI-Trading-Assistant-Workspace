from compatibility.historical_context_memory_boundary_v1 import validate_historical_context


def base_kwargs(timestamp):
    return {
        "timestamp": timestamp,
        "symbol": "GBPUSD",
        "timeframe": "H1",
        "context": {"trend": "UP", "structure": "INTACT"},
        "provenance": {"source": "historical_context_memory"},
    }


def test_pre_oos_context_passes_and_remains_non_directional():
    result = validate_historical_context(**base_kwargs("2024-12-31T23:00:00Z"))
    assert result.status == "PASS"
    assert result.record["not_a_strategy"] is True
    assert result.record["direction"] is None
    assert result.record["final_trade_decision"] is None


def test_2025_is_locked_oos():
    result = validate_historical_context(**base_kwargs("2025-01-02T00:00:00Z"))
    assert result.status == "NOT_EVALUABLE"
    assert result.reason == "2025_OOS_LOCKED"


def test_future_data_is_forbidden():
    result = validate_historical_context(**base_kwargs("2026-01-01T00:00:00Z"))
    assert result.status == "NOT_EVALUABLE"
    assert result.reason == "FUTURE_DATA_FORBIDDEN"


def test_invalid_timestamp_and_missing_identity_fail_closed():
    invalid = validate_historical_context(**base_kwargs("not-a-date"))
    assert invalid.status == "NOT_EVALUABLE"
    assert invalid.reason == "INVALID_TIMESTAMP"

    missing = validate_historical_context(
        timestamp="2024-01-01T00:00:00Z",
        symbol="",
        timeframe="H1",
        context={"trend": "UP"},
        provenance={},
    )
    assert missing.status == "NOT_EVALUABLE"
    assert missing.reason == "MISSING_CONTEXT_IDENTITY"
