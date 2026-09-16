from __future__ import annotations

from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "BACKTEST" / "DEV_BACKTEST_RUNNER_GOVERNED_V2.py"


def load_runner():
    spec = importlib.util.spec_from_file_location("governed_runner", RUNNER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_runner_signature_defaults_tiz_to_optional():
    r = load_runner()
    assert "tiz_mode" in r.run.__code__.co_varnames
    assert r.run.__defaults__[-1] == "optional"


def test_runner_source_passes_tiz_mode_to_gate():
    source = RUNNER.read_text(encoding="utf-8")
    assert "tiz_mode=tiz_mode" in source
    assert "if tiz_mode == \"strict\" and tiz_value == \"NOT_EVALUABLE\":" in source or "tiz_mode == \"strict\"" in source
