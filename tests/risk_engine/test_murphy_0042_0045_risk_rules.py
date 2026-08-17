from risk_engine.murphy_0042_0045_risk_adapter import (
    evaluate_0042,
    evaluate_0043,
    evaluate_0044,
    evaluate_0045,
    evaluate_portfolio,
)


def test_0042_boundary_and_breach():
    assert evaluate_0042(0.50) is True
    assert evaluate_0042(0.500001) is False


def test_0043_boundary_and_breach():
    assert evaluate_0043(0.15) is True
    assert evaluate_0043(0.150001) is False


def test_0044_boundary_and_breach():
    assert evaluate_0044(0.05) is True
    assert evaluate_0044(0.050001) is False


def test_0045_boundary_and_breach():
    assert evaluate_0045(0.25) is True
    assert evaluate_0045(0.250001) is False


def test_negative_values_fail():
    assert evaluate_0042(-0.01) is False
    assert evaluate_0043(-0.01) is False
    assert evaluate_0044(-0.01) is False
    assert evaluate_0045(-0.01) is False


def test_portfolio_passes_at_operational_boundaries():
    result = evaluate_portfolio(
        total_investment=0.50,
        single_market_exposure=0.15,
        risk_per_market=0.05,
        total_margin=0.25,
    )
    assert result["pass"] is True
    assert all(result["checks"].values())


def test_portfolio_fails_when_any_rule_breaches():
    result = evaluate_portfolio(
        total_investment=0.50,
        single_market_exposure=0.150001,
        risk_per_market=0.05,
        total_margin=0.25,
    )
    assert result["pass"] is False
    assert result["checks"]["MURPHY_0043"] is False
