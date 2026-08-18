from tiz_runtime_bridge_candidate_v1 import normalize, can_generate_direction


def test_missing_evidence_is_not_evaluable():
    result = normalize({"trading_zone": {}})
    assert all(v["state"] == "NOT_EVALUABLE" for v in result["rules"].values())


def test_direction_is_always_neutral():
    assert can_generate_direction() is False
    assert normalize({})["direction"] == "NEUTRAL"


def test_complete_evidence_can_be_available_without_generating_direction():
    meta = {"value": True, "availability": True, "timestamp": "2026-08-18T00:00:00Z", "provenance": "test", "state_semantics": "boolean"}
    runtime = {"trading_zone": {
        "pre_trade_state_gate": meta,
        "risk_acceptance": meta,
        "post_trade_review": meta,
        "loss_sequence_control": meta,
        "rule_adherence": meta,
        "no_impulsive_override": meta,
    }}
    result = normalize(runtime)
    assert result["direction"] == "NEUTRAL"
    assert all(v["state"] == "AVAILABLE" for v in result["rules"].values())
