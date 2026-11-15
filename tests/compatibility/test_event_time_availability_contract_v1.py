from __future__ import annotations

from compatibility.event_time_availability_contract_v1 import (
    validate_evidence_timing,
    validate_event_evidence_bundle,
)


def evidence(**overrides):
    row = {
        "source_id": "H1",
        "producer_id": "canonical_h1_builder_v1",
        "source_ref": "archive://GBPUSD_H1/2020.csv#row-123",
        "timestamp_label_semantics": "BAR_OPEN",
        "source_timestamp": "2020-01-03T00:00:00Z",
        "bar_open_time": "2020-01-03T00:00:00Z",
        "bar_close_time": "2020-01-03T01:00:00Z",
        "available_at": "2020-01-03T01:00:00Z",
    }
    row.update(overrides)
    return row


def test_completed_bar_available_at_decision_boundary_is_eligible():
    result = validate_evidence_timing(evidence(), "2020-01-03T01:00:00Z")
    assert result["status"] == "ELIGIBLE"
    assert result["reason"] == "SOURCE_CLOSED_AND_AVAILABLE_AS_OF_DECISION"


def test_bar_open_timestamp_does_not_make_full_bar_available_at_open():
    result = validate_evidence_timing(evidence(), "2020-01-03T00:00:00Z")
    assert result["status"] == "NOT_EVALUABLE"
    assert result["reason"] == "BLOCKED_BAR_NOT_CLOSED_AT_DECISION"


def test_evidence_available_after_decision_is_rejected_even_if_bar_close_precedes_it():
    row = evidence(
        bar_close_time="2020-01-03T00:55:00Z",
        available_at="2020-01-03T01:00:00Z",
    )
    result = validate_evidence_timing(row, "2020-01-03T00:55:00Z")
    assert result["status"] == "NOT_EVALUABLE"
    assert result["reason"] == "BLOCKED_EVIDENCE_NOT_YET_AVAILABLE"


def test_missing_availability_metadata_fails_closed():
    row = evidence()
    row.pop("available_at")
    result = validate_evidence_timing(row, "2020-01-03T01:00:00Z")
    assert result["status"] == "NOT_EVALUABLE"
    assert result["reason"] == "BLOCKED_MISSING_TIME_METADATA"
    assert "available_at" in result["missing_fields"]


def test_unknown_timestamp_label_semantics_fails_closed():
    result = validate_evidence_timing(
        evidence(timestamp_label_semantics="UNKNOWN"),
        "2020-01-03T01:00:00Z",
    )
    assert result["status"] == "NOT_EVALUABLE"
    assert result["reason"] == "BLOCKED_UNKNOWN_TIMESTAMP_SEMANTICS"


def test_timestamp_label_must_match_declared_bar_open_or_close():
    result = validate_evidence_timing(
        evidence(source_timestamp="2020-01-03T01:00:00Z"),
        "2020-01-03T01:00:00Z",
    )
    assert result["status"] == "NOT_EVALUABLE"
    assert result["reason"] == "BLOCKED_TIMESTAMP_LABEL_MISMATCH"


def test_naive_timestamp_is_rejected():
    result = validate_evidence_timing(
        evidence(available_at="2020-01-03T01:00:00"),
        "2020-01-03T01:00:00Z",
    )
    assert result["status"] == "NOT_EVALUABLE"
    assert result["reason"] == "BLOCKED_INVALID_TIME_METADATA"


def test_available_before_bar_close_is_rejected():
    result = validate_evidence_timing(
        evidence(available_at="2020-01-03T00:59:59Z"),
        "2020-01-03T01:00:00Z",
    )
    assert result["status"] == "NOT_EVALUABLE"
    assert result["reason"] == "BLOCKED_INVALID_TIME_ORDER"


def test_bar_close_timestamp_semantics_are_supported_explicitly():
    row = evidence(
        timestamp_label_semantics="BAR_CLOSE",
        source_timestamp="2020-01-03T01:00:00Z",
    )
    result = validate_evidence_timing(row, "2020-01-03T01:00:00Z")
    assert result["status"] == "ELIGIBLE"


def test_bundle_requires_each_source_and_every_record_to_be_available():
    rows = [
        evidence(),
        evidence(
            source_id="MTF_M5",
            producer_id="mtf_alignment_v1",
            source_ref="archive://MTF/2020.csv#row-456",
            timestamp_label_semantics="BAR_CLOSE",
            source_timestamp="2020-01-03T01:00:00Z",
            bar_open_time="2020-01-03T00:55:00Z",
            bar_close_time="2020-01-03T01:00:00Z",
            available_at="2020-01-03T01:00:00Z",
        ),
    ]
    result = validate_event_evidence_bundle(
        rows,
        "2020-01-03T01:00:00Z",
        required_sources=["H1", "MTF_M5", "MURPHY", "NISON", "MARKET_STATE"],
    )
    assert result["status"] == "NOT_EVALUABLE"
    assert result["missing_sources"] == ["MURPHY", "NISON", "MARKET_STATE"]


def test_bundle_fails_when_any_required_source_contains_future_evidence():
    rows = [
        evidence(),
        evidence(
            source_id="MTF_M5",
            producer_id="mtf_alignment_v1",
            source_ref="archive://MTF/2020.csv#row-456",
            timestamp_label_semantics="BAR_OPEN",
            source_timestamp="2020-01-03T00:55:00Z",
            bar_open_time="2020-01-03T00:55:00Z",
            bar_close_time="2020-01-03T01:00:00Z",
            available_at="2020-01-03T01:00:00Z",
        ),
    ]
    result = validate_event_evidence_bundle(
        rows,
        "2020-01-03T00:55:00Z",
        required_sources=["H1", "MTF_M5"],
    )
    assert result["status"] == "NOT_EVALUABLE"
    assert result["reason"] == "BLOCKED_EVENT_EVIDENCE_TIME_CONTRACT"
    assert result["evidence_results"][1]["reason"] == "BLOCKED_BAR_NOT_CLOSED_AT_DECISION"


def test_bundle_passes_only_when_all_required_sources_are_closed_and_available():
    rows = [
        evidence(),
        evidence(
            source_id="MTF_M5",
            producer_id="mtf_alignment_v1",
            source_ref="archive://MTF/2020.csv#row-456",
            timestamp_label_semantics="BAR_CLOSE",
            source_timestamp="2020-01-03T01:00:00Z",
            bar_open_time="2020-01-03T00:55:00Z",
            bar_close_time="2020-01-03T01:00:00Z",
            available_at="2020-01-03T01:00:00Z",
        ),
    ]
    result = validate_event_evidence_bundle(
        rows,
        "2020-01-03T01:00:00Z",
        required_sources=["H1", "MTF_M5"],
    )
    assert result["status"] == "ELIGIBLE_FOR_DOWNSTREAM_EVALUATION"
