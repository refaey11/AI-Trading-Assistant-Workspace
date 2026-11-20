from __future__ import annotations

import importlib.util
from pathlib import Path

import pandas as pd
import pytest


MODULE_PATH = Path(__file__).with_name("mtf_brain_input_join_v1.py")
SPEC = importlib.util.spec_from_file_location("mtf_brain_input_join_v1", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_explicit_offsets_are_normalized_to_utc() -> None:
    values = pd.Series(["2024-01-02T10:00:00+02:00", "2024-01-02T09:00:00Z"])
    parsed = MODULE._parse_aware_timestamps(values, label="test")
    assert str(parsed.dt.tz) == "UTC"
    assert parsed.iloc[0] == pd.Timestamp("2024-01-02T08:00:00Z")
    assert parsed.iloc[1] == pd.Timestamp("2024-01-02T09:00:00Z")


def test_naive_timestamp_is_rejected() -> None:
    values = pd.Series(["2024-01-02 10:00:00"])
    with pytest.raises(ValueError, match="TIMEZONE_PROVENANCE_UNRESOLVED"):
        MODULE._parse_aware_timestamps(values, label="test")


def test_mixed_aware_and_naive_timestamps_are_rejected() -> None:
    values = pd.Series(["2024-01-02T10:00:00+02:00", "2024-01-02 09:00:00"])
    with pytest.raises(ValueError, match="TIMEZONE_PROVENANCE_UNRESOLVED"):
        MODULE._parse_aware_timestamps(values, label="test")


def test_invalid_timestamp_is_rejected() -> None:
    values = pd.Series(["not-a-timestamp"])
    with pytest.raises(ValueError, match="invalid timestamp"):
        MODULE._parse_aware_timestamps(values, label="test")


def test_different_offsets_that_resolve_to_same_instant_are_detected_as_duplicate() -> None:
    events = pd.DataFrame({"timestamp": ["2024-01-02T10:00:00+02:00"]})
    mtf = pd.DataFrame(
        {
            "timestamp": ["2024-01-02T08:00:00Z", "2024-01-02T10:00:00+02:00"],
            **{field: [1, 1] for field in MODULE.REQUIRED_MTF_FIELDS},
        }
    )
    with pytest.raises(ValueError, match="mtf: duplicate timestamps"):
        MODULE.join_mtf_to_events(events, mtf)


def test_asof_join_rejects_non_finite_mtf_source_values() -> None:
    events = pd.DataFrame({"timestamp": ["2024-01-02T08:30:00Z"]})
    mtf = pd.DataFrame(
        {
            "timestamp": ["2024-01-02T08:00:00Z"],
            **{field: [1.0] for field in MODULE.REQUIRED_MTF_FIELDS},
        }
    )
    mtf.loc[0, "mtf_trend_score"] = float("inf")
    with pytest.raises(ValueError, match="non-finite values in mtf_trend_score"):
        MODULE.join_mtf_to_events(events, mtf)


def test_asof_join_uses_latest_non_future_mtf_row() -> None:
    events = pd.DataFrame(
        {"timestamp": ["2024-01-02T08:30:00Z", "2024-01-02T09:30:00Z"]}
    )
    mtf = pd.DataFrame(
        {
            "timestamp": ["2024-01-02T08:00:00Z", "2024-01-02T09:00:00Z"],
            **{field: [1, 2] for field in MODULE.REQUIRED_MTF_FIELDS},
        }
    )
    joined = MODULE.join_mtf_to_events(events, mtf)
    assert joined["mtf_trend_score"].tolist() == [1, 2]
    assert joined["M5_trend_regime"].tolist() == [1, 2]


BUILDER_PATH = MODULE_PATH.parents[2] / "tools" / "gate3c_build_single_event_bundle_v1.py"
BUILDER_SPEC = importlib.util.spec_from_file_location("gate3c_build_single_event_bundle_v1", BUILDER_PATH)
assert BUILDER_SPEC is not None and BUILDER_SPEC.loader is not None
BUILDER = importlib.util.module_from_spec(BUILDER_SPEC)
BUILDER_SPEC.loader.exec_module(BUILDER)


def test_gate3c_builder_rejects_naive_source_timestamp() -> None:
    with pytest.raises(ValueError, match="BLOCKED_TIMEZONE_PROVENANCE_UNRESOLVED"):
        BUILDER.parse_aware_timestamp("2024-01-02 10:00:00", source="fixture")


def test_gate3c_builder_normalizes_explicit_offset_to_utc() -> None:
    parsed = BUILDER.parse_aware_timestamp("2024-01-02T10:00:00+02:00", source="fixture")
    assert parsed == pd.Timestamp("2024-01-02T08:00:00Z")


def test_gate3c_builder_rejects_mixed_naive_and_aware_source_rows(tmp_path: Path) -> None:
    source = tmp_path / "mixed.csv"
    source.write_text(
        "timestamp,value\n2024-01-02T10:00:00+02:00,1\n2024-01-02 09:00:00,2\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="BLOCKED_TIMEZONE_PROVENANCE_UNRESOLVED"):
        BUILDER.read_rows_at(source, pd.Timestamp("2024-01-02T08:00:00Z"), exact=False)


GATE3C_PATH = MODULE_PATH.with_name("gate3c_single_event_e2e_v1.py")
GATE3C_SPEC = importlib.util.spec_from_file_location("gate3c_single_event_e2e_v1", GATE3C_PATH)
assert GATE3C_SPEC is not None and GATE3C_SPEC.loader is not None
GATE3C = importlib.util.module_from_spec(GATE3C_SPEC)
GATE3C_SPEC.loader.exec_module(GATE3C)


def test_gate3c_event_timestamp_rejects_naive_values() -> None:
    with pytest.raises(ValueError, match="BLOCKED_TIMEZONE_PROVENANCE_UNRESOLVED"):
        GATE3C._timestamp("2024-01-02 10:00:00")


def test_gate3c_event_timestamp_normalizes_explicit_offset_to_utc() -> None:
    parsed = GATE3C._timestamp("2024-01-02T10:00:00+02:00")
    assert parsed == pd.Timestamp("2024-01-02T08:00:00Z")


def test_gate3c_rule_timestamp_series_rejects_naive_values() -> None:
    values = pd.Series(["2024-01-02T10:00:00+02:00", "2024-01-02 09:00:00"])
    with pytest.raises(ValueError, match="BLOCKED_TIMEZONE_PROVENANCE_UNRESOLVED"):
        GATE3C._parse_aware_timestamp_series(values, label="murphy")


def test_gate3c_rule_timestamp_series_normalizes_offsets_to_utc() -> None:
    values = pd.Series(["2024-01-02T10:00:00+02:00", "2024-01-02T09:00:00Z"])
    parsed = GATE3C._parse_aware_timestamp_series(values, label="nison")
    assert str(parsed.dt.tz) == "UTC"
    assert parsed.iloc[0] == pd.Timestamp("2024-01-02T08:00:00Z")
    assert parsed.iloc[1] == pd.Timestamp("2024-01-02T09:00:00Z")


MTF_GATE_PATH = MODULE_PATH.parents[2] / "BACKTEST" / "mtf_source_contract_gate_v1.py"
MTF_GATE_SPEC = importlib.util.spec_from_file_location("mtf_source_contract_gate_v1", MTF_GATE_PATH)
assert MTF_GATE_SPEC is not None and MTF_GATE_SPEC.loader is not None
MTF_GATE = importlib.util.module_from_spec(MTF_GATE_SPEC)
MTF_GATE_SPEC.loader.exec_module(MTF_GATE)


def _write_mtf_source(path: Path, timestamps: list[str]) -> Path:
    rows = {
        "timestamp": timestamps,
        **{field: [1.0] * len(timestamps) for field in MTF_GATE.REQUIRED},
    }
    pd.DataFrame(rows).to_csv(path, index=False)
    return path


def test_mtf_gate_normalizes_explicit_offsets_to_utc(tmp_path: Path) -> None:
    source = _write_mtf_source(tmp_path / "aware.csv", ["2024-01-02T10:00:00+02:00"])
    report = MTF_GATE.inspect(source)
    assert report["status"] == "PASS"
    assert report["min_timestamp"] == "2024-01-02T08:00:00+00:00"
    assert report["max_timestamp"] == "2024-01-02T08:00:00+00:00"


def test_mtf_gate_rejects_infinite_numeric_source_field(tmp_path: Path) -> None:
    source = _write_mtf_source(tmp_path / "infinite.csv", ["2024-01-02T10:00:00+02:00"])
    frame = pd.read_csv(source)
    frame.loc[0, "H4_trend_regime"] = float("inf")
    frame.to_csv(source, index=False)
    with pytest.raises(SystemExit, match="BLOCKED_MTF_NON_FINITE_SOURCE_FIELD:H4_trend_regime"):
        MTF_GATE.inspect(source)


def test_mtf_gate_rejects_naive_timestamp(tmp_path: Path) -> None:
    source = _write_mtf_source(tmp_path / "naive.csv", ["2024-01-02 10:00:00"])
    with pytest.raises(SystemExit, match="BLOCKED_MTF_TIMEZONE_PROVENANCE_UNRESOLVED"):
        MTF_GATE.inspect(source)


def test_mtf_gate_rejects_mixed_aware_and_naive_timestamps(tmp_path: Path) -> None:
    source = _write_mtf_source(
        tmp_path / "mixed.csv",
        ["2024-01-02T10:00:00+02:00", "2024-01-02 09:00:00"],
    )
    with pytest.raises(SystemExit, match="BLOCKED_MTF_TIMEZONE_PROVENANCE_UNRESOLVED"):
        MTF_GATE.inspect(source)


def test_mtf_gate_rejects_invalid_timestamp(tmp_path: Path) -> None:
    source = _write_mtf_source(tmp_path / "invalid.csv", ["not-a-timestamp"])
    with pytest.raises(SystemExit, match="BLOCKED_MTF_INVALID_TIMESTAMP"):
        MTF_GATE.inspect(source)


def test_mtf_gate_rejects_duplicate_instants_after_utc_normalization(tmp_path: Path) -> None:
    source = _write_mtf_source(
        tmp_path / "duplicate.csv",
        ["2024-01-02T10:00:00+02:00", "2024-01-02T08:00:00Z"],
    )
    with pytest.raises(SystemExit, match="BLOCKED_MTF_DUPLICATE_TIMESTAMP"):
        MTF_GATE.inspect(source)


def test_mtf_source_workflow_uses_the_same_fail_closed_timestamp_parser() -> None:
    root = MODULE_PATH.parents[2]
    workflow = (root / ".github" / "workflows" / "mtf-source-gate-smoke-2026-09-02.yml").read_text(encoding="utf-8")
    assert "parse_aware_timestamps(df['timestamp']" in workflow
    assert "pd.to_datetime(df['timestamp'],utc=True" not in workflow


from RUNTIME.DECISION_RUNTIME_V1.full_brain_runtime_bridge_v1 import (
    _enforce_development_risk_contract,
)


def _canonical_risk(**overrides):
    values = {"rr": 3.0, "stop_loss": 98.0, "take_profit": 106.0}
    values.update(overrides)
    return values


def _execution_result(stop_loss=98.5, take_profit=103.0):
    return {
        "status": "EXECUTABLE",
        "execution_plan": {
            "status": "EXECUTABLE",
            "stop_loss": stop_loss,
            "take_profit": take_profit,
        },
        "audit": {},
    }


def test_development_mode_blocks_candidate_2r_levels_against_canonical_3r_risk() -> None:
    result = _enforce_development_risk_contract(
        _execution_result(stop_loss=98.5, take_profit=103.0),
        _canonical_risk(),
        mode="development",
    )
    assert result["status"] == "NOT_EXECUTABLE"
    assert result["reason"] == "EXECUTION_PLAN_DIFFERS_FROM_CANONICAL_RISK_LEVELS"
    assert result["execution_plan"]["status"] == "NOT_EXECUTABLE"
    assert result["audit"]["canonical_risk_execution_match"] is False


def test_development_mode_accepts_only_levels_returned_by_canonical_risk() -> None:
    result = _enforce_development_risk_contract(
        _execution_result(stop_loss=98.0, take_profit=106.0),
        _canonical_risk(),
        mode="development",
    )
    assert result["status"] == "EXECUTABLE"
    assert result["audit"]["canonical_risk_execution_match"] is True


@pytest.mark.parametrize(
    "risk_overrides,execution_overrides",
    [
        ({"rr": float("nan")}, {}),
        ({"stop_loss": float("inf")}, {}),
        ({}, {"take_profit": float("nan")}),
    ],
)
def test_development_mode_blocks_non_finite_canonical_risk_values(
    risk_overrides: dict,
    execution_overrides: dict,
) -> None:
    result = _enforce_development_risk_contract(
        _execution_result(**execution_overrides),
        _canonical_risk(**risk_overrides),
        mode="development",
    )
    assert result["status"] == "NOT_EXECUTABLE"
    assert result["reason"] == "CANONICAL_RISK_PLAN_INPUTS_NON_FINITE"


def test_development_mode_fails_closed_when_canonical_rr_is_missing() -> None:
    result = _enforce_development_risk_contract(
        _execution_result(stop_loss=98.0, take_profit=106.0),
        _canonical_risk(rr=None),
        mode="development",
    )
    assert result["status"] == "NOT_EXECUTABLE"
    assert result["reason"] == "CANONICAL_RISK_PLAN_INPUTS_MISSING"


def test_oos_candidate_mode_preserves_its_separate_frozen_adapter_contract() -> None:
    original = _execution_result()
    returned = _enforce_development_risk_contract(
        original,
        _canonical_risk(),
        mode="oos_evaluation",
    )
    assert returned is original


def test_mtf_gate_reports_blank_values_as_missing_without_imputation(tmp_path: Path) -> None:
    source = _write_mtf_source(tmp_path / "blank.csv", ["2024-01-02T10:00:00+02:00"])
    frame = pd.read_csv(source)
    frame.loc[0, "M15_trend_regime"] = ""
    frame.to_csv(source, index=False)
    with pytest.raises(
        SystemExit,
        match=r"BLOCKED_MTF_MISSING_SOURCE_VALUE:M15_trend_regime:count=1",
    ):
        MTF_GATE.inspect(source)


def test_mtf_gate_distinguishes_invalid_tokens_from_blank_source_values(tmp_path: Path) -> None:
    source = _write_mtf_source(tmp_path / "invalid-token.csv", ["2024-01-02T10:00:00+02:00"])
    frame = pd.read_csv(source)
    frame.loc[0, "M15_trend_regime"] = "UNKNOWN"
    frame.to_csv(source, index=False)
    with pytest.raises(
        SystemExit,
        match=r"BLOCKED_MTF_NON_NUMERIC_SOURCE_FIELD:M15_trend_regime:count=1",
    ):
        MTF_GATE.inspect(source)


def test_shared_timestamp_parser_uses_source_specific_fail_closed_code() -> None:
    values = pd.Series(["2024-01-02 10:00:00"])
    with pytest.raises(ValueError, match="BLOCKED_SOURCE_TIMEZONE_PROVENANCE_UNRESOLVED"):
        MTF_GATE.parse_aware_timestamps(
            values,
            label="H1",
            error_prefix="BLOCKED_SOURCE",
        )


def test_circleci_timestamp_consumers_use_explicit_timezone_parser() -> None:
    root = MODULE_PATH.parents[2]
    gate_source = (root / "BACKTEST" / "CIRCLECI_RUN_GOVERNED_GATE.py").read_text(encoding="utf-8")
    frozen_source = (root / "BACKTEST" / "CIRCLECI_FROZEN_SCOPE_CHECK.py").read_text(encoding="utf-8")

    assert "parse_aware_timestamps" in gate_source
    assert 'pd.to_datetime(chunk["timestamp"], utc=True' not in gate_source
    assert "parse_aware_timestamps" in frozen_source
    assert 'pd.to_datetime(h1["timestamp"], utc=True' not in frozen_source
    assert 'pd.to_datetime(n["timestamp"], utc=True' not in frozen_source
    assert 'pd.to_datetime(m["timestamp"], utc=True' not in frozen_source


def test_mtf_source_workflow_runs_on_pr_head_and_keeps_2025_out_of_scope() -> None:
    root = MODULE_PATH.parents[2]
    workflow = (root / ".github" / "workflows" / "mtf-source-gate-smoke-2026-09-02.yml").read_text(encoding="utf-8")

    assert "pull_request:" in workflow
    assert "github.event.pull_request.head.sha || github.sha" in workflow
    assert "range(2016,2025)" in workflow
    assert "range(2016,2026)" not in workflow
    assert "run_governed_backtest" not in workflow
