from compatibility.similarity_memory_v2_boundary import validate_similarity_read


def base_context(timestamp):
    return {
        "pair": "GBPUSD",
        "timestamp": timestamp,
        "trend": "BEAR_TREND",
        "structure": "INSIDE_RANGE",
    }


def match(timestamp):
    return {
        "pair": "EURUSD",
        "timestamp": timestamp,
        "similarity": 10.0,
        "context_signature": "BEAR_TREND / INSIDE_RANGE",
    }


def test_pre_oos_similarity_passes_and_is_non_directional():
    result = validate_similarity_read(
        current_context=base_context("2024-12-31 16:00:00+00:00"),
        similar_contexts=[match("2023-08-16 06:00:00+00:00")],
    )
    assert result.status == "PASS"
    assert result.result["top_k"] == 20
    assert result.result["not_a_strategy"] is True
    assert result.result["direction"] is None
    assert result.result["final_trade_decision"] is None


def test_current_2025_is_locked_oos():
    result = validate_similarity_read(
        current_context=base_context("2025-12-31 16:00:00+00:00"),
        similar_contexts=[match("2023-08-16 06:00:00+00:00")],
    )
    assert result.status == "NOT_EVALUABLE"
    assert result.reason == "2025_OOS_LOCKED"


def test_2025_similar_match_is_locked_oos():
    result = validate_similarity_read(
        current_context=base_context("2024-12-31 16:00:00+00:00"),
        similar_contexts=[match("2025-11-20 19:00:00+00:00")],
    )
    assert result.status == "NOT_EVALUABLE"
    assert result.reason == "2025_SIMILAR_MATCH_LOCKED"


def test_future_and_top_k_boundaries_fail_closed():
    future = validate_similarity_read(
        current_context=base_context("2026-01-01 00:00:00+00:00"),
        similar_contexts=[],
    )
    assert future.status == "NOT_EVALUABLE"
    assert future.reason == "FUTURE_DATA_FORBIDDEN"

    too_many = validate_similarity_read(
        current_context=base_context("2024-01-01 00:00:00+00:00"),
        similar_contexts=[match(f"2024-01-01 00:{i:02d}:00+00:00") for i in range(21)],
    )
    assert too_many.status == "NOT_EVALUABLE"
    assert too_many.reason == "TOP_K_EXCEEDED"
