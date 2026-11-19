from __future__ import annotations

import importlib.util
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "BACKTEST" / "DEV_BACKTEST_RUNNER_V1.py"
SPEC = importlib.util.spec_from_file_location("dev_backtest_runner_mtf_safety", RUNNER_PATH)
assert SPEC and SPEC.loader
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def valid_mtf(**overrides):
    row = {
        "mtf_trend_score": 2,
        "M5_trend_regime": 1,
        "M15_trend_regime": 1,
        "M30_trend_regime": 0,
        "H1_trend_regime": -1,
        "H4_trend_regime": 1,
        "D1_trend_regime": 0,
    }
    row.update(overrides)
    return row


def test_timestamp_parser_rejects_naive_values():
    values = pd.Series(["2024-01-02 10:00:00"])
    with pytest.raises(ValueError, match="TIMEZONE_PROVENANCE_UNRESOLVED_NAIVE_TIMESTAMP"):
        runner._parse_aware_timestamps(values, label="fixture")


def test_timestamp_parser_normalizes_explicit_offsets_to_utc():
    values = pd.Series(["2024-01-02T12:00:00+02:00"])
    parsed = runner._parse_aware_timestamps(values, label="fixture")
    assert str(parsed.iloc[0]) == "2024-01-02 10:00:00+00:00"


def test_read_csv_rejects_naive_source_timestamps(tmp_path):
    path = tmp_path / "source.csv"
    pd.DataFrame({"timestamp": ["2024-01-02 10:00:00"], "value": [1]}).to_csv(path, index=False)
    with pytest.raises(ValueError, match="TIMEZONE_PROVENANCE_UNRESOLVED_NAIVE_TIMESTAMP"):
        runner.read_csv(path, {"timestamp", "value"})


def test_read_csv_rejects_duplicate_aware_timestamps(tmp_path):
    path = tmp_path / "source.csv"
    pd.DataFrame({
        "timestamp": ["2024-01-02T10:00:00Z", "2024-01-02T10:00:00Z"],
        "value": [1, 2],
    }).to_csv(path, index=False)
    with pytest.raises(ValueError, match="duplicate timestamps"):
        runner.read_csv(path, {"timestamp", "value"})


def test_build_row_copies_all_seven_canonical_fields_without_recoding():
    source = valid_mtf()
    result = runner.build_row({"trend": "BEAR_TREND"}, source)
    for field in runner.REQUIRED_MTF_FIELDS:
        assert result[field] == float(source[field])
    assert result["H1_trend_regime"] == -1.0
    assert result["mtf_trend_score"] == 2.0
    assert result["volume_available"] is False
    assert "atr" not in result


def test_build_row_does_not_fabricate_missing_values_as_zero():
    source = valid_mtf(D1_trend_regime="")
    with pytest.raises(ValueError, match="MISSING_OR_BLANK:D1_trend_regime"):
        runner.build_row({}, source)


def test_build_row_rejects_non_numeric_or_non_finite_values():
    with pytest.raises(ValueError, match="NON_NUMERIC:M5_trend_regime"):
        runner.build_row({}, valid_mtf(M5_trend_regime="BULL_TREND"))
    with pytest.raises(ValueError, match="NON_FINITE:M5_trend_regime"):
        runner.build_row({}, valid_mtf(M5_trend_regime=float("nan")))


def test_build_row_rejects_legacy_alias_only_input():
    with pytest.raises(ValueError, match="MISSING_OR_BLANK:mtf_trend_score"):
        runner.build_row({}, {"trend": "BULL_TREND", "h4_trend": "BEAR_TREND"})


def test_build_row_rejects_missing_asof_source_row():
    with pytest.raises(ValueError, match="NO_ASOF_SOURCE_ROW"):
        runner.build_row({}, {})
