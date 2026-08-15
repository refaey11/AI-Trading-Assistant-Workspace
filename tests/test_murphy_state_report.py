from datetime import datetime, timezone

from tools.murphy_evidence_chain import EvidenceRecord
from tools.murphy_state_report import build_report


def rec(rule_id: str, sha: str, claim: str | None = None) -> EvidenceRecord:
    return EvidenceRecord(
        rule_id=rule_id,
        commit_sha=sha,
        timestamp=datetime(2026, 8, 15, 10, 0, tzinfo=timezone.utc),
        evidence_type="status" if claim else "git_commit",
        status_claim=claim,
    )


def test_report_always_contains_exactly_51_rules():
    report = build_report([rec("0021", "a"), rec("0051", "b", "REVIEW")])
    assert report["rule_count"] == 51
    assert [row["rule_id"] for row in report["rows"]] == [f"{n:04d}" for n in range(1, 52)]


def test_report_does_not_promote_a_status_claim_to_frozen_gate():
    report = build_report([rec("0021", "a", "FROZEN")])
    row = next(item for item in report["rows"] if item["rule_id"] == "0021")
    assert row["status_claims"] == {"FROZEN": 1}
    assert row["state"] != "FROZEN"
    assert "status/artifact evidence exists but no recognized gate evidence is established" in row["reasons"]


def test_report_ignores_out_of_range_rule_ids():
    report = build_report([rec("0052", "x"), rec("0000", "y"), rec("0001", "z")])
    rows = {row["rule_id"] for row in report["rows"]}
    assert "0052" not in rows
    assert "0000" not in rows
    assert "0001" in rows
