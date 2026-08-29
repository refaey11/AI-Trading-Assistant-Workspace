from __future__ import annotations

import ast
import json
from pathlib import Path

from REAL_SOURCE_E2E_PREFLIGHT_V1 import SIX_TF, ast_defines, ast_has_call, infer_timeframes


def test_six_timeframes_are_fixed_contract():
    assert SIX_TF == ("M5", "M15", "M30", "H1", "H4", "D1")


def test_timeframe_inference_is_path_only(tmp_path: Path):
    (tmp_path / "GBPUSD_M5.csv").write_text("timestamp\n", encoding="utf-8")
    (tmp_path / "GBPUSD_M15.csv").write_text("timestamp\n", encoding="utf-8")
    (tmp_path / "GBPUSD_M30.csv").write_text("timestamp\n", encoding="utf-8")
    (tmp_path / "GBPUSD_H1.csv").write_text("timestamp\n", encoding="utf-8")
    (tmp_path / "GBPUSD_H4.csv").write_text("timestamp\n", encoding="utf-8")
    (tmp_path / "GBPUSD_D1.csv").write_text("timestamp\n", encoding="utf-8")
    assert infer_timeframes(tmp_path) == set(SIX_TF)


def test_ast_runner_contract_helpers():
    tree = ast.parse("""
from compatibility.dynamic_mtf_binding_adapter_v1 import bind_dynamic_mtf

def execution_plan(x):
    return x

bind_dynamic_mtf(available_timeframes={'M5'}, role_assignments={})
""")
    assert ast_defines(tree, "execution_plan") is True
    assert ast_has_call(tree, "bind_dynamic_mtf") is True


def test_tiz_boundary_contract_file_is_process_only():
    p = Path(__file__).resolve().parents[1] / "03_TIZ/TIZ_RUNTIME_BOUNDARY_RESOLUTION_V2.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["status"] == "AUTHORITATIVE_BOUNDARY"
    assert data["role"] == "process_only"
    assert data["direction"] == "NEUTRAL"
