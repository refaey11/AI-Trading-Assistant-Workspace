"""Normalize existing book-rule outputs into Decision Brain evidence.

This adapter does not contain or rewrite registry rules and does not invent
strategy thresholds. It only validates/normalizes an already-produced rule
result for downstream evaluation.
"""
from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class NormalizedRuleEvidence:
    module: str
    statement: str
    direction: str
    strength: float
    available: bool
    source_rule_id: str | None
    gate: str
    conflict: str
    decision_hint: str
    confidence_delta: float


def _bounded(value: Any, lo: float = 0.0, hi: float = 1.0) -> float:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return 0.0
    return max(lo, min(hi, x))


def normalize_rule_result(raw: Mapping[str, Any]) -> NormalizedRuleEvidence:
    """Normalize one existing rule output without creating new trading logic."""
    direction = str(raw.get("direction", "neutral"))
    if direction not in {"bullish", "bearish", "neutral"}:
        direction = "neutral"

    gate = str(raw.get("gate", "needs_review"))
    if gate not in {"pass", "fail", "needs_review"}:
        gate = "needs_review"

    conflict = str(raw.get("conflict", "insufficient"))
    if conflict not in {"supports", "contradicts", "neutral", "insufficient"}:
        conflict = "insufficient"

    hint = str(raw.get("decision_hint", "neutral"))
    if hint not in {"bullish", "bearish", "neutral", "no_trade"}:
        hint = "neutral"

    delta = max(-1.0, min(1.0, float(raw.get("confidence_delta", 0.0) or 0.0)))

    return NormalizedRuleEvidence(
        module=str(raw.get("module", "RuleAdapter")),
        statement=str(raw.get("statement", "")),
        direction=direction,
        strength=_bounded(raw.get("strength", 0.0)),
        available=bool(raw.get("available", False)),
        source_rule_id=(str(raw["source_rule_id"]) if raw.get("source_rule_id") is not None else None),
        gate=gate,
        conflict=conflict,
        decision_hint=hint,
        confidence_delta=delta,
    )
