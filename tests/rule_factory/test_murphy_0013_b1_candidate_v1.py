from src.rule_factory.murphy_0013_b1_candidate_v1 import evaluate_0013_b1_candidate

DECISION = "2026-01-01T10:10:00+00:00"
C1 = "2026-01-01T10:05:00+00:00"
C2 = "2026-01-01T10:10:00+00:00"


def test_0013_b1_adapter_confirms_two_close_up_break():
    result = evaluate_0013_b1_candidate(100.0, True, [101.0, 102.0], "UP", [C1, C2], DECISION)
    assert result["status"] == "DECISIVE_BREAK_CONFIRMED"


def test_0013_b1_adapter_confirms_two_close_down_break():
    result = evaluate_0013_b1_candidate(100.0, True, [99.0, 98.0], "DOWN", [C1, C2], DECISION)
    assert result["status"] == "DECISIVE_BREAK_CONFIRMED"


def test_0013_b1_adapter_one_close_is_only_candidate():
    result = evaluate_0013_b1_candidate(100.0, True, [101.0], "UP", [C1], DECISION)
    assert result["status"] == "BREAK_CANDIDATE"


def test_0013_b1_adapter_intervening_close_blocks_confirmation():
    result = evaluate_0013_b1_candidate(100.0, True, [101.0, 99.0], "UP", [C1, C2], DECISION)
    assert result["status"] == "NO_CONFIRMATION"


def test_0013_b1_adapter_unavailable_boundary_is_not_evaluable():
    result = evaluate_0013_b1_candidate(100.0, False, [101.0, 102.0], "UP", [C1, C2], DECISION)
    assert result["status"] == "NOT_EVALUABLE"


def test_0013_b1_adapter_missing_close_provenance_is_not_evaluable():
    result = evaluate_0013_b1_candidate(100.0, True, [101.0, 102.0], "UP")
    assert result["status"] == "NOT_EVALUABLE"


def test_0013_b1_adapter_future_close_is_not_evaluable():
    future = "2026-01-01T10:11:00+00:00"
    result = evaluate_0013_b1_candidate(100.0, True, [101.0, 102.0], "UP", [C1, future], DECISION)
    assert result["status"] == "NOT_EVALUABLE"


def test_0013_b1_adapter_reversed_close_chronology_is_not_evaluable():
    result = evaluate_0013_b1_candidate(100.0, True, [101.0, 102.0], "UP", [C2, C1], DECISION)
    assert result["status"] == "NOT_EVALUABLE"


def test_0013_b1_adapter_invalid_direction_is_not_evaluable():
    result = evaluate_0013_b1_candidate(100.0, True, [101.0, 102.0], "SIDEWAYS", [C1, C2], DECISION)
    assert result["status"] == "NOT_EVALUABLE"
