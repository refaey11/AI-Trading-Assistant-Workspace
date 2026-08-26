from pathlib import Path

import pandas as pd

from OOS_2025.audit_direction_arbitration_2025_v1 import audit


def test_direction_arbitration_separates_neutral_from_opposite(tmp_path, monkeypatch):
    context = pd.DataFrame(
        [
            {"timestamp": "2025-01-01T00:00:00Z", "mtf_trend_score": 0, "M5_trend_regime": 0, "M15_trend_regime": 0, "M30_trend_regime": 0, "H1_trend_regime": 0, "H4_trend_regime": 0, "D1_trend_regime": 0, "volume_available": False},
            {"timestamp": "2025-01-01T01:00:00Z", "mtf_trend_score": 1, "M5_trend_regime": 1, "M15_trend_regime": 1, "M30_trend_regime": 1, "H1_trend_regime": 1, "H4_trend_regime": 1, "D1_trend_regime": 1, "volume_available": False},
        ]
    )
    murphy = pd.DataFrame(
        [
            {"timestamp": "2025-01-01T00:00:00Z", "status": "PASS", "direction": "BULLISH", "source_rule_id": "MURPHY_0021"},
            {"timestamp": "2025-01-01T01:00:00Z", "status": "PASS", "direction": "BEARISH", "source_rule_id": "MURPHY_0021"},
        ]
    )
    risk = pd.DataFrame(
        [
            {"timestamp": "2025-01-01T00:00:00Z", "risk_status": "PASS"},
            {"timestamp": "2025-01-01T01:00:00Z", "risk_status": "PASS"},
        ]
    )
    cp = tmp_path / "context.csv"
    mp = tmp_path / "murphy.csv"
    rp = tmp_path / "risk.csv"
    outj = tmp_path / "audit.json"
    outc = tmp_path / "confusion.csv"
    context.to_csv(cp, index=False)
    murphy.to_csv(mp, index=False)
    risk.to_csv(rp, index=False)

    result = audit(cp, mp, rp, outj, outc)
    assert result["candidate_pass_rows"] == 2
    assert result["risk_pass_candidate_rows"] == 2
    assert "BRAIN_NON_DIRECTIONAL" in result["risk_pass_candidate_direction_relation_counts"]
    assert "OPPOSITE" in result["risk_pass_candidate_direction_relation_counts"]
