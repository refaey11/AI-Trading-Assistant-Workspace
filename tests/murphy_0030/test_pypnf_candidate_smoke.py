"""Smoke compatibility checks for the externally discovered pnf-chart-system candidate.

These tests establish API/feature availability only. They do not certify Murphy
semantic equivalence or approve a box-size policy.
"""
import pytest

pypnf = pytest.importorskip("pypnf")


def build_candidate_chart():
    cfg = pypnf.ChartConfig()
    cfg.method = pypnf.ConstructionMethod.HighLow
    cfg.box_size_method = pypnf.BoxSizeMethod.Traditional
    cfg.box_size = 0.0
    cfg.reversal = 3
    chart = pypnf.Chart(cfg)
    for row in [
        (1.1050, 1.1000, 1.1030, 1700000000),
        (1.1080, 1.1010, 1.1060, 1700003600),
        (1.1100, 1.1040, 1.1080, 1700007200),
        (1.1060, 1.0960, 1.0990, 1700010800),
        (1.1030, 1.0920, 1.0950, 1700014400),
        (1.1000, 1.0890, 1.0920, 1700018000),
    ]:
        chart.add_data(*row)
    return chart


def test_candidate_exposes_required_0030_construction_surface():
    chart = build_candidate_chart()
    assert chart.column_count() >= 1
    assert hasattr(chart, "has_bullish_bias")
    assert hasattr(chart, "is_above_bullish_support")


def test_candidate_bullish_support_check_is_callable():
    chart = build_candidate_chart()
    result = chart.is_above_bullish_support(1.0950)
    assert isinstance(result, bool)


def test_candidate_configuration_is_explicitly_three_box_high_low():
    cfg = pypnf.ChartConfig()
    cfg.method = pypnf.ConstructionMethod.HighLow
    cfg.box_size_method = pypnf.BoxSizeMethod.Traditional
    cfg.box_size = 0.0
    cfg.reversal = 3
    assert cfg.method == pypnf.ConstructionMethod.HighLow
    assert cfg.reversal == 3
