#!/usr/bin/env python3
"""Murphy Rule State Verifier.

Evidence-first verifier scaffold. It never trusts chat memory or a single
status document as authoritative. A rule is FROZEN only when explicit freeze
evidence is present in the repository evidence index supplied to this tool.

This module is intentionally conservative: missing/ambiguous evidence yields
UNVERIFIED or CONFLICT rather than an inferred completion.
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
    blocker_closed: bool = False
    freeze_manifest: bool = False
    frozen_snapshot: bool = False
    production_freeze: bool = False
    merged_main: bool = False
    canonical_frozen: bool = False
    oos_2025_clean: bool = False
    evidence_commits: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class Verification:
    rule_id: str
    state: State
    reasons: tuple[str, ...]
    evidence_commits: tuple[str, ...]


def verify(rule_id: str, evidence: Evidence, conflicting_states: Iterable[str] = ()) -> Verification:
    """Return the most conservative evidence-backed state for one Rule."""
    rid = str(rule_id).zfill(4)
    conflicts = {str(x).upper() for x in conflicting_states}
    if len(conflicts) > 1:
        return Verification(rid, State.CONFLICT, ("multiple conflicting state assertions",), evidence.evidence_commits)

    if evidence.production_freeze and evidence.freeze_manifest and evidence.canonical_frozen:
        return Verification(rid, State.FROZEN, ("explicit production freeze + freeze manifest + canonical frozen state",), evidence.evidence_commits)

    if evidence.freeze_manifest or evidence.frozen_snapshot:
        return Verification(rid, State.INTEGRATION_PENDING, ("freeze evidence exists but full production-freeze proof is incomplete",), evidence.evidence_commits)

    if evidence.tests_pass and evidence.historical_qa and evidence.no_lookahead:
        return Verification(rid, State.QA_COMPLETE, ("QA evidence passes but production freeze is not proven",), evidence.evidence_commits)

    if evidence.implementation and evidence.compatibility_audit:
        return Verification(rid, State.TECHNICALLY_COMPLETE, ("implementation and compatibility evidence exist",), evidence.evidence_commits)

    return Verification(rid, State.UNVERIFIED, ("insufficient traceable evidence",), evidence.evidence_commits)


def verify_many(records: Mapping[str, Evidence]) -> list[Verification]:
    """Verify records while refusing to infer missing evidence."""
    return [verify(rule_id, evidence) for rule_id, evidence in sorted(records.items())]


if __name__ == "__main__":
    print("Murphy State Verifier scaffold: supply repository evidence records before classification.")
