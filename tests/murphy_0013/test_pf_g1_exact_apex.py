from src.murphy_0013.pf_g1_exact_apex import evaluate_convergence


def line(slope, intercept, availability=2, anchor_end=2):
    return {
        "slope": slope,
        "intercept": intercept,
        "availability_ts": availability,
        "anchor_end_ts": anchor_end,
    }


def test_valid_forward_apex_is_converging():
    result = evaluate_convergence(line(-0.5, 10), line(0.5, 2), 5)
    assert result["relationship"] == "CONVERGING"
    assert result["apex_timestamp"] == 8
    assert result["apex_price"] == 6
    assert result["availability_timestamp"] == 2


def test_evaluation_before_geometry_availability_is_not_evaluable():
    result = evaluate_convergence(line(-0.5, 10), line(0.5, 2), 1)
    assert result["relationship"] == "NOT_EVALUABLE"


def test_missing_geometry_is_not_evaluable():
    result = evaluate_convergence({}, line(0.5, 2), 5)
    assert result["relationship"] == "NOT_EVALUABLE"


def test_wrong_slope_orientation_is_not_converging():
    result = evaluate_convergence(line(0.5, 10), line(0.5, 2), 5)
    assert result["relationship"] == "NOT_CONVERGING"


def test_apex_in_past_is_not_converging():
    # Upper: y = -0.5x + 4; lower: y = 0.5x + 2 => apex x=2, before evaluation.
    result = evaluate_convergence(line(-0.5, 4), line(0.5, 2), 5)
    assert result["relationship"] == "NOT_CONVERGING"


def test_future_suffix_cannot_change_a_record_from_same_geometry():
    base = evaluate_convergence(line(-0.5, 10), line(0.5, 2), 5)
    mutated_future = evaluate_convergence(line(-0.5, 10), line(0.5, 2), 5)
    assert mutated_future == base


def test_no_buy_sell_output_is_possible():
    result = evaluate_convergence(line(-0.5, 10), line(0.5, 2), 5)
    assert "BUY" not in result
    assert "SELL" not in result
