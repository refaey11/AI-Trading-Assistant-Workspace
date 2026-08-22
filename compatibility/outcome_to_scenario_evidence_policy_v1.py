"""Governed attachment boundary from Historical Outcome evidence to Market Scenario.

Historical Outcome remains descriptive evidence only. This adapter does not
recompute returns, create thresholds, alter scenario scores/confidence, or
generate trade direction.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional


@dataclass(frozen=True)
class OutcomeScenarioEvidenceResult:
    status: str
    scenario: Mapping[str, Any]
    reason: Optional[str] = None


def attach_outcome_evidence(
    *,
    scenario: Mapping[str, Any],
    memory_package: Mapping[str, Any],
) -> OutcomeScenarioEvidenceResult:
    if not isinstance(scenario, Mapping):
        return OutcomeScenarioEvidenceResult("NOT_EVALUABLE", {}, "INVALID_SCENARIO")
    if not isinstance(memory_package, Mapping):
        return OutcomeScenarioEvidenceResult("NOT_EVALUABLE", {}, "INVALID_MEMORY_PACKAGE")

    required_scenario = {
        "pair", "primary_scenario", "decision", "confidence",
        "bullish_score", "bearish_score", "neutral_score",
    }
    if any(field not in scenario for field in required_scenario):
        return OutcomeScenarioEvidenceResult("NOT_EVALUABLE", {}, "INCOMPLETE_SCENARIO")

    if memory_package.get("memory_role") != "EVIDENCE_ONLY":
        return OutcomeScenarioEvidenceResult("NOT_EVALUABLE", {}, "MEMORY_NOT_EVIDENCE_ONLY")
    if memory_package.get("direction") is not None:
        return OutcomeScenarioEvidenceResult("NOT_EVALUABLE", {}, "MEMORY_DIRECTION_FORBIDDEN")
    if memory_package.get("final_trade_decision") is not None:
        return OutcomeScenarioEvidenceResult("NOT_EVALUABLE", {}, "MEMORY_TRADE_DECISION_FORBIDDEN")

    outcome = memory_package.get("historical_outcome")
    if not isinstance(outcome, Mapping):
        return OutcomeScenarioEvidenceResult("NOT_EVALUABLE", {}, "MISSING_HISTORICAL_OUTCOME_EVIDENCE")

    for forbidden in ("direction", "final_trade_decision", "scenario_classification"):
        if outcome.get(forbidden) is not None:
            return OutcomeScenarioEvidenceResult("NOT_EVALUABLE", {}, "DIRECTIONAL_OUTCOME_EVIDENCE_FORBIDDEN")

    outcome_pair = outcome.get("pair")
    if outcome_pair is not None and outcome_pair != scenario["pair"]:
        return OutcomeScenarioEvidenceResult("NOT_EVALUABLE", {}, "PAIR_MISMATCH")

    attached = dict(scenario)
    attached["historical_outcome_evidence"] = dict(outcome)
    attached["historical_outcome_role"] = "DESCRIPTIVE_EVIDENCE_ONLY"
    attached["historical_outcome_can_override_scenario"] = False
    attached["historical_outcome_used_for_direction"] = False
    attached["final_trade_decision"] = None

    return OutcomeScenarioEvidenceResult("PASS", attached)
