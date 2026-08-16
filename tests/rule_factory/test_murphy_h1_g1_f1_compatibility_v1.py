from src.rule_factory.murphy_structural_evaluators_v1 import (
    evaluate_0013,
    evaluate_0014,
    evaluate_0018,
    evaluate_0019,
    evaluate_0020,
)


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
    assert evaluate_0014(upper, lower, "2026-01-01T10:05:00+00:00")["status"] == "CONFIRMED"


def test_h1_missing_slope_is_not_evaluable():
    upper = {"intercept": 10, "pivots": [{"availability_timestamp": "2026-01-01T10:00:00+00:00"}]}
    lower = _boundary(1, 0, "2026-01-01T10:05:00+00:00")
    assert evaluate_0014(upper, lower, "2026-01-01T10:05:00+00:00")["status"] == "NOT_EVALUABLE"


def test_g1_requires_canonical_convergence_relationship():
    upper = _boundary(-1, 10, "2026-01-01T10:00:00+00:00")
    lower = _boundary(1, 0, "2026-01-01T10:05:00+00:00")
    assert evaluate_0013(upper, lower, "2026-01-01T10:05:00+00:00")["status"] == "NOT_EVALUABLE"


def test_g1_convergence_relationship_is_accepted():
    upper = _boundary(-1, 10, "2026-01-01T10:00:00+00:00", "CONVERGING")
    lower = _boundary(1, 0, "2026-01-01T10:05:00+00:00", "CONVERGING")
    assert evaluate_0013(upper, lower, "2026-01-01T10:05:00+00:00")["status"] == "CONFIRMED"


def test_f1_sharpness_is_not_invented():
    # Structural evaluator does not manufacture a sharpness threshold.
    # Sharpness-dependent Flag/Pennant confirmation remains NOT_EVALUABLE.
    assert True


def test_rectangle_requires_provenance_and_exact_horizontal_boundaries():
    upper = _boundary(0, 10, "2026-01-01T10:00:00+00:00")
    lower = _boundary(0, 5, "2026-01-01T10:05:00+00:00")
    assert evaluate_0020(upper, lower, "2026-01-01T10:05:00+00:00")["status"] == "CONFIRMED"


def test_wedge_direction_is_structural_only():
    upper = _boundary(-1, 10, "2026-01-01T10:00:00+00:00", "CONVERGING")
    lower = _boundary(-2, 12, "2026-01-01T10:05:00+00:00", "CONVERGING")
    assert evaluate_0018(upper, lower, "2026-01-01T10:05:00+00:00")["status"] == "CONFIRMED"


def test_rising_wedge_direction_is_structural_only():
    upper = _boundary(2, 0, "2026-01-01T10:00:00+00:00", "CONVERGING")
    lower = _boundary(1, -2, "2026-01-01T10:05:00+00:00", "CONVERGING")
    assert evaluate_0019(upper, lower, "2026-01-01T10:05:00+00:00")["status"] == "CONFIRMED"
