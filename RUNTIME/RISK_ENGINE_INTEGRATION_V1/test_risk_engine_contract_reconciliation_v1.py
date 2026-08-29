from RUNTIME.RISK_ENGINE_INTEGRATION_V1.risk_engine_integration_v1 import evaluate_risk


def test_risk_result_exposes_execution_prices():
    result = evaluate_risk(
        equity=10000.0,
        entry=1.25,
        stop_loss=1.2485,
        take_profit=1.2545,
        atr=0.002,
        prior_loss_streak=0,
        peak_equity=10000.0,
    )

    assert result.risk_pass is True
    assert result.risk_percent == 0.005
    assert result.stop_loss == 1.2485
    assert result.take_profit == 1.2545
    assert result.rr >= 3.0
    assert result.position_size is not None


def test_exact_3r_float_rounding_does_not_fail_boundary():
    result = evaluate_risk(
        equity=10000.0,
        entry=1.25,
        stop_loss=1.2485,
        take_profit=1.2545,
        atr=0.002,
        prior_loss_streak=0,
        peak_equity=10000.0,
    )

    assert abs(result.rr - 3.0) <= 1e-12
    assert result.risk_pass is True
    assert result.reason == "RISK_GATE_PASS"


def test_materially_below_3r_still_fails():
    result = evaluate_risk(
        equity=10000.0,
        entry=1.25,
        stop_loss=1.2485,
        take_profit=1.2544,
        atr=0.002,
        prior_loss_streak=0,
        peak_equity=10000.0,
    )

    assert result.risk_pass is False
    assert result.reason == "RR_BELOW_CURRENT_CANONICAL_MINIMUM"
