import pandas as pd

from full_78_event_orchestrator_v1 import ALL_RULES, build_frozen_events


def test_missing_rules_never_become_eligible():
    market = pd.DataFrame({"timestamp": ["2025-01-01T10:00:00Z"]})
    rule_output = pd.DataFrame([
        {"timestamp": "2025-01-01T10:00:00Z", "rule_id": "MURPHY_0003", "status": "PASS", "directional_confirmation": "BULLISH"},
    ])
    risk = pd.DataFrame([{"timestamp": "2025-01-01T10:00:00Z", "risk_pass": True, "stop_loss": 1.2, "take_profit": 1.3, "position_size": 10.0}])
    out = build_frozen_events(market, rule_output, risk)
    assert len(ALL_RULES) == 78
    assert out.loc[0, "missing_rule_count"] == 77
    assert out.loc[0, "eligible"] is False


def test_full_rule_payload_can_be_eligible_without_tiz_inference():
    ts = "2025-01-01T10:00:00Z"
    rules = []
    for rule_id in sorted(ALL_RULES):
        rules.append({"timestamp": ts, "rule_id": rule_id, "status": "PASS", "directional_confirmation": "BULLISH" if rule_id == "MURPHY_0003" else ""})
    market = pd.DataFrame({"timestamp": [ts]})
    risk = pd.DataFrame([{"timestamp": ts, "risk_pass": True, "stop_loss": 1.2, "take_profit": 1.3, "position_size": 10.0}])
    out = build_frozen_events(market, pd.DataFrame(rules), risk)
    assert out.loc[0, "missing_rule_count"] == 0
    assert out.loc[0, "eligible"] is True
    assert out.loc[0, "direction"] == "BUY"


def test_nison_contradiction_blocks_even_when_all_rules_present():
    ts = "2025-01-01T10:00:00Z"
    rules = []
    for rule_id in sorted(ALL_RULES):
        status = "CONTRADICTORY" if rule_id == "NISON_0001" else "PASS"
        rules.append({"timestamp": ts, "rule_id": rule_id, "status": status, "directional_confirmation": "BULLISH" if rule_id == "MURPHY_0003" else ""})
    market = pd.DataFrame({"timestamp": [ts]})
    risk = pd.DataFrame([{"timestamp": ts, "risk_pass": True}])
    out = build_frozen_events(market, pd.DataFrame(rules), risk)
    assert out.loc[0, "eligible"] is False
    assert out.loc[0, "nison_contradiction"] is True
