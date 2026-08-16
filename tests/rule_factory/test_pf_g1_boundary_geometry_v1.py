from src.rule_factory.pf_g1_boundary_geometry_v1 import evaluate_pf_g1


def test_exact_parallel_lines():
    result = evaluate_pf_g1({"slope": 1, "intercept": 5}, {"slope": 1, "intercept": 1})
    assert result["status"] == "PARALLEL_EXACT"


def test_exact_convergence():
    result = evaluate_pf_g1({"slope": 1, "intercept": 5}, {"slope": -1, "intercept": 1})
    assert result["status"] == "CONVERGING_EXACT"
    assert result["intersection_x"] == -2


def test_missing_geometry_is_not_evaluable():
    result = evaluate_pf_g1({"slope": 1}, {"slope": -1, "intercept": 1})
    assert result["status"] == "NOT_EVALUABLE"
