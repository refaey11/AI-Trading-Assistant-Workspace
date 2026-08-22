import pandas as pd
from OOS_2025.oos_2025_evidence_assembler_v1 import build_from_frames


def test_assembler_keeps_2025_scope_and_fails_closed():
    market = pd.DataFrame([
        {'timestamp':'2025-01-02T00:00:00Z','trend':'BEAR_TREND','structure_event':'INSIDE_RANGE','location':'NEAR_SUPPORT','volatility_state':'NORMAL','volume_state':'CONTRACTION','atr20':0.001},
        {'timestamp':'2024-12-31T00:00:00Z','trend':'BULL_TREND','structure_event':'BREAKOUT','location':'MID_RANGE','volatility_state':'NORMAL','volume_state':'NORMAL','atr20':0.002},
    ])
    mtf = pd.DataFrame([
        {'timestamp':'2025-01-02T00:00:00Z','mtf_state':'ALIGNED_BEAR','h4_trend':'BEAR_TREND','h4_structure':'INSIDE_RANGE'},
    ])
    smoke = pd.DataFrame([
        {'timestamp':'2025-01-02T00:00:00Z','status':'PASS','directional_confirmation':'BEARISH','rule_id':'MURPHY_0021'},
    ])
    out = build_from_frames(market, mtf, smoke)
    assert len(out) == 1
    assert out.iloc[0]['mtf_state'] == 'ALIGNED_BEAR'
    assert out.iloc[0]['murphy_pass'] == 1
    assert out.iloc[0]['nison_status'] == 'NOT_EVALUABLE'
    assert out.iloc[0]['tiz_process_state'] == 'NOT_EVALUABLE'
    assert out.iloc[0]['risk_pass'] is False
    assert out.iloc[0]['missing_authoritative'] == 'nison_evidence|tiz_evidence|risk_evidence'
