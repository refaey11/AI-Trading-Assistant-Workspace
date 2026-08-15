#!/usr/bin/env python3
"""Deterministic, evidence-first Murphy Rule state verifier.

This module intentionally does not inspect chat memory. Callers supply
traceable repository evidence. Missing or contradictory evidence never gets
upgraded by inference.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Mapping


FROZEN_RULES = {
    "0003", "0004", "0006", "0007", "0008",
    "0021", "0022", "0023", "0025", "0026",
}


class State(str, Enum):
    FROZEN = "FROZEN"
    QA_COMPLETE = "QA_COMPLETE"
    TECHNICALLY_COMPLETE = "TECHNICALLY_COMPLETE"
    INTEGRATION_PENDING = "INTEGRATION_PENDING"
    BLOCKED = "BLOCKED"
    UNVERIFIED = "UNVERIFIED"
    CONFLICT = "CONFLICT"


@dataclass(frozen=True)
class Evidence:
    implementation: bool = False
    tests_pass: bool = False
    historical_qa: bool = False
    no_lookahead: bool = False
    compatibility_audit: bool = False
    blocker_open: bool = False
    blocker_closed: bool = False
    freeze_manifest: bool = False
    frozen_snapshot: bool = False
    production_freeze: bool = False
    merged_main: bool = False
    canonical_frozen: bool = False
    oos_2025_clean: bool = False
    oos_2025_used_for_forbidden_purpose: bool = False
    future_data_contamination: bool = False
    evidence_commits: tuple[str, ...] = field(default_factory=tuple)

    @property
    def active_blocker(self) -> bool:
        """A later, traceable closure supersedes an older blocker claim."""
        return self.blocker_open and not self.blocker_closed


@dataclass(frozen=True)
class Verification:
    rule_id: str
    state: State
    reasons: tuple[str, ...]
    evidence_commits: tuple[str, ...]


def _conflict(states: Iterable[str]) -> bool:
    normalized = {str(x).upper() for x in states if str(x).strip()}
    return len(normalized) > 1


def verify(rule_id: str, evidence: Evidence, conflicting_states: Iterable[str] = ()) -> Verification:
    """Return the strongest state proven by the supplied evidence.

    Evidence precedence is deterministic. Active blockers and OOS/leakage
    violations are hard stops. Contradictory authoritative state assertions
    return CONFLICT instead of guessing.
    """
    rid = str(rule_id).zfill(4)
    if _conflict(conflicting_states):
        return Verification(rid, State.CONFLICT, ("contradictory authoritative state assertions",), evidence.evidence_commits)

    if evidence.future_data_contamination or evidence.oos_2025_used_for_forbidden_purpose:
        return Verification(rid, State.BLOCKED, ("future-data contamination or forbidden 2025 OOS use",), evidence.evidence_commits)

    if evidence.active_blocker:
        return Verification(rid, State.BLOCKED, ("active authoritative blocker remains open",), evidence.evidence_commits)

    frozen_gate = (
        evidence.implementation
        and evidence.tests_pass
        and evidence.historical_qa
        and evidence.no_lookahead
        and evidence.compatibility_audit
        and evidence.oos_2025_clean
        and evidence.freeze_manifest
        and evidence.frozen_snapshot
        and evidence.production_freeze
        and evidence.canonical_frozen
    )
    if frozen_gate:
        return Verification(rid, State.FROZEN, ("all freeze, QA, compatibility, leakage, OOS, and canonical gates are proven",), evidence.evidence_commits)

    if evidence.freeze_manifest or evidence.frozen_snapshot or evidence.production_freeze:
        return Verification(rid, State.INTEGRATION_PENDING, ("freeze evidence exists but the complete freeze gate is not proven",), evidence.evidence_commits)

    if evidence.tests_pass and evidence.historical_qa and evidence.no_lookahead and evidence.oos_2025_clean:
        return Verification(rid, State.QA_COMPLETE, ("required QA, no-lookahead, and OOS protection are proven",), evidence.evidence_commits)

    if evidence.implementation and evidence.compatibility_audit:
        return Verification(rid, State.TECHNICALLY_COMPLETE, ("implementation and compatibility evidence are proven",), evidence.evidence_commits)

    return Verification(rid, State.UNVERIFIED, ("insufficient traceable evidence",), evidence.evidence_commits)


def verify_many(records: Mapping[str, Evidence]) -> list[Verification]:
    """Verify records in stable Rule-ID order without filling missing evidence."""
    return [verify(rule_id, evidence) for rule_id, evidence in sorted(records.items())]


if __name__ == "__main__":
    print("Murphy State Verifier: supply traceable repository evidence records before classification.")
