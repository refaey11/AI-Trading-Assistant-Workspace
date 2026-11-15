from __future__ import annotations

import importlib.util
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


risk_builder = load(ROOT / "OOS_2025" / "build_single_event_risk_evidence_v1.py", "test_gate3c_risk_builder")
e2e = load(ROOT / "RUNTIME" / "DECISION_RUNTIME_V1" / "gate3c_single_event_e2e_v1.py", "test_gate3c_e2e")

TS = pd.Timestamp("2020-01-02T01:00:00Z")


def write_registry(path: Path):
    pd.DataFrame([
        {"rule_id": "MURPHY_0021", "historical_status": "SOURCE_BACKED_HISTORICAL_EVALUATION", "decision_eligible": "YES"},
        {"rule_id": "MURPHY_0025", "historical_status": "SOURCE_BACKED_FEATURE_REPLAY", "decision_eligible": "YES"},
        {"rule_id": "MURPHY_0003", "historical_status": "OBSERVED_BUT_NOT_DECISION_ELIGIBLE", "decision_eligible": "NO"},
    ]).to_csv(path, index=False)


def test_selector_accepts_only_registry_eligible_directional_pass(tmp_path):
    evidence = tmp_path / "murphy.csv"
    registry = tmp_path / "registry.csv"
    write_registry(registry)
    pd.DataFrame([
        {"timestamp": TS.isoformat(), "status": "PASS", "direction": "BULLISH",
         "source_rule_id": "MURPHY_0025", "pass_rule_id": "MURPHY_0025"},
        {"timestamp": TS.isoformat(), "status": "PASS", "direction": "BULLISH",
         "source_rule_id": "MURPHY_0021|MURPHY_0022|MURPHY_0023", "pass_rule_id": "MURPHY_0021"},
    ]).to_csv(evidence, index=False)

    selected = risk_builder._one_directional_murphy_row(evidence, TS, registry)
    assert selected["pass_rule_id"] == "MURPHY_0021"


def test_selector_rejects_context_only_pass(tmp_path):
    evidence = tmp_path / "murphy.csv"
    registry = tmp_path / "registry.csv"
    write_registry(registry)
    pd.DataFrame([
        {"timestamp": TS.isoformat(), "status": "PASS", "direction": "BULLISH",
         "source_rule_id": "MURPHY_0025", "pass_rule_id": "MURPHY_0025"},
    ]).to_csv(evidence, index=False)

    with pytest.raises(ValueError, match="registry-eligible directional PASS"):
        risk_builder._one_directional_murphy_row(evidence, TS, registry)


def test_selector_rejects_pass_rule_not_in_source_provenance(tmp_path):
    evidence = tmp_path / "murphy.csv"
    registry = tmp_path / "registry.csv"
    write_registry(registry)
    pd.DataFrame([
        {"timestamp": TS.isoformat(), "status": "PASS", "direction": "BULLISH",
         "source_rule_id": "MURPHY_0022|MURPHY_0023", "pass_rule_id": "MURPHY_0021"},
    ]).to_csv(evidence, index=False)

    with pytest.raises(ValueError, match="registry-eligible directional PASS"):
        risk_builder._one_directional_murphy_row(evidence, TS, registry)


def test_murphy_and_risk_direction_must_match():
    murphy = {"direction": "BUY", "pass_rule_id": "MURPHY_0021",
              "directional_source_rule_id": "MURPHY_0021|MURPHY_0022|MURPHY_0023"}
    risk = {"direction": "BUY", "pass_rule_id": "MURPHY_0021",
            "directional_source_rule_id": "MURPHY_0021|MURPHY_0022|MURPHY_0023"}
    rows = [{"source_rule_id": "MURPHY_0021|MURPHY_0022|MURPHY_0023"}]
    assert e2e._murphy_risk_direction_contract(murphy, risk, rows) is None


def test_murphy_and_risk_direction_conflict_is_blocked():
    murphy = {"direction": "BUY", "pass_rule_id": "MURPHY_0021",
              "directional_source_rule_id": "MURPHY_0021|MURPHY_0022|MURPHY_0023"}
    risk = {"direction": "SELL", "pass_rule_id": "MURPHY_0021",
            "directional_source_rule_id": "MURPHY_0021|MURPHY_0022|MURPHY_0023"}
    rows = [{"source_rule_id": "MURPHY_0021|MURPHY_0022|MURPHY_0023"}]
    assert e2e._murphy_risk_direction_contract(murphy, risk, rows) == "MURPHY_RISK_DIRECTION_CONFLICT"


def test_murphy_and_risk_pass_rule_must_match():
    murphy = {"direction": "BUY", "pass_rule_id": "MURPHY_0021",
              "directional_source_rule_id": "MURPHY_0021|MURPHY_0022|MURPHY_0023"}
    risk = {"direction": "BUY", "pass_rule_id": "MURPHY_0022",
            "directional_source_rule_id": "MURPHY_0021|MURPHY_0022|MURPHY_0023"}
    rows = [{"source_rule_id": "MURPHY_0021|MURPHY_0022|MURPHY_0023"}]
    assert e2e._murphy_risk_direction_contract(murphy, risk, rows) == "MURPHY_RISK_PASS_RULE_MISMATCH"
