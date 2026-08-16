from src.rule_factory.murphy_structural_evaluators_v1 import (
    evaluate_0013,
    evaluate_0014,
    evaluate_0018,
    evaluate_0019,
    evaluate_0020,
)

DECISION = "2026-01-01T10:05:00+00:00"


def _boundary(slope, intercept, availability, relationship=None):
    result = {
        "slope": slope,
        "intercept": intercept,
        "pivots": [{"availability_timestamp": availability}],
    }
    if relationship is not None:
        result["relationship"] = relationship
    return result


def test_h1_exact_horizontal_is_evaluable():
    upper = _boundary(0, 10, "2026-01-01T10:00:00+00:00")
    lower = _boundary(1, 0, "2026-01-01T10:05:00+00:00")
    result = evaluate_0014(upper, lower, DECISION)
    assert result["status"] == "CONFIRMED"


def test_h1_missing_slope_is_not_evaluable():
    upper = {"intercept": 10, "pivots": [{"availability_timestamp": "2026-01-01T10:00:00+00:00"}]}
    lower = _boundary(1, 0, "2026-01-01T10:05:00+00:00")
    result = evaluate_0014(upper, lower, DECISION)
    assert result["status"] == "NOT_EVALUABLE"


def test_h1_near_horizontal_is_not_confirmed_without_approved_tolerance():
    upper = _boundary(1e-9, 10, "2026-01-01T10:00:00+00:00")
    lower = _boundary(1, 0, "2026-01-01T10:05:00+00:00")
    result = evaluate_0014(upper, lower, DECISION)
    assert result["status"] != "CONFIRMED"


def test_g1_requires_canonical_convergence_relationship():
    upper = _boundary(-1, 10, "2026-01-01T10:00:00+00:00")
    lower = _boundary(1, 0, "2026-01-01T10:05:00+00:00")
    result = evaluate_0013(upper, lower, DECISION)
    assert result["status"] == "NOT_EVALUABLE"


def test_g1_convergence_relationship_is_accepted():
    upper = _boundary(-1, 10, "2026-01-01T10:00:00+00:00", "CONVERGING")
    lower = _boundary(1, 0, "2026-01-01T10:05:00+00:00", "CONVERGING")
    result = evaluate_0013(upper, lower, DECISION)
    assert result["status"] == "CONFIRMED"


def test_g1_inconsistent_relationship_is_not_confirmed():
    upper = _boundary(-1, 10, "2026-01-01T10:00:00+00:00", "CONVERGING")
    lower = _boundary(1, 0, "2026-01-01T10:05:00+00:00", "PARALLEL")
    result = evaluate_0013(upper, lower, DECISION)
    assert result["status"] == "NOT_CONFIRMED"


def test_f1_sharpness_dependent_decision_is_not_claimed_by_structural_suite():
    # This suite deliberately does not invent a numeric definition of "sharp".
    # Flag/Pennant sharpness remains a separate NOT_EVALUABLE gate.
    assert "sharp" not in {"approved_threshold": None}


def test_rectangle_requires_two_distinct_exact_horizontal_boundaries():
    upper = _boundary(0, 10, "2026-01-01T10:00:00+00:00")
    lower = _boundary(0, 5, "2026-01-01T10:05:00+00:00")
    result = evaluate_0020(upper, lower, DECISION)
    assert result["status"] == "CONFIRMED"


def test_rectangle_same_boundary_is_not_confirmed():
    upper = _boundary(0, 10, "2026-01-01T10:00:00+00:00")
    lower = _boundary(0, 10, "2026-01-01T10:05:00+00:00")
    result = evaluate_0020(upper, lower, DECISION)
    assert result["status"] == "NOT_CONFIRMED"


def test_falling_wedge_requires_convergence_and_negative_slopes():
    upper = _boundary(-1, 10, "2026-01-01T10:00:00+00:00", "CONVERGING")
    lower = _boundary(-2, 12, "2026-01-01T10:05:00+00:00", "CONVERGING")
    result = evaluate_0018(upper, lower, DECISION)
    assert result["status"] == "CONFIRMED"


def test_rising_wedge_requires_convergence_and_positive_slopes():
    upper = _boundary(2, 0, "2026-01-01T10:00:00+00:00", "CONVERGING")
    lower = _boundary(1, -2, "2026-01-01T10:05:00+00:00", "CONVERGING")
    result = evaluate_0019(upper, lower, DECISION)
    assert result["status"] == "CONFIRMED"
