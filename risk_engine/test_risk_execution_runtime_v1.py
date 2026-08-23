from risk_execution_runtime_v1 import RiskRequest, evaluate_risk

def req(**overrides):
    data = dict(equity=10000.0, risk_percent=0.005, entry_price=1.2500, stop_distance=0.0050, take_profit_distance=0.0075, stop_mode="structure", risk_budget_locked=True)
    data.update(overrides)
    return RiskRequest(**data)

def test_valid_buy_passes():
    r = evaluate_risk(req(), "BUY", 0.005)
    assert r.risk_pass is True
    assert round(r.risk_money, 6) == 50.0
    assert round(r.position_size, 6) == 10000.0
    assert round(r.stop_loss, 6) == 1.245
    assert round(r.take_profit, 6) == 1.2575

def test_sl_outside_atr_range_fails():
    r = evaluate_risk(req(stop_distance=0.0005), "BUY", 0.005)
    assert r.risk_pass is False
    assert r.reason == "STOP_DISTANCE_OUTSIDE_0_5_TO_4_ATR"

def test_missing_tp_fails():
    r = evaluate_risk(req(take_profit_distance=0.0), "BUY", 0.005)
    assert r.risk_pass is False
    assert r.reason == "TAKE_PROFIT_UNDEFINED"

def test_unlocked_budget_fails():
    r = evaluate_risk(req(risk_budget_locked=False), "BUY", 0.005)
    assert r.risk_pass is False
    assert r.reason == "RISK_BUDGET_NOT_LOCKED"

def test_unsupported_profile_fails_closed():
    r = evaluate_risk(req(risk_percent=0.0075), "BUY", 0.005)
    assert r.risk_pass is False
    assert r.reason == "RISK_PROFILE_NOT_FROZEN"
