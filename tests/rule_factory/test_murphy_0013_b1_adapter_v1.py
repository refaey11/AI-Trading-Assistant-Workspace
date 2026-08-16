from src.rule_factory.murphy_0013_b1_candidate_v1 import evaluate_0013_b1_candidate


def test_0013_b1_two_close_up_confirmation():
    result = evaluate_0013_b1_candidate(100.0, True, [101.0, 102.0], "UP")
    assert result["status"] == "DECISIVE_BREAK_CONFIRMED"
    assert result["confirmation_index"] == 1


def test_0013_b1_two_close_down_confirmation():
    result = evaluate_0013_b1_candidate(100.0, True, [99.0, 98.0], "DOWN")
    assert result["status"] == "DECISIVE_BREAK_CONFIRMED"


def test_0013_b1_first_close_is_only_candidate():
    result = evaluate_0013_b1_candidate(100.0, True, [99.0], "DOWN")
    assert result["status"] == "BREAK_CANDIDATE"


def test_0013_b1_intervening_close_blocks_confirmation():
    result = evaluate_0013_b1_candidate(100.0, True, [99.0, 101.0, 98.0], "DOWN")
    assert result["status"] == "NO_CONFIRMATION"


def test_0013_b1_boundary_unavailable_is_not_evaluable():
    result = evaluate_0013_b1_candidate(100.0, False, [99.0, 98.0], "DOWN")
    assert result["status"] == "NOT_EVALUABLE"


def test_0013_b1_no_break_candidate():
    result = evaluate_0013_b1_candidate(100.0, True, [100.0, 99.0], "DOWN")
    assert result["status"] == "NO_BREAK_CANDIDATE"


def test_0013_b1_no_new_tolerance_parameter_exists():
    # The adapter contract intentionally exposes no tolerance/ATR/pip/percent input.
    assert evaluate_0013_b1_candidate.__code__.co_argcount == 4
