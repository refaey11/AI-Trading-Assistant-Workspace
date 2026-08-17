from risk_engine.murphy_0042_0045_risk_adapter import evaluate_portfolio


def test_all_limits_pass_at_boundaries():
    r = evaluate_portfolio(total_investment=.50, single_market_exposure=.15,
                           risk_per_market=.05, total_margin=.25)
    assert r["pass"] is True
    assert all(r["checks"].values())


def test_total_investment_breach():
    r = evaluate_portfolio(total_investment=.500001, single_market_exposure=.15,
                           risk_per_market=.05, total_margin=.25)
    assert r["checks"]["MURPHY_0042"] is False
    assert r["pass"] is False


def test_single_market_exposure_breach():
    r = evaluate_portfolio(total_investment=.50, single_market_exposure=.150001,
                           risk_per_market=.05, total_margin=.25)
    assert r["checks"]["MURPHY_0043"] is False


def test_market_risk_breach():
    r = evaluate_portfolio(total_investment=.50, single_market_exposure=.15,
                           risk_per_market=.050001, total_margin=.25)
    assert r["checks"]["MURPHY_0044"] is False


def test_margin_breach():
    r = evaluate_portfolio(total_investment=.50, single_market_exposure=.15,
                           risk_per_market=.05, total_margin=.250001)
    assert r["checks"]["MURPHY_0045"] is False
