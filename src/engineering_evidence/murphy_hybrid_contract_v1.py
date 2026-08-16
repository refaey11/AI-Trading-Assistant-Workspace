"""Contract-only adapter for Murphy Hybrid Evidence Pilot V1.

Consumes canonical evidence and emits engineering evidence separately.
It deliberately does not implement or redefine Murphy pattern semantics.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class MurphyHybridEvidence:
    rule_id: str
    canonical_status: str
    engineering_grade: str
    provenance: str = "ENG-HYBRID-V1"
    evidence_only: bool = True


def combine_canonical_and_engineering(
    rule_id: str,
    canonical_status: str,
    engineering_grade: str,
) -> MurphyHybridEvidence:
    if canonical_status not in {"PASS", "FAIL", "NOT_EVALUABLE"}:
        raise ValueError("invalid canonical status")
    if engineering_grade not in {"LOW", "MEDIUM", "HIGH"}:
        raise ValueError("invalid engineering grade")

    # Engineering evidence never changes canonical status.
    return MurphyHybridEvidence(
        rule_id=rule_id,
        canonical_status=canonical_status,
        engineering_grade=engineering_grade,
    )
