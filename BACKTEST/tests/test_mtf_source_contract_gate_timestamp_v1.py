from __future__ import annotations

import importlib.util
from pathlib import Path

import pandas as pd
import pytest


GATE_PATH = Path(__file__).parents[1] / "mtf_source_contract_gate_v1.py"
SPEC = importlib.util.spec_from_file_location("mtf_source_contract_gate_v1", GATE_PATH)
assert SPEC is not None and SPEC.loader is not None
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)


def _write_source(tmp_path: Path, timestamps: list[str], **overrides: list[object]) -> Path:
    data: dict[str, list[object]] = {
        "timestamp": timestamps,
        **{field: [1] * len(timestamps) for field in GATE.REQUIRED},
    }
    data.update(overrides)
    path = tmp_path / "mtf.csv"
    pd.DataFrame(data).to_csv(path, index=False)
    return path


def test_explicit_utc_timestamp_passes(tmp_path: Path) -> None:
    report = GATE.inspect(_write_source(tmp_path, ["2024-01-02T08:00:00Z"]))
    assert report["status"] == "PASS"
    assert report["min_timestamp"] == "2024-01-02T08:00:00+00:00"


def test_explicit_offset_is_normalized_to_utc(tmp_path: Path) -> None:
    report = GATE.inspect(_write_source(tmp_path, ["2024-01-02T10:00:00+02:00"]))
    assert report["min_timestamp"] == "2024-01-02T08:00:00+00:00"


def test_naive_timestamp_is_blocked(tmp_path: Path) -> None:
    with pytest.raises(SystemExit, match="BLOCKED_MTF_TIMEZONE_PROVENANCE_UNRESOLVED"):
        GATE.inspect(_write_source(tmp_path, ["2024-01-02 10:00:00"]))


def test_mixed_aware_and_naive_timestamps_are_blocked(tmp_path: Path) -> None:
    with pytest.raises(SystemExit, match="BLOCKED_MTF_TIMEZONE_PROVENANCE_UNRESOLVED"):
        GATE.inspect(
            _write_source(
                tmp_path,
                ["2024-01-02T10:00:00+02:00", "2024-01-02 09:00:00"],
            )
        )


def test_invalid_timestamp_is_blocked(tmp_path: Path) -> None:
    with pytest.raises(SystemExit, match="BLOCKED_MTF_INVALID_TIMESTAMP"):
        GATE.inspect(_write_source(tmp_path, ["not-a-timestamp"]))


def test_duplicate_instants_with_different_offsets_are_blocked(tmp_path: Path) -> None:
    with pytest.raises(SystemExit, match="BLOCKED_MTF_DUPLICATE_TIMESTAMP"):
        GATE.inspect(
            _write_source(
                tmp_path,
                ["2024-01-02T10:00:00+02:00", "2024-01-02T08:00:00Z"],
            )
        )


def test_missing_timestamp_column_is_blocked(tmp_path: Path) -> None:
    data = {field: [1] for field in GATE.REQUIRED}
    path = tmp_path / "missing_timestamp.csv"
    pd.DataFrame(data).to_csv(path, index=False)
    with pytest.raises(SystemExit, match="BLOCKED_MTF_MISSING_TIMESTAMP"):
        GATE.inspect(path)


def test_missing_required_mtf_field_remains_blocked(tmp_path: Path) -> None:
    data = {
        "timestamp": ["2024-01-02T08:00:00Z"],
        **{field: [1] for field in GATE.REQUIRED[:-1]},
    }
    path = tmp_path / "missing_field.csv"
    pd.DataFrame(data).to_csv(path, index=False)
    with pytest.raises(SystemExit, match="BLOCKED_MTF_MISSING_REQUIRED_FIELDS"):
        GATE.inspect(path)


def test_non_numeric_mtf_field_remains_blocked(tmp_path: Path) -> None:
    path = _write_source(
        tmp_path,
        ["2024-01-02T08:00:00Z"],
        M5_trend_regime=["not-numeric"],
    )
    with pytest.raises(SystemExit, match="BLOCKED_MTF_NON_NUMERIC_SOURCE_FIELD:M5_trend_regime"):
        GATE.inspect(path)


@pytest.mark.parametrize("value", ["inf", "-inf"])
def test_non_finite_mtf_value_is_blocked(tmp_path: Path, value: str) -> None:
    path = _write_source(
        tmp_path,
        ["2024-01-02T08:00:00Z"],
        M5_trend_regime=[value],
    )
    with pytest.raises(SystemExit, match="BLOCKED_MTF_NON_FINITE_SOURCE_FIELD:M5_trend_regime"):
        GATE.inspect(path)


def test_empty_source_is_blocked(tmp_path: Path) -> None:
    path = _write_source(tmp_path, [])
    with pytest.raises(SystemExit, match="BLOCKED_MTF_EMPTY_SOURCE"):
        GATE.inspect(path)
