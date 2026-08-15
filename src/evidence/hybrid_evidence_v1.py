"""Conservative engineering evidence helpers for the Murphy pilot.

These functions never emit a trade direction and never override canonical gates.
They are project engineering measurements, not Murphy methodology claims.
"""

from math import exp


def require_canonical_gate(passed: bool) -> bool:
    """Hard gate: engineering evidence cannot rescue canonical failure."""
    return bool(passed)


def relative_position(value: float, low: float, high: float) -> float:
    """Normalized position in [0, 1]; deterministic and parameter-free."""
    if high <= low:
        raise ValueError("high must be greater than low")
    return max(0.0, min(1.0, (value - low) / (high - low)))


def fuzzy_membership(value: float, low: float, high: float) -> float:
    """Simple monotonic fuzzy membership for a qualitative engineering feature.

    The function is intentionally generic; its bounds are supplied by a
    versioned engineering contract and are never attributed to Murphy.
    """
    if high <= low:
        raise ValueError("high must be greater than low")
    x = max(0.0, min(1.0, (value - low) / (high - low)))
    return x


def evidence_grade(score: float) -> str:
    """Map an engineering score to an ordinal label; not a trading signal."""
    if not 0.0 <= score <= 1.0:
        raise ValueError("score must be in [0, 1]")
    if score < 1 / 3:
        return "LOW"
    if score < 2 / 3:
        return "MEDIUM"
    return "HIGH"


def gated_evidence(canonical_pass: bool, score: float) -> dict:
    """Return auditable evidence while enforcing the hard-gate boundary."""
    if not canonical_pass:
        return {
            "canonical": "FAIL",
            "engineering_score": None,
            "engineering_grade": "NOT_APPLICABLE",
            "decision": "NOT_EVALUABLE",
        }
    return {
        "canonical": "PASS",
        "engineering_score": round(float(score), 6),
        "engineering_grade": evidence_grade(float(score)),
        "decision": "EVIDENCE_ONLY",
    }
