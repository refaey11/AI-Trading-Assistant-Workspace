from __future__ import annotations

from pathlib import Path

import pandas as pd

from MTF_SIX_TF_SOURCE_ADAPTER_V1 import SIX_TF, discover, infer_tf_from_text, timestamp_series


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

    by_tf, _, out_of_scope = discover(tmp_path, max_rows=10)
    assert out_of_scope == []
    assert all(by_tf[tf] for tf in SIX_TF)
    assert sorted(by_tf) == sorted(SIX_TF)
    for tf in SIX_TF:
        assert by_tf[tf][0]["sampled_rows"] == 2
        assert by_tf[tf][0]["has_2025_sample"] is False


def test_noncanonical_symbol_is_out_of_scope(tmp_path: Path) -> None:
    for tf in ("M5",):
        _write_ohlc(tmp_path / f"EURUSD_{tf}_DATA.csv", ["2016-01-04T00:00:00Z", "2016-01-04T00:05:00Z"], tf)

    by_tf, _, out_of_scope = discover(tmp_path, max_rows=10)
    assert by_tf["M5"] == []
    assert len(out_of_scope) == 1


def test_duplicate_canonical_timeframe_is_visible(tmp_path: Path) -> None:
    _write_ohlc(tmp_path / "GBPUSD_M5_A.csv", ["2016-01-04T00:00:00Z", "2016-01-04T00:05:00Z"], "M5")
    _write_ohlc(tmp_path / "GBPUSD_M5_B.csv", ["2016-01-04T00:00:00Z", "2016-01-04T00:05:00Z"], "M5")
    by_tf, _, out_of_scope = discover(tmp_path, max_rows=10)
    assert out_of_scope == []
    assert len(by_tf["M5"]) == 2


def test_2025_is_detected_not_relabelled(tmp_path: Path) -> None:
    _write_ohlc(tmp_path / "GBPUSD_M5_DATA.csv", ["2025-01-02T00:00:00Z", "2025-01-02T00:05:00Z"], "M5")
    by_tf, _, _ = discover(tmp_path, max_rows=10)
    assert by_tf["M5"][0]["has_2025_sample"] is True


def test_date_and_time_are_combined_without_using_bare_time(tmp_path: Path) -> None:
    frame = pd.DataFrame({"Date": ["2016-01-04", "2016-01-04"], "Time": ["00:00:00", "00:05:00"]})
    ts, label = timestamp_series(frame)
    assert label == "Date+Time"
    assert ts.dt.year.tolist() == [2016, 2016]
    assert ts.dt.minute.tolist() == [0, 5]

    bare = pd.DataFrame({"Time": ["00:00:00", "00:05:00"]})
    try:
        timestamp_series(bare)
    except ValueError as exc:
        assert "timestamp" in str(exc).lower() or "date+time" in str(exc).lower()
    else:
        raise AssertionError("bare time must not be accepted as a full timestamp")
