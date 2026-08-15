import math
from datetime import date

import pytest

from src.murphy_0030_0032.project_box_policy import compute_three_year_box_pct


def test_box_policy_is_deterministic():
    closes = [100.0, 101.0, 100.0, 102.0]
    a = compute_three_year_box_pct(closes, date(2016, 1, 1), date(2018, 12, 31))
    b = compute_three_year_box_pct(closes, date(2016, 1, 1), date(2018, 12, 31))
    assert a == b


def test_box_policy_uses_sample_standard_deviation_of_log_returns():
    closes = [100.0, 101.0, 100.0, 102.0]
    result = compute_three_year_box_pct(closes, date(2016, 1, 1), date(2018, 12, 31))
    returns = [math.log(101/100), math.log(100/101), math.log(102/100)]
    expected = (sum((r - sum(returns)/len(returns))**2 for r in returns) / 2) ** 0.5
    assert abs(result.daily_log_return_std - expected) < 1e-12
    assert abs(result.box_pct - expected * 100) < 1e-12


def test_invalid_inputs_are_rejected():
    with pytest.raises(ValueError):
        compute_three_year_box_pct([100.0], date(2016, 1, 1), date(2018, 12, 31))
    with pytest.raises(ValueError):
        compute_three_year_box_pct([100.0, -1.0], date(2016, 1, 1), date(2018, 12, 31))
    with pytest.raises(ValueError):
        compute_three_year_box_pct([100.0, 101.0], date(2018, 12, 31), date(2016, 1, 1))
