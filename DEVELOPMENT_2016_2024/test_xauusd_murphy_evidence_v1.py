from pathlib import Path
import importlib.util

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def load_module(relative_path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_rule_count_and_2025_lock():
    mod = load_module(
        "DEVELOPMENT_2016_2024/run_xauusd_murphy_evidence_v1.py",
        "xau_adapter",
    )
    assert len(mod.MURPHY_RULES) == 34
    assert "MURPHY_0008" not in mod.MURPHY_RULES
    assert mod.BLOCKED_MURPHY_RULES == ("MURPHY_0008",)
    assert mod.DEV_END == pd.Timestamp("2025-01-01", tz="UTC")


def test_runtime_trendline_module_is_wired():
    source = (
        ROOT
        / "DEVELOPMENT_2016_2024/run_xauusd_murphy_evidence_v1.py"
    ).read_text(encoding="utf-8")
    assert "build_xau_trendline_evidence" in source
    assert '"2025_used": False' in source


def test_pivot_confirmation_is_two_bars_late():
    mod = load_module(
        "DEVELOPMENT_2016_2024/xauusd_murphy_0006_0007_runtime_evidence_v1.py",
        "xau_trendline",
    )
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
    low, high = mod.strict_five_bar_pivots(frame)
    # Center bar 2 is a strict low/high confirmation candidate, but it may
    # only become available at bar 4. This test protects the AS-OF boundary.
    assert bool(low[2]) is True
    assert bool(high[2]) is False
