import pandas as pd

from full_78_rule_decision_event_stream_v2 import ALLOWLIST, build_rule_event_stream, summarize_coverage


def test_stream_emits_all_78_rules_per_timestamp_without_inventing_evidence():
    timestamps = pd.to_datetime(["2025-01-02T00:00:00Z", "2025-01-02T01:00:00Z"], utc=True)
    murphy = [{
        "timestamp": timestamps[0], "rule_id": "MURPHY_0021", "status": "PASS",
        "available": True, "direction": "BULLISH", "reason": "existing runtime",
    }]
    nison = [{
        "timestamp": timestamps[0], "rule_id": "NISON_0001", "status": "NOT_EVALUABLE",
        "available": False, "direction": None, "reason": "missing confirmation",
    }]
    stream = build_rule_event_stream(timestamps, murphy_rows=murphy, nison_rows=nison)
    assert len(stream) == 2 * 78
    assert set(stream.rule_id) == set(ALLOWLIST)
    row = stream[(stream.timestamp == timestamps[0]) & (stream.rule_id == "MURPHY_0021")].iloc[0]
    assert row.status == "PASS" and bool(row.available)
    missing = stream[(stream.timestamp == timestamps[1]) & (stream.rule_id == "NISON_0044")].iloc[0]
    assert missing.status == "NOT_EVALUABLE"
    assert missing.reason == "NO_2025_OUTPUT"


def test_coverage_summary_is_explicit_about_missing_outputs():
    timestamps = pd.to_datetime(["2025-01-02T00:00:00Z"], utc=True)
    stream = build_rule_event_stream(timestamps)
    summary = summarize_coverage(stream)
    assert summary["runtime_allowlist_count"] == 78
    assert summary["observed_rule_count"] == 78
    assert summary["expected_rule_rows"] == 78
    assert summary["actual_rows"] == 78
    assert summary["available_rows"] == 0
    assert summary["availability_rate"] == 0.0
    assert summary["generated_from_existing_outputs_only"] is True
    assert summary["2025_tuning"] is False
