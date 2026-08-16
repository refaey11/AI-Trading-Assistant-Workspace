from src.rule_factory.murphy_0013_rule_candidate_v1 import evaluate_0013_rule_candidate

DECISION = "2026-01-01T10:10:00+00:00"
C1 = "2026-01-01T10:05:00+00:00"
C2 = "2026-01-01T10:10:00+00:00"


def _boundary(slope, intercept, availability, relationship="CONVERGING"):
    return {
        "slope": slope,
        "intercept": intercept,
        "relationship": relationship,
        "pivots": [{"availability_timestamp": availability}],
    }


def test_0013_end_to_end_candidate_requires_structure_then_two_closes():
    upper = _boundary(-1, 10, "2026-01-01T10:00:00+00:00")
    lower = _boundary(1, 0, "2026-01-01T10:05:00+00:00")
    result = evaluate_0013_rule_candidate(
        upper, lower, DECISION, 100.0, True, [101.0, 102.0], "UP", [C1, C2]
    )
    assert result["status"] == "CONFIRMED"
    assert result["stage"] == "RULE_CANDIDATE"


def test_0013_end_to_end_stops_at_break_candidate_on_one_close():
    upper = _boundary(-1, 10, "2026-01-01T10:00:00+00:00")
    lower = _boundary(1, 0, "2026-01-01T10:05:00+00:00")
    result = evaluate_0013_rule_candidate(
        upper, lower, DECISION, 100.0, True, [101.0], "UP", [C1]
    )
    assert result["status"] == "BREAK_CANDIDATE"
    assert result["stage"] == "B1"


def test_0013_end_to_end_missing_close_provenance_blocks_b1():
    upper = _boundary(-1, 10, "2026-01-01T10:00:00+00:00")
    lower = _boundary(1, 0, "2026-01-01T10:05:00+00:00")
    result = evaluate_0013_rule_candidate(
        upper, lower, DECISION, 100.0, True, [101.0, 102.0], "UP"
    )
    assert result["status"] == "NOT_EVALUABLE"
    assert result["stage"] == "B1"


def test_0013_end_to_end_future_close_blocks_b1():
    upper = _boundary(-1, 10, "2026-01-01T10:00:00+00:00")
    lower = _boundary(1, 0, "2026-01-01T10:05:00+00:00")
    result = evaluate_0013_rule_candidate(
        upper, lower, DECISION, 100.0, True, [101.0, 102.0], "UP", [C1, "2026-01-01T10:11:00+00:00"]
    )
    assert result["status"] == "NOT_EVALUABLE"
    assert result["stage"] == "B1"


def test_0013_end_to_end_structural_failure_blocks_b1():
    upper = _boundary(1, 10, "2026-01-01T10:00:00+00:00")
    lower = _boundary(1, 0, "2026-01-01T10:05:00+00:00")
    result = evaluate_0013_rule_candidate(
        upper, lower, DECISION, 100.0, True, [101.0, 102.0], "UP", [C1, C2]
    )
    assert result["stage"] == "STRUCTURAL"
    assert result["status"] == "NOT_CONFIRMED"
