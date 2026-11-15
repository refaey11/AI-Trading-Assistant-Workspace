import importlib.util
from pathlib import Path

import pandas as pd

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "validate_m1_to_mtf_candle_reconciliation_v1.py"
SPEC = importlib.util.spec_from_file_location("m1_mtf_reconciliation", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
reconcile_frames = MODULE.reconcile_frames


def _m1_rows():
    return pd.DataFrame([
        {"timestamp": f"2016-01-03 17:0{i}:00", "open": 1.47335 if i == 0 else 1.47328,
         "high": [1.47335, 1.47336, 1.47335, 1.47333, 1.47334][i],
         "low": [1.47329, 1.47326, 1.47329, 1.47329, 1.47332][i],
         "close": [1.47329, 1.47335, 1.47329, 1.47332, 1.47332][i],
         "volume": 0, "volume_available": False}
        for i in range(5)
    ])


def _actual_row(high=1.47336):
    return pd.DataFrame([{
        "timestamp": "2016-01-03 17:00:00",
        "open": 1.47335,
        "high": high,
        "low": 1.47326,
        "close": 1.47332,
        "volume": 0,
        "m1_count": 5,
        "bar_complete": True,
        "volume_available": False,
    }])


def test_exact_m1_to_m5_ohlc_aggregation_matches():
    result = reconcile_frames(_m1_rows(), _actual_row(), "M5")
    assert result["expected_bars"] == 1
    assert result["matched_timestamps"] == 1
    assert result["full_match_rows"] == 1
    assert result["full_match_rate"] == 1.0


def test_ohlc_mismatch_is_reported_not_repaired():
    result = reconcile_frames(_m1_rows(), _actual_row(high=1.47340), "M5")
    assert result["full_match_rows"] == 0
    assert result["mismatch_samples"][0]["mismatch_fields"] == ["high_match"]


def test_2025_rows_are_excluded_from_development_reconciliation():
    m1 = _m1_rows()
    future = m1.copy()
    future["timestamp"] = future["timestamp"].str.replace("2016", "2025")
    combined = pd.concat([m1, future], ignore_index=True)

    actual = pd.concat([
        _actual_row(),
        _actual_row().assign(timestamp="2025-01-03 17:00:00"),
    ], ignore_index=True)

    result = reconcile_frames(combined, actual, "M5")
    assert result["m1_rows"] == 5
    assert result["expected_bars"] == 1
    assert result["actual_bars"] == 1
    assert result["extra_output_bars"] == 0
