import pandas as pd

from OOS_2025.nison_2025_evidence_aggregate_v1 import aggregate_nison_evidence


def test_directional_pass_creates_confirmation_only_from_existing_pass():
    evidence = pd.DataFrame(
        [
            {"timestamp": "2025-01-01T00:00:00Z", "rule_id": "NISON_0001", "status": "PASS", "direction": "BULLISH"},
            {"timestamp": "2025-01-01T00:00:00Z", "rule_id": "NISON_0002", "status": "FAIL", "direction": "UNKNOWN"},
        ]
    )
    out = aggregate_nison_evidence(evidence).iloc[0]
    assert out["confirmation"] == "BULLISH"
    assert bool(out["confirmation_available"]) is True
    assert bool(out["contradiction"]) is False


def test_missing_directional_pass_stays_absent():
    evidence = pd.DataFrame(
        [
            {"timestamp": "2025-01-01T00:00:00Z", "rule_id": "NISON_0003", "status": "FAIL", "direction": "UNKNOWN"},
            {"timestamp": "2025-01-01T00:00:00Z", "rule_id": "NISON_0031", "status": "NOT_EVALUABLE", "direction": "UNKNOWN"},
        ]
    )
    out = aggregate_nison_evidence(evidence).iloc[0]
    assert out["confirmation"] == "ABSENT"
    assert bool(out["confirmation_available"]) is False
    assert bool(out["contradiction"]) is False


def test_explicit_directional_fail_is_contradiction_evidence():
    evidence = pd.DataFrame(
        [
            {"timestamp": "2025-01-01T00:00:00Z", "rule_id": "NISON_0002", "status": "FAIL", "direction": "BEARISH"},
        ]
    )
    out = aggregate_nison_evidence(evidence).iloc[0]
    assert out["confirmation"] == "ABSENT"
    assert bool(out["contradiction"]) is True
