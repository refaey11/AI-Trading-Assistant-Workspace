from compatibility.historical_outcome_memory_boundary_v1 import validate_historical_outcome


def base_stats():
    return {
        "occurrences": 100,
        "median_return_6h": 0.001,
        "mean_return_6h": 0.0012,
        "positive_rate_6h": 0.52,
        "median_return_12h": 0.0015,
        "mean_return_12h": 0.0017,
        "positive_rate_12h": 0.53,
        "median_return_24h": 0.002,
        "mean_return_24h": 0.0021,
        "positive_rate_24h": 0.54,
        "median_return_48h": 0.0024,
        "mean_return_48h": 0.0026,
        "positive_rate_48h": 0.55,
    }


def base_kwargs(timestamp):
    return {
        "timestamp": timestamp,
        "pair": "GBPUSD",
        "context_signature": "BULL_TREND / INSIDE_RANGE / MID_RANGE / NORMAL / NORMAL / no_major_candle",
        "stats": base_stats(),
        "provenance": {"source": "historical_outcome_memory_v1"},
    }


def test_pre_oos_outcome_passes_and_is_evidence_only():
    result = validate_historical_outcome(**base_kwargs("2024-12-31T23:00:00Z"))
    assert result.status == "PASS"
    assert result.evidence["not_a_strategy"] is True
    assert result.evidence["direction"] is None
    assert result.evidence["final_trade_decision"] is None
    assert result.evidence["scenario_classification"] is None


def test_2025_is_locked_oos():
    result = validate_historical_outcome(**base_kwargs("2025-01-02T00:00:00Z"))
    assert result.status == "NOT_EVALUABLE"
    assert result.reason == "2025_OOS_LOCKED"


def test_future_data_is_forbidden():
    result = validate_historical_outcome(**base_kwargs("2026-01-01T00:00:00Z"))
    assert result.status == "NOT_EVALUABLE"
    assert result.reason == "FUTURE_DATA_FORBIDDEN"


def test_missing_or_invalid_stats_fail_closed():
    missing = validate_historical_outcome(
        timestamp="2024-01-01T00:00:00Z",
        pair="GBPUSD",
        context_signature="CTX",
        stats={"occurrences": 1},
        provenance={},
    )
    assert missing.status == "NOT_EVALUABLE"
    assert missing.reason == "MISSING_OUTCOME_STATS"

    invalid = base_kwargs("2024-01-01T00:00:00Z")
    invalid["stats"] = {**base_stats(), "positive_rate_6h": 1.5}
    result = validate_historical_outcome(**invalid)
    assert result.status == "NOT_EVALUABLE"
    assert result.reason == "INVALID_POSITIVE_RATE"
