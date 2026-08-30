from risk_engine_integration_v1 import evaluate_risk


def test_recovered_runtime_accepts_1_5r_research_case():
    result = evaluate_risk(
        equity=10_000.0,
        entry=1.2500,
        stop_loss=1.2450,
        take_profit=1.2575,
        atr=0.0050,
        prior_loss_streak=0,
        peak_equity=10_000.0,
    )
    assert result.risk_pass is True
    assert round(result.rr, 6) == 1.5
    assert round(result.stop_loss, 6) == 1.245
    assert round(result.take_profit, 6) == 1.2575


def test_frozen_execution_adapter_2r_case_is_accepted():
    result = evaluate_risk(
        equity=10_000.0,
        entry=1.2500,
        stop_loss=1.2450,
        take_profit=1.2600,
        atr=0.0050,
        prior_loss_streak=0,
        peak_equity=10_000.0,
    )
    assert result.risk_pass is True
    assert round(result.rr, 6) == 2.0


def test_missing_execution_inputs_fail_closed():
    result = evaluate_risk(
        equity=10_000.0,
        entry=1.2500,
        stop_loss=None,
        take_profit=None,
        atr=0.0050,
        prior_loss_streak=0,
        peak_equity=10_000.0,
    )
    assert result.risk_pass is False
    assert result.reason == "MISSING_EXECUTION_INPUT"
