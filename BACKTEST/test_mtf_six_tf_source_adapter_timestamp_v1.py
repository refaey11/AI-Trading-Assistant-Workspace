from __future__ import annotations

import importlib.util
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "BACKTEST" / "MTF_SIX_TF_SOURCE_ADAPTER_V1.py"
SPEC = importlib.util.spec_from_file_location("mtf_six_tf_source_adapter", MODULE_PATH)
assert SPEC and SPEC.loader
adapter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(adapter)


def test_timestamp_series_rejects_naive_timestamp_column():
    frame = pd.DataFrame({"timestamp": ["2024-01-02 10:00:00"]})
    with pytest.raises(ValueError, match="TIMEZONE_PROVENANCE_UNRESOLVED_NAIVE_TIMESTAMP"):
        adapter.timestamp_series(frame)


def test_timestamp_series_normalizes_explicit_offset_to_utc():
    frame = pd.DataFrame({"timestamp": ["2024-01-02T12:00:00+02:00"]})
    parsed, column = adapter.timestamp_series(frame)
    assert column == "timestamp"
    assert str(parsed.iloc[0]) == "2024-01-02 10:00:00+00:00"


def test_timestamp_series_rejects_mixed_aware_and_naive_values():
    frame = pd.DataFrame({"timestamp": ["2024-01-02T12:00:00Z", "2024-01-02 13:00:00"]})
    with pytest.raises(ValueError, match="TIMEZONE_PROVENANCE_UNRESOLVED_NAIVE_TIMESTAMP"):
        adapter.timestamp_series(frame)


def test_date_time_columns_must_include_explicit_timezone():
    frame = pd.DataFrame({"date": ["2024-01-02"], "time": ["10:00:00"]})
    with pytest.raises(ValueError, match="TIMEZONE_PROVENANCE_UNRESOLVED_NAIVE_TIMESTAMP"):
        adapter.timestamp_series(frame)


def test_inspect_csv_rejects_naive_source_before_reporting_pass(tmp_path):
    path = tmp_path / "GBPUSD_M5.csv"
    pd.DataFrame({
        "timestamp": ["2024-01-02 10:00:00"],
        "open": [1.1], "high": [1.2], "low": [1.0], "close": [1.15],
    }).to_csv(path, index=False)
    with pytest.raises(ValueError, match="TIMEZONE_PROVENANCE_UNRESOLVED_NAIVE_TIMESTAMP"):
        adapter.inspect_csv(path, max_rows=10)


def test_inspect_csv_accepts_explicit_offset_and_preserves_utc(tmp_path):
    path = tmp_path / "GBPUSD_M5.csv"
    pd.DataFrame({
        "timestamp": ["2024-01-02T12:00:00+02:00"],
        "open": [1.1], "high": [1.2], "low": [1.0], "close": [1.15],
    }).to_csv(path, index=False)
    result = adapter.inspect_csv(path, max_rows=10)
    assert result["sampled_min_timestamp"] == "2024-01-02T10:00:00+00:00"
    assert result["sampled_years"] == [2024]
