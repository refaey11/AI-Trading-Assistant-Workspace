from risk_engine.risk_execution_runtime_v1 import RiskRequest, evaluate_risk


def test_pre2025_real_event_candidate_geometry_passes_risk_runtime():
    """Contract proof using the recovered 2016 candidate geometry.

    Account state is deliberately a test fixture; this is NOT Gate 3C proof.
    The test only proves that the real Risk Engine runtime accepts the
    source-backed candidate SL/TP geometry without imposing an invented RR gate.
    """
    entry = 1.4392
    stop_loss = 1.43778475
    take_profit = 1.4420305
    stop_distance = abs(entry - stop_loss)
    atr = stop_distance / 0.75
    target_distance = abs(take_profit - entry)

    result = evaluate_risk(
        RiskRequest(
            equity=10000.0,              # test fixture only
            risk_percent=0.005,          # frozen supported profile
            entry_price=entry,
            stop_distance=stop_distance,
            take_profit_distance=target_distance,
            stop_mode="structure",
            risk_budget_locked=True,
        ),
        "BUY",
        atr,
    )

    assert result.risk_pass is True
    assert result.reason == "PASS"
    assert result.stop_loss == stop_loss
    assert result.take_profit == take_profit


def test_real_event_candidate_geometry_is_exactly_2r():
    entry = 1.4392
    stop_loss = 1.43778475
    take_profit = 1.4420305
    assert abs((take_profit - entry) / (entry - stop_loss) - 2.0) < 1e-12
