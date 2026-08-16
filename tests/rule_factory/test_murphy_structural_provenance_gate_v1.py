from src.rule_factory.murphy_structural_evaluators_v1 import evaluate_0013, evaluate_0020


def _boundary(slope, intercept, availability):
    return {
        "slope": slope,
        "intercept": intercept,
        "pivots": [{"availability_timestamp": availability}],
    }


def test_structural_confirm_requires_available_pivots():
    upper = _boundary(-1, 10, "2026-01-01T10:00:00+00:00")
    lower = _boundary(1, 0, "2026-01-01T10:05:00+00:00")
    result = evaluate_0013(upper, lower, "2026-01-01T10:05:00+00:00")
    assert result["status"] == "CONFIRMED"


def test_future_pivot_cannot_confirm_structure():
    upper = _boundary(-1, 10, "2026-01-01T10:00:00+00:00")
    lower = _boundary(1, 0, "2026-01-01T10:06:00+00:00")
    result = evaluate_0013(upper, lower, "2026-01-01T10:05:00+00:00")
    assert result["status"] == "NOT_EVALUABLE"


def test_missing_provenance_cannot_confirm_rectangle():
    upper = {"slope": 0, "intercept": 10}
    lower = {"slope": 0, "intercept": 5}
    result = evaluate_0020(upper, lower, "2026-01-01T10:05:00+00:00")
    assert result["status"] == "NOT_EVALUABLE"
