from __future__ import annotations

import pandas as pd

from BACKTEST.mtf_source_contract_gate_v1 import diagnose_field


def test_diagnose_field_separates_missing_and_non_numeric_values():
    frame = pd.DataFrame({
        "timestamp": ["2016-01-01T00:00:00Z", "2016-01-01T00:05:00Z", "2016-01-01T00:10:00Z", "2016-01-01T00:15:00Z"],
        "M15_trend_regime": [1.0, None, "   ", "BULL_TREND"],
    })

    result = diagnose_field(frame, "M15_trend_regime")

    assert result["missing_count"] == 2
    assert result["non_numeric_count"] == 1
    assert len(result["missing_samples"]) == 2
    assert len(result["non_numeric_samples"]) == 1
    assert result["non_numeric_samples"][0]["M15_trend_regime"] == "BULL_TREND"


def test_diagnose_field_accepts_numeric_strings():
    frame = pd.DataFrame({"M15_trend_regime": ["1", "-1", "0"]})

    result = diagnose_field(frame, "M15_trend_regime")

    assert result["missing_count"] == 0
    assert result["non_numeric_count"] == 0
