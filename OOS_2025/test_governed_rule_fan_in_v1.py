import pandas as pd

from governed_rule_fan_in_v1 import (
    build_lossless_rule_groups,
    combine_timestamp_evidence,
    evidence_summary,
    legacy_selected_row,
)


def _df():
    ts = pd.to_datetime(["2025-01-01T00:00:00Z", "2025-01-01T00:00:00Z", "2025-01-01T01:00:00Z"])
    return pd.DataFrame(
        {
            "timestamp": ts,
            "source_rule_id": ["MURPHY_0003", "MURPHY_0021", "MURPHY_0004"],
            "status": ["PASS", "PASS", "FAIL"],
            "direction": ["BULLISH_STRUCTURE", "BULLISH", "NONE"],
        }
    )


def test_lossless_groups_preserve_same_timestamp_rules():
    groups = build_lossless_rule_groups(_df())
    ts = pd.Timestamp("2025-01-01T00:00:00Z")
    assert len(groups[ts]) == 2
    assert [r["source_rule_id"] for r in groups[ts]] == ["MURPHY_0003", "MURPHY_0021"]


def test_legacy_selector_is_explicit_and_non_aggregating():
    rows = build_lossless_rule_groups(_df())[pd.Timestamp("2025-01-01T00:00:00Z")]
    selected = legacy_selected_row(rows)
    assert selected["source_rule_id"] == "MURPHY_0021"
    assert len(rows) == 2


def test_synthetic_ids_are_not_real_evidence():
    df = _df()
    df.loc[len(df)] = [pd.Timestamp("2025-01-01T00:00:00Z"), "NISON_NONE", "", ""]
    groups = build_lossless_rule_groups(df)
    ts = pd.Timestamp("2025-01-01T00:00:00Z")
    assert "NISON_NONE" not in [r["source_rule_id"] for r in groups[ts]]


def test_summary_reports_all_rules():
    rows = build_lossless_rule_groups(_df())[pd.Timestamp("2025-01-01T00:00:00Z")]
    summary = evidence_summary(rows)
    assert summary["record_count"] == 2
    assert summary["unique_rule_ids"] == ["MURPHY_0003", "MURPHY_0021"]
    assert summary["lossless"] is True


def test_combined_envelope_preserves_both_books():
    murphy = _df()
    nison = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(["2025-01-01T00:00:00Z"]),
            "source_rule_id": ["NISON_0001"],
            "confirmation": ["CONFIRMED"],
            "contradiction": [False],
        }
    )
    envelope = combine_timestamp_evidence(murphy, nison)
    ts = pd.Timestamp("2025-01-01T00:00:00Z")
    assert envelope[ts]["murphy_summary"]["record_count"] == 2
    assert envelope[ts]["nison_summary"]["record_count"] == 1
    assert envelope[ts]["murphy_summary"]["lossless"] is True
