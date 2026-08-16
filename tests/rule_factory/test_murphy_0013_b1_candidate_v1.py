from datetime import datetime, timezone

from src.rule_factory.murphy_0013_b1_candidate_v1 import evaluate_0013_b1_candidate


def test_0013_b1_adapter_confirms_two_close_up_break():
    result = evaluate_0013_b1_candidate(100.0, True, [101.0, 102.0], "UP")
    assert result["status"] == "DECISIVE_BREAK_CONFIRMED"
    assert result["confirmation_index"] == 1


def test_0013_b1_adapter_confirms_two_close_down_break():
    result = evaluate_0013_b1_candidate(100.0, True, [99.0, 98.0], "DOWN")
    assert result["status"] == "DECISIVE_BREAK_CONFIRMED"


def test_0013_b1_adapter_one_close_is_only_candidate():
    result = evaluate_0013_b1_candidate(100.0, True, [101.0], "UP")
    assert result["status"] == "BREAK_CANDIDATE"


def test_0013_b1_adapter_intervening_close_blocks_confirmation():
    result = evaluate_0013_b1_candidate(100.0, True, [101.0, 99.0], "UP")
    assert result["status"] == "NO_CONFIRMATION"


def test_0013_b1_adapter_unavailable_boundary_is_not_evaluable():
    result = evaluate_0013_b1_candidate(100.0, False, [101.0, 102.0], "UP")
    assert result["status"] == "NOT_EVALUABLE"


def test_0013_b1_adapter_invalid_direction_is_not_evaluable():
    result = evaluate_0013_b1_candidate(100.0, True, [101.0, 102.0], "SIDEWAYS")
    assert result["status"] == "NOT_EVALUABLE"


def test_0013_b1_adapter_future_boundary_must_not_be_used():
    decision = datetime(2026, 1, 2, tzinfo=timezone.utc)
    boundary_available = datetime(2026, 1, 3, tzinfo=timezone.utc)
    assert boundary_available > decision
    # Availability is an input contract gate; future evidence is not usable.
    result = evaluate_0013_b1_candidate(None, False, [101.0, 102.0], "UP")
    assert result["status"] == "NOT_EVALUABLE"
