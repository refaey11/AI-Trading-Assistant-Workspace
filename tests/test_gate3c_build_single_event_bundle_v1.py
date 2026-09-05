"""Regression tests for the fail-closed Gate 3C Murphy fan-in."""

import inspect

from tools.gate3c_build_single_event_bundle_v1 import MURPHY_IDS, build, murphy_coverage


TIMESTAMP = "2024-01-02T03:04:05Z"


def test_current_build_interface_accepts_event_timestamp_and_all_sources() -> None:
    parameters = list(inspect.signature(build).parameters)
    assert parameters == [
        "event_ts",
        "h1",
        "market_state",
        "nison",
        "murphy_root",
        "mtf_root",
        "historical_context_root",
        "historical_outcome_root",
        "similarity_root",
        "retrieval_root",
    ]
    assert 2016 <= int(TIMESTAMP[:4]) <= 2024


def test_complete_murphy_34_rule_fan_in_passes() -> None:
    coverage = murphy_coverage(sorted(MURPHY_IDS))
    assert len(MURPHY_IDS) == 34
    assert coverage["missing_rule_ids"] == []
    assert coverage["unknown_rule_ids"] == []
    assert coverage["complete"] is True


def test_missing_murphy_rule_rejects_event() -> None:
    missing_rule = sorted(MURPHY_IDS)[-1]
    coverage = murphy_coverage(sorted(MURPHY_IDS - {missing_rule}))
    assert coverage["missing_rule_ids"] == [missing_rule]
    assert coverage["complete"] is False


def test_unknown_murphy_id_rejects_event() -> None:
    unknown_rule = "MURPHY_9999"
    coverage = murphy_coverage([*sorted(MURPHY_IDS), unknown_rule])
    assert coverage["missing_rule_ids"] == []
    assert coverage["unknown_rule_ids"] == [unknown_rule]
    assert coverage["complete"] is False


def test_duplicate_murphy_rows_do_not_inflate_rule_count() -> None:
    coverage = murphy_coverage([*sorted(MURPHY_IDS), sorted(MURPHY_IDS)[0], sorted(MURPHY_IDS)[0]])
    assert coverage["missing_rule_ids"] == []
    assert coverage["unknown_rule_ids"] == []
    assert coverage["complete"] is True
