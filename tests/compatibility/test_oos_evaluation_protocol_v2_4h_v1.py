import json
from pathlib import Path


def test_v2_4h_oos_protocol_is_frozen_but_not_official():
    root = Path(__file__).parents[2]
    config = json.loads((root / "governance/OOS_EVALUATION_PROTOCOL_V2_4H_V1.json").read_text(encoding="utf-8"))
    assert config["status"] == "FROZEN_FOR_OOS_EVALUATION_ONLY"
    assert config["not_official_baseline"] is True
    assert config["stop_loss"]["multiplier"] == 0.75
    assert config["take_profit"]["multiple"] == 2.0
    assert config["governance"]["2025_oos_locked"] is True
    assert config["governance"]["official_baseline_claim"] is False


def test_execution_risk_profile_is_not_strategy_tuning():
    root = Path(__file__).parents[2]
    config = json.loads((root / "governance/OOS_EVALUATION_PROTOCOL_V2_4H_V1.json").read_text(encoding="utf-8"))
    assert config["execution_risk"]["risk_percent"] == 0.005
    assert config["execution_risk"]["strategy_parameter"] is False
