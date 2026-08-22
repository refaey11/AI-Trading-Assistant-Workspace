from compatibility.rule_adapter_allowlist_runtime_gate_v1 import gate_rule_result


def test_verified_rule_is_eligible():
    out = gate_rule_result({"source_rule_id": "NISON_0031"})
    assert out["eligible"] is True
    assert out["status"] == "PASS"


def test_murphy_0008_is_rejected():
    out = gate_rule_result({"source_rule_id": "MURPHY_0008"})
    assert out["eligible"] is False
    assert out["status"] == "REJECT"
    assert out["reason"] == "RULE_NOT_IN_FROZEN_ALLOWLIST"


def test_unknown_rule_is_rejected():
    out = gate_rule_result({"source_rule_id": "NISON_9999"})
    assert out["eligible"] is False
    assert out["status"] == "REJECT"


def test_missing_rule_id_is_rejected():
    out = gate_rule_result({})
    assert out["eligible"] is False
    assert out["status"] == "REJECT"
