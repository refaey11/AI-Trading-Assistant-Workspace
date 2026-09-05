"""Regression tests for the fail-closed Gate 3C Murphy fan-in."""

import csv
from pathlib import Path

import pytest

from tools.gate3c_build_single_event_bundle_v1 import MURPHY_IDS, build_bundle, murphy_coverage


TIMESTAMP = "2025-01-02T03:04:05Z"


def _write_event(root: Path, rule_ids: tuple[str, ...] | list[str]) -> None:
    with (root / "murphy.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("timestamp", "source_rule_id"))
        writer.writeheader()
        writer.writerows(
            {"timestamp": TIMESTAMP, "source_rule_id": rule_id} for rule_id in rule_ids
        )


def test_complete_murphy_34_rule_fan_in_passes(tmp_path: Path) -> None:
    _write_event(tmp_path, MURPHY_IDS)

    bundle = build_bundle(TIMESTAMP, tmp_path)

    assert bundle["murphy"]["rule_count"] == 34
    assert bundle["murphy"]["missing_rule_ids"] == []
    assert bundle["murphy"]["unknown_rule_ids"] == []
    assert bundle["murphy"]["complete"] is True


def test_missing_murphy_rule_rejects_event(tmp_path: Path) -> None:
    missing_rule = MURPHY_IDS[-1]
    _write_event(tmp_path, MURPHY_IDS[:-1])

    coverage = murphy_coverage(MURPHY_IDS[:-1])

    assert coverage["missing_rule_ids"] == [missing_rule]
    assert coverage["complete"] is False
    with pytest.raises(RuntimeError, match="BLOCKED_MURPHY_34_INCOMPLETE"):
        build_bundle(TIMESTAMP, tmp_path)


def test_unknown_murphy_id_rejects_event(tmp_path: Path) -> None:
    unknown_rule = "MURPHY_9999"
    _write_event(tmp_path, (*MURPHY_IDS, unknown_rule))

    coverage = murphy_coverage((*MURPHY_IDS, unknown_rule))

    assert coverage["missing_rule_ids"] == []
    assert coverage["unknown_rule_ids"] == [unknown_rule]
    assert coverage["complete"] is False
    with pytest.raises(RuntimeError, match="BLOCKED_MURPHY_34_INCOMPLETE"):
        build_bundle(TIMESTAMP, tmp_path)


def test_duplicate_murphy_rows_do_not_inflate_rule_count() -> None:
    coverage = murphy_coverage((*MURPHY_IDS, MURPHY_IDS[0], MURPHY_IDS[0]))

    assert coverage["rule_count"] == 34
    assert coverage["rule_ids"] == sorted(MURPHY_IDS)
    assert coverage["missing_rule_ids"] == []
    assert coverage["unknown_rule_ids"] == []
    assert coverage["complete"] is True
