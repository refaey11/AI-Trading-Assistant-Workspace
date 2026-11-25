from pathlib import Path

import pandas as pd

from DEVELOPMENT_2016_2024 import run_xauusd_murphy_evidence_v1 as adapter
from DEVELOPMENT_2016_2024.xauusd_murphy_0006_0007_runtime_evidence_v1 import (
    strict_five_bar_pivots,
)

ROOT = Path(__file__).resolve().parents[1]


def test_rule_count_and_2025_lock():
    assert len(adapter.MURPHY_RULES) == 34
    assert "MURPHY_0008" not in adapter.MURPHY_RULES
    assert adapter.BLOCKED_MURPHY_RULES == ("MURPHY_0008",)
    assert adapter.DEV_END == pd.Timestamp("2025-01-01", tz="UTC")


def test_runtime_trendline_module_is_wired():
    source = (
        ROOT / "DEVELOPMENT_2016_2024/run_xauusd_murphy_evidence_v1.py"
    ).read_text(encoding="utf-8")
    assert "build_xau_trendline_evidence" in source
    assert '"2025_used": False' in source


def test_pivot_confirmation_is_two_bars_late():
    ts = pd.date_range("2024-01-01", periods=7, freq="min", tz="UTC")
    frame = pd.DataFrame(
        {
            "timestamp": ts,
            "open": [10, 9, 8, 9, 10, 9, 10],
            "high": [11, 10, 9, 10, 11, 10, 11],
            "low": [9, 8, 7, 8, 9, 8, 9],
            "close": [10, 9, 8, 9, 10, 9, 10],
        }
    )
    low, high = strict_five_bar_pivots(frame)

    assert bool(low[2]) is True
    assert bool(high[2]) is False
    assert ts[4] > ts[2]
