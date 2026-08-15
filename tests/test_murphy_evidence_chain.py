from datetime import datetime, timedelta, timezone

from tools.murphy_evidence_chain import EvidenceRecord, reduce_state
from tools.murphy_state_verifier import State


BASE = datetime(2026, 8, 15, tzinfo=timezone.utc)


def rec(**kwargs):
    defaults = {
        "rule_id": "0025",
        "commit_sha": "c",
        "timestamp": BASE,
        "evidence_type": "status",
    }
    defaults.update(kwargs)
    return EvidenceRecord(**defaults)


def test_later_freeze_supersedes_older_blocked_assertion():
    old = rec(commit_sha="blocked", status_claim="BLOCKED")
    new = rec(
        commit_sha="freeze",
        timestamp=BASE + timedelta(hours=1),
        status_claim="FROZEN",
        supersedes="blocked",
    )
    state, reasons = reduce_state([old, new])
    assert state is State.FROZEN
    assert "FROZEN" in reasons[0]


def test_live_conflicting_authoritative_claims_return_conflict():
    a = rec(commit_sha="a", status_claim="FROZEN")
    b = rec(commit_sha="b", timestamp=BASE + timedelta(hours=1), status_claim="BLOCKED")
    state, _ = reduce_state([a, b])
    assert state is State.CONFLICT


def test_blocker_closure_requires_traceable_closure_commit():
    opened = rec(commit_sha="open", evidence_type="blocker_open", blocker_id="B1")
    unlinked_close = rec(
        commit_sha="close",
        timestamp=BASE + timedelta(hours=1),
        evidence_type="blocker_closed",
        blocker_id="B1",
        blocker_closed_by="missing",
    )
    state, _ = reduce_state([opened, unlinked_close])
    assert state is State.BLOCKED


def test_traceable_blocker_closure_removes_blocker():
    opened = rec(commit_sha="open", evidence_type="blocker_open", blocker_id="B1")
    close_commit = rec(
        commit_sha="close",
        timestamp=BASE + timedelta(hours=1),
        evidence_type="closure_commit",
    )
    closed = rec(
        commit_sha="closed-record",
        timestamp=BASE + timedelta(hours=2),
        evidence_type="blocker_closed",
        blocker_id="B1",
        blocker_closed_by="close",
        status_claim="FROZEN",
    )
    state, _ = reduce_state([opened, close_commit, closed])
    assert state is State.FROZEN


def test_non_authoritative_claim_is_ignored():
    chat = rec(commit_sha="chat", status_claim="FROZEN", authoritative=False)
    state, _ = reduce_state([chat])
    assert state is State.UNVERIFIED
