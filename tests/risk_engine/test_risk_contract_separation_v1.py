from RUNTIME.RISK_ENGINE_INTEGRATION_V1.risk_engine_integration_v1 import evaluate_risk as evaluate_canonical_risk
from risk_engine.risk_execution_runtime_v1 import RiskRequest, evaluate_risk as evaluate_candidate_risk


def test_canonical_contract_requires_at_least_3r():
    common = dict(
        equity=10000.0,
        entry=1.25,
        stop_loss=1.2485,
        atr=0.002,
        prior_loss_streak=0,
        peak_equity=10000.0,
    )

    three_r = evaluate_canonical_risk(
        **common,
        take_profit=1.2545,
    )
    two_r = evaluate_canonical_risk(
        **common,
        take_profit=1.2530,
    )
    one_and_half_r = evaluate_canonical_risk(
        **common,
        take_profit=1.25225,
    )

    assert three_r.risk_pass is True
    assert three_r.rr == 3.0
    assert two_r.risk_pass is False
    assert two_r.reason == "RR_BELOW_CURRENT_CANONICAL_MINIMUM"
    assert one_and_half_r.risk_pass is False
    assert one_and_half_r.reason == "RR_BELOW_CURRENT_CANONICAL_MINIMUM"


def test_candidate_evaluation_runtime_accepts_its_frozen_2r_profile():
    request = RiskRequest(
        equity=10000.0,
        risk_percent=0.005,
        entry_price=1.25,
        stop_distance=0.0015,
        take_profit_distance=0.0030,
        stop_mode="structure",
        risk_budget_locked=True,
    )

    result = evaluate_candidate_risk(request, "BUY", atr=0.002)

    assert result.risk_pass is True
    assert result.stop_loss == 1.2485
    assert result.take_profit == 1.253
