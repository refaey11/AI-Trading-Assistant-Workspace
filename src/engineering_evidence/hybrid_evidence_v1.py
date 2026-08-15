"""Conservative Hybrid Evidence Pilot.

This module is an engineering layer only. It does not redefine Murphy semantics,
generate direction, or override canonical gates.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


def fuzzy_membership(value: float, low: float, high: float) -> float:
    """Simple monotone membership; parameters are explicit engineering policy."""
    if high <= low:
        raise ValueError("high must be greater than low")
    if value <= low:
        return 0.0
    if value >= high:
        return 1.0
    return (value - low) / (high - low)


@dataclass(frozen=True)
class EngineeringEvidence:
    relative_magnitude: float
    contextual_strength: float
    grade: str
    method_version: str = "ENG-HYBRID-V1"


def grade_engineering_evidence(relative_magnitude: float,
                               contextual_strength: float) -> EngineeringEvidence:
    """Convert engineering measurements to an evidence grade only."""
    score = (relative_magnitude + contextual_strength) / 2.0
    if score >= 0.75:
        grade = "HIGH"
    elif score >= 0.45:
        grade = "MEDIUM"
    else:
        grade = "LOW"
    return EngineeringEvidence(relative_magnitude, contextual_strength, grade)


def evaluate_hybrid(canonical_pass: bool,
                    relative_measure: float,
                    context_measure: float) -> dict:
    """Hard canonical gate dominates engineering evidence.

    A failed canonical gate can never be promoted by a high engineering score.
    """
    evidence = grade_engineering_evidence(
        fuzzy_membership(relative_measure, 0.0, 1.0),
        fuzzy_membership(context_measure, 0.0, 1.0),
    )
    if not canonical_pass:
        return {
            "status": "NOT_EVALUABLE",
            "evidence_only": True,
            "engineering": evidence,
        }
    return {
        "status": "CANONICAL_PASS",
        "evidence_only": True,
        "engineering": evidence,
    }
