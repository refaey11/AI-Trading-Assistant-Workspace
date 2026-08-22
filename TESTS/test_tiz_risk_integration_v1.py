from RUNTIME.TIZ_PROCESS_GATE_V1.tiz_process_gate_v1 import evaluate_tiz_gate
from RUNTIME.RISK_ENGINE_INTEGRATION_V1.risk_engine_integration_v1 import evaluate_risk


def test_tiz_passes_clean_process():
    r = evaluate_tiz_gate(
        rule_adherence=True,
        risk_accepted=True,
        impulse_override=False,
        loss_chasing=False,
        revenge_trade=False,
    )
    assert r.process_state == "READY"


def test_tiz_blocks_bad_process():
    r = evaluate_tiz_gate(
        rule_adherence=True,
        risk_accepted=True,
        impulse_override=False,
        loss_chasing=True,
        revenge_trade=False,
    )
    assert r.process_state == "NOT_READY"


def test_risk_passes_at_canonical_3r():
    r = evaluate_risk(
        equity=10000,
        entry=100,
        stop_loss=98,
        take_profit=106,
        atr=2,
        prior_loss_streak=0,
        peak_equity=10000,
    )
    assert r.risk_pass is True
    assert abs(r.rr - 3.0) < 1e-12
    assert abs(r.risk_percent - 0.005) < 1e-12


def test_risk_rejects_legacy_1_5r_target():
    r = evaluate_risk(
        equity=10000,
        entry=100,
        stop_loss=98,
        take_profit=103,
        atr=2,
        prior_loss_streak=0,
        peak_equity=10000,
    )
    assert r.risk_pass is False
    assert r.reason == "RR_BELOW_CURRENT_CANONICAL_MINIMUM"


def test_risk_drawdown_breaker():
    r = evaluate_risk(
        equity=9400,
        entry=100,
        stop_loss=98,
        take_profit=106,
        atr=2,
        prior_loss_streak=0,
        peak_equity=10000,
    )
    assert r.risk_pass is False
    assert r.reason == "DRAWDOWN_CIRCUIT_BREAKER"
