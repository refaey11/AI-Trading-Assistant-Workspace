from core_profitability_eval_v1 import evaluate_event
from frozen_candidate_risk_profile_v1 import evaluate_frozen_candidate_risk


def test_nison_absence_does_not_block_medium_confirmation_path():
    out = evaluate_event({
        "murphy_pass": 1,
        "directional_confirmation": "BULLISH",
        "nison_status": "NOT_EVALUABLE",
        "tiz_process_state": "NOT_EVALUABLE",
        "entry_price": 1.2500,
        "atr20": 0.0100,
    })
    assert out["status"] == "ELIGIBLE_FOR_CORE_PROFITABILITY_BACKTEST"
    assert out["direction"] == "BUY"
    assert out["risk_pass"] is True
    assert out["tiz_verified"] is False


def test_explicit_nison_contradiction_blocks():
    out = evaluate_event({
        "murphy_pass": 1,
        "directional_confirmation": "BEARISH",
        "nison_status": "CONTRADICTORY",
        "entry_price": 1.2500,
        "atr20": 0.0100,
    })
    assert out["status"] == "NO_TRADE"
    assert out["reason"] == "NISON_CONTRADICTION"


def test_frozen_candidate_risk_preserves_existing_075_atr_2r_protocol():
    out = evaluate_frozen_candidate_risk(
        direction="BUY", equity=10000.0, peak_equity=10000.0,
        entry=1.2500, atr=0.0100,
    )
    assert out.risk_pass is True
    assert round(out.stop_loss, 6) == 1.2425
    assert round(out.take_profit, 6) == 1.265
