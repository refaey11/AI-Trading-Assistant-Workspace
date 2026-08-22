import json
from pathlib import Path

ALLOWLIST = Path("governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json")


def test_allowlist_count_and_partition():
    data = json.loads(ALLOWLIST.read_text(encoding="utf-8"))
    murphy = data["verified_runtime"]["MURPHY"]
    nison = data["verified_runtime"]["NISON"]
    assert len(murphy) == 34
    assert len(nison) == 44
    assert len(set(murphy + nison)) == 78
    assert data["verified_runtime_count"] == 78


def test_explicitly_blocked_rule_is_not_eligible():
    data = json.loads(ALLOWLIST.read_text(encoding="utf-8"))
    verified = set(data["verified_runtime"]["MURPHY"] + data["verified_runtime"]["NISON"])
    assert "MURPHY_0008" not in verified
    assert data["explicitly_blocked"][0]["rule_id"] == "MURPHY_0008"
    assert data["governance"]["deny_by_default"] is True


def test_unknown_rule_ids_are_denied_by_default():
    data = json.loads(ALLOWLIST.read_text(encoding="utf-8"))
    verified = set(data["verified_runtime"]["MURPHY"] + data["verified_runtime"]["NISON"])
    for rule_id in ("MURPHY_9999", "NISON_9999", "TIZ_0001"):
        assert rule_id not in verified
    assert data["governance"]["unknown_rule_id"] == "REJECT"


def test_2025_remains_oos():
    data = json.loads(ALLOWLIST.read_text(encoding="utf-8"))
    assert data["governance"]["2025_oos"] is True
