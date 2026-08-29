from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from MTF_SIX_TF_SOURCE_ADAPTER_V1 import SIX_TF, discover, infer_tf_from_text


def _write_ohlc(path: Path, timestamps: list[str], tf: str) -> None:
    pd.DataFrame(
        {
            "timestamp": timestamps,
            "open": [1.0] * len(timestamps),
            "high": [1.1] * len(timestamps),
            "low": [0.9] * len(timestamps),
            "close": [1.05] * len(timestamps),
            "source_tf": [tf] * len(timestamps),
        }
    ).to_csv(path, index=False)


def test_fixed_timeframe_contract() -> None:
    assert SIX_TF == ("M5", "M15", "M30", "H1", "H4", "D1")
    assert infer_tf_from_text("GBPUSD_M15_DATA.csv") == "M15"
    assert infer_tf_from_text("GBPUSD_D1_DATA.csv") == "D1"


def test_discovery_requires_real_csv_content(tmp_path: Path) -> None:
    for tf in SIX_TF:
        _write_ohlc(tmp_path / f"GBPUSD_{tf}_DATA.csv", ["2016-01-04T00:00:00Z", "2016-01-04T00:05:00Z"], tf)

    by_tf, _ = discover(tmp_path, max_rows=10)
    assert all(by_tf[tf] for tf in SIX_TF)
    assert sorted(by_tf) == sorted(SIX_TF)
    for tf in SIX_TF:
        assert by_tf[tf][0]["sampled_rows"] == 2
        assert by_tf[tf][0]["has_2025_sample"] is False


def test_duplicate_timeframe_is_visible(tmp_path: Path) -> None:
    _write_ohlc(tmp_path / "GBPUSD_M5_A.csv", ["2016-01-04T00:00:00Z", "2016-01-04T00:05:00Z"], "M5")
    _write_ohlc(tmp_path / "GBPUSD_M5_B.csv", ["2016-01-04T00:00:00Z", "2016-01-04T00:05:00Z"], "M5")
    by_tf, _ = discover(tmp_path, max_rows=10)
    assert len(by_tf["M5"]) == 2


def test_2025_is_detected_not_relabelled(tmp_path: Path) -> None:
    _write_ohlc(tmp_path / "GBPUSD_M5_DATA.csv", ["2025-01-02T00:00:00Z", "2025-01-02T00:05:00Z"], "M5")
    by_tf, _ = discover(tmp_path, max_rows=10)
    assert by_tf["M5"][0]["has_2025_sample"] is True
