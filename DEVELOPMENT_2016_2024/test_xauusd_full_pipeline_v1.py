from pathlib import Path

import pandas as pd

from DEVELOPMENT_2016_2024.run_xauusd_full_pipeline_v1 import (
    DEV_END,
    DEV_START,
    normalize_nison_direction,
    split_mtf_source,
    trend_for_nison,
)

ROOT = Path(__file__).resolve().parents[1]


def test_frozen_window_and_direction_normalization():
    assert DEV_START == pd.Timestamp("2016-01-01", tz="UTC")
    assert DEV_END == pd.Timestamp("2025-01-01", tz="UTC")
    assert normalize_nison_direction("BUY_CANDIDATE") == "BULLISH"
    assert normalize_nison_direction("SELL_CANDIDATE") == "BEARISH"
    assert normalize_nison_direction("UNKNOWN") is None


def test_nison_trend_mapping_is_source_only():
    assert trend_for_nison("BULL_TREND") == "Uptrend"
    assert trend_for_nison("BEAR_TREND") == "Downtrend"
    assert trend_for_nison("TRANSITION") == ""


def test_mtf_split_requires_explicit_source_trends(tmp_path: Path):
    ts = pd.date_range("2024-01-01", periods=2, freq="h", tz="UTC")
    src = pd.DataFrame(
        {
            "timestamp": ts,
            "H1_trend": ["BULL_TREND", "BEAR_TREND"],
            "H4_trend": ["BULL_TREND", "TRANSITION"],
        }
    )
    out = split_mtf_source(src, tmp_path)
    h1 = pd.read_csv(out / "H1/XAUUSD_H1.csv")
    h4 = pd.read_csv(out / "H4/XAUUSD_H4.csv")
    assert list(h1["trend"]) == ["BULL_TREND", "BEAR_TREND"]
    assert list(h4["trend"]) == ["BULL_TREND", "TRANSITION"]


def test_2025_lock_in_source_contract():
    source = (
        ROOT / "DEVELOPMENT_2016_2024/run_xauusd_full_pipeline_v1.py"
    ).read_text(encoding="utf-8")
    assert 'DEV_END = pd.Timestamp("2025-01-01", tz="UTC")' in source
    assert '"2025_used": False' in source
    assert "XAUUSD_MTF_H4_H1.csv" in source
    assert "XAUUSD_MARKET_STATE.csv" in source
