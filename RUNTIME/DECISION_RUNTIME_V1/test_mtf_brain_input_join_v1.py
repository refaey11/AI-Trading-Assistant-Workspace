from __future__ import annotations

import importlib.util
from pathlib import Path

import pandas as pd
import pytest

MODULE_PATH = Path(__file__).with_name("mtf_brain_input_join_v1.py")
spec = importlib.util.spec_from_file_location("mtf_join", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def _events(values):
    return pd.DataFrame({"timestamp": pd.to_datetime(values, utc=True)})


def _mtf(values):
    base = {
        "timestamp": pd.to_datetime(values, utc=True),
        "mtf_trend_score": [0.25, 0.50],
        "M5_trend_regime": [1.0, 1.0],
        "M15_trend_regime": [1.0, 1.0],
        "M30_trend_regime": [1.0, 1.0],
        "H1_trend_regime": [1.0, 1.0],
        "H4_trend_regime": [1.0, 1.0],
        "D1_trend_regime": [1.0, 1.0],
    }
    return pd.DataFrame(base)


def test_exact_or_backward_asof_join():
    events = _events(["2016-01-08 06:00:00", "2016-01-08 06:10:00"])
    mtf = _mtf(["2016-01-08 05:55:00", "2016-01-08 06:05:00"])
    out = module.join_mtf_to_events(events, mtf)
    assert len(out) == 2
    assert out.loc[0, "mtf_trend_score"] == 0.25
    assert out.loc[1, "mtf_trend_score"] == 0.50


def test_missing_brain_field_fails_closed():
    events = _events(["2016-01-08 06:00:00"])
    mtf = _mtf(["2016-01-08 05:55:00", "2016-01-08 06:05:00"]).drop(columns=["D1_trend_regime"])
    with pytest.raises(ValueError, match="missing required columns"):
        module.join_mtf_to_events(events, mtf)


def test_future_only_mtf_input_fails_closed():
    events = _events(["2016-01-08 06:00:00"])
    mtf = _mtf(["2016-01-08 06:05:00", "2016-01-08 06:10:00"])
    with pytest.raises(ValueError, match="MISSING_SOURCE_BACKED_MTF_INPUT"):
        module.join_mtf_to_events(events, mtf)


def test_duplicates_fail_closed():
    events = _events(["2016-01-08 06:00:00"])
    mtf = _mtf(["2016-01-08 05:55:00", "2016-01-08 05:55:00"])
    with pytest.raises(ValueError, match="duplicate timestamps"):
        module.join_mtf_to_events(events, mtf)
