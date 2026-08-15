#!/usr/bin/env python3
"""Deterministic, evidence-first Murphy Rule state verifier."""

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
    blocker_closure_traceable: bool = False
    blocker_closed_after_open: bool = False
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
    def no_unresolved_blocker(self) -> bool:
        if not self.blocker_open:
            return True
        return (
            self.blocker_closed
            and self.blocker_closure_traceable
            and self.blocker_closed_after_open
        )


@dataclass(frozen=True)
class Verification:
    rule_id: str
    state: State
    reasons: tuple[str, ...]
    evidence_commits: tuple[str, ...]


def verify(
    rule_id: str,
    evidence: Evidence,
    conflicting_states: Iterable[str] = (),
) -> Verification:
    """Return the strongest state justified by the supplied evidence.

    No chat claim, frozen-rule allowlist, or single status assertion can promote
    a rule. Conflicts and safety violations take precedence over completion.
    """
    rid = str(rule_id).zfill(4)
    conflicts = {str(x).upper() for x in conflicting_states}

    if len(conflicts) > 1:
        return Verification(
            rid,
            State.CONFLICT,
            ("multiple conflicting authoritative state assertions",),
            evidence.evidence_commits,
        )

    if evidence.oos_2025_used_for_forbidden_purpose:
        return Verification(
            rid,
            State.BLOCKED,
            ("2025 OOS used for a forbidden tuning/selection/calibration/optimization purpose",),
            evidence.evidence_commits,
        )

    if evidence.future_data_contamination:
        return Verification(
            rid,
            State.BLOCKED,
            ("future-data/lookahead contamination is present",),
            evidence.evidence_commits,
        )

    if not evidence.no_unresolved_blocker:
        return Verification(
            rid,
            State.BLOCKED,
            ("active authoritative blocker remains unresolved",),
            evidence.evidence_commits,
        )

    frozen_gate = (
        evidence.implementation
        and evidence.tests_pass
        and evidence.historical_qa
        and evidence.no_lookahead
        and evidence.compatibility_audit
        and evidence.no_unresolved_blocker
        and evidence.freeze_manifest
        and evidence.frozen_snapshot
        and evidence.production_freeze
        and evidence.canonical_frozen
        and evidence.oos_2025_clean
    )
    if frozen_gate:
        return Verification(
            rid,
            State.FROZEN,
            ("all required implementation, QA, compatibility, freeze, canonical, and OOS gates are proven",),
            evidence.evidence_commits,
        )

    if evidence.tests_pass and evidence.historical_qa and evidence.no_lookahead:
        return Verification(
            rid,
            State.QA_COMPLETE,
            ("required QA evidence passes but the complete production-freeze gate is not proven",),
            evidence.evidence_commits,
        )

    if evidence.implementation and evidence.compatibility_audit:
        return Verification(
            rid,
            State.TECHNICALLY_COMPLETE,
            ("implementation and compatibility evidence exist",),
            evidence.evidence_commits,
        )

    if evidence.freeze_manifest or evidence.frozen_snapshot:
        return Verification(
            rid,
            State.INTEGRATION_PENDING,
            ("freeze evidence exists but the complete production-freeze proof is incomplete",),
            evidence.evidence_commits,
        )

    return Verification(
        rid,
        State.UNVERIFIED,
        ("insufficient traceable evidence",),
        evidence.evidence_commits,
    )


def verify_many(records: Mapping[str, Evidence]) -> list[Verification]:
    """Verify records in stable Rule-ID order without inferring missing evidence."""
    return [verify(rule_id, evidence) for rule_id, evidence in sorted(records.items())]


if __name__ == "__main__":
    print("Murphy State Verifier: supply repository evidence records before classification.")
