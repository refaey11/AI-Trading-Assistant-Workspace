"""Deterministic reducer for traceable Murphy Rule evidence chains.

This module does not fetch GitHub data itself. It consumes normalized evidence
records produced by a repository collector and resolves stale claims only when
supersession/closure is explicitly traceable. Ambiguous authoritative states
remain CONFLICT.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from tools.murphy_state_verifier import State


@dataclass(frozen=True)
class EvidenceRecord:
    rule_id: str
    commit_sha: str
    timestamp: datetime
    evidence_type: str
    status_claim: str | None = None
    supersedes: str | None = None
    blocker_id: str | None = None
    blocker_closed_by: str | None = None
    artifact_path: str = ""
    oos_used: bool = False
    oos_forbidden_purpose: bool = False
    future_data_contamination: bool = False
    notes: str = ""
    authoritative: bool = True


def _ordered(records: Iterable[EvidenceRecord]) -> list[EvidenceRecord]:
    return sorted(records, key=lambda r: (r.timestamp, r.commit_sha, r.evidence_type))


def reduce_state(records: Iterable[EvidenceRecord]) -> tuple[State, tuple[str, ...]]:
    """Reduce one Rule's traceable records without guessing."""
    ordered = _ordered(r for r in records if r.authoritative)
    if not ordered:
        return State.UNVERIFIED, ("no authoritative evidence records",)

    if any(r.oos_forbidden_purpose for r in ordered):
        return State.BLOCKED, ("forbidden 2025 OOS use is present",)
    if any(r.future_data_contamination for r in ordered):
        return State.BLOCKED, ("future-data contamination is present",)

    by_sha = {r.commit_sha: r for r in ordered}
    superseded: set[str] = set()
    for record in ordered:
        if record.supersedes and record.supersedes in by_sha:
            superseded.add(record.supersedes)

    live = [r for r in ordered if r.commit_sha not in superseded]
    claims = {r.status_claim.upper() for r in live if r.status_claim}
    if len(claims) > 1:
        return State.CONFLICT, ("multiple incompatible authoritative state assertions remain live",)

    open_times: dict[str, datetime] = {}
    for record in ordered:
        if record.evidence_type == "blocker_open" and record.blocker_id:
            open_times[record.blocker_id] = min(
                record.timestamp,
                open_times.get(record.blocker_id, record.timestamp),
            )

    closed_blockers: set[str] = set()
    for record in ordered:
        if record.evidence_type != "blocker_closed" or not record.blocker_id:
            continue
        closure_sha = record.blocker_closed_by
        closure = by_sha.get(closure_sha) if closure_sha else None
        opened_at = open_times.get(record.blocker_id)
        if closure and opened_at and closure.timestamp > opened_at:
            closed_blockers.add(record.blocker_id)

    unresolved = set(open_times) - closed_blockers
    if unresolved:
        return State.BLOCKED, ("active authoritative blocker(s): " + ", ".join(sorted(unresolved)),)

    if not claims:
        return State.UNVERIFIED, ("authoritative evidence exists but no state assertion is established",)

    claim = next(iter(claims))
    try:
        return State(claim), (f"latest non-superseded authoritative state: {claim}",)
    except ValueError:
        return State.UNVERIFIED, (f"unsupported state claim: {claim}",)
