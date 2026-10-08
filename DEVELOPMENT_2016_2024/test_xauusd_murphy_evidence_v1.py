from pathlib import Path
import importlib.util
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("xau_adapter",ROOT/"DEVELOPMENT_2016_2024"/"run_xauusd_murphy_evidence_v1.py")
MOD=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(MOD)

def test_rule_count_and_2025_lock():
    assert len(MOD.MURPHY_RULES)==35
    assert MOD.DEV_END == pd.Timestamp("2025-01-01",tz="UTC")

def test_fail_closed_rules_are_explicit():
    assert {"MURPHY_0006","MURPHY_0007","MURPHY_0039","MURPHY_0042","MURPHY_0043","MURPHY_0044","MURPHY_0045"}.issubset(set(MOD.MURPHY_RULES))

def test_adapter_has_no_synthetic_geometry():
    source=(ROOT/"DEVELOPMENT_2016_2024"/"run_xauusd_murphy_evidence_v1.py").read_text(encoding="utf-8")
    assert "Requires source-backed event/line geometry" in source
    assert '"2025_used":False' in source
