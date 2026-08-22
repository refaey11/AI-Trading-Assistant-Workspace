from tiz_preentry_evidence_adapter_v1 import normalize_preentry


def env(value=True):
    return {
        "value": value,
        "availability": True,
        "timestamp": "2025-01-02T12:00:00Z",
        "provenance": "frozen_preentry_source_v1",
        "state_semantics": "explicit_preentry_state",
    }


def test_complete_preentry_evidence_is_preserved_and_neutral():
    record = {"trading_zone": {k: env() for k in (
        "process_state", "rule_adherence", "risk_accepted",
        "impulse_override", "loss_chasing", "revenge_trade")}}
    result = normalize_preentry(record)
    assert result["state"] == "AVAILABLE"
    assert result["missing"] == []
    assert result["direction"] == "NEUTRAL"
    assert result["process_state"]["value"] is True


def test_missing_preentry_evidence_fails_closed():
    result = normalize_preentry({"trading_zone": {"process_state": env()}})
    assert result["state"] == "NOT_EVALUABLE"
    assert "rule_adherence" in result["missing"]
    assert result["direction"] == "NEUTRAL"
