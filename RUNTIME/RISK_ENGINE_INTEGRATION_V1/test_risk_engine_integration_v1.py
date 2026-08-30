from RUNTIME.RISK_ENGINE_INTEGRATION_V1.risk_engine_integration_v1 import evaluate_risk


def test_frozen_2r_boundary_passes_without_float_failure():
    result = evaluate_risk(
        equity=10000.0,
        entry=1.25,
        stop_loss=1.2485,
        take_profit=1.253,
        atr=0.002,
        prior_loss_streak=0,
        peak_equity=10000.0,
    )
    assert result.risk_pass is True
    assert result.rr is not None
    assert abs(result.rr - 2.0) < 1e-10
    assert result.stop_loss == 1.2485
    assert result.take_profit == 1.253


def test_sub_2r_boundary_is_rejected():
    result = evaluate_risk(
        equity=10000.0,
        entry=1.25,
        stop_loss=1.2485,
        take_profit=1.25299,
        atr=0.002,
        prior_loss_streak=0,
        peak_equity=10000.0,
    )
    assert result.risk_pass is False
    assert result.reason == "RR_BELOW_CURRENT_CANONICAL_MINIMUM"
