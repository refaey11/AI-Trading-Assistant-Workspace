"""Final E2E readiness boundary for the governed Decision Brain.

This is a readiness/governance harness, not a profitability backtest.
It deliberately fails closed for execution when authoritative TIZ/Risk
producers are unavailable and keeps 2025 locked in development.
"""
from __future__ import annotations

from typing import Any, Mapping

from compatibility.decision_brain_v1_handoff_adapter import assess_with_governance


def run_final_e2e_readiness(
    decision_brain_module,
    *,
    row: Mapping[str, Any],
    query_as_of: Any,
    murphy_evidence: Mapping[str, Any] | None = None,
    nison_evidence: Mapping[str, Any] | None = None,
    tiz_evidence: Mapping[str, Any] | None = None,
    risk_evidence: Mapping[str, Any] | None = None,
    historical_evidence: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    result = assess_with_governance(
        decision_brain_module,
        row=row,
        query_as_of=query_as_of,
        mode="development",
        murphy_evidence=murphy_evidence,
        nison_evidence=nison_evidence,
        tiz_evidence=tiz_evidence,
        risk_evidence=risk_evidence,
        historical_evidence=historical_evidence,
        provenance={"test": "final_e2e_readiness_v1"},
    )

    if result.get("status") != "PASS":
        return result

    execution = result["execution"]
    # Readiness must never claim production execution eligibility unless
    # authoritative TIZ and Risk gates actually pass.
    execution["eligible"] = bool(execution.get("eligible")) and bool(
        (tiz_evidence or {}).get("authoritative", False)
        and (risk_evidence or {}).get("authoritative", False)
    )
    if not execution["eligible"]:
        execution["needs_review"] = list(execution.get("needs_review", []))
        for marker in ("TIZ_NOT_PRODUCTION_AUTHORIZED", "RISK_NOT_PRODUCTION_AUTHORIZED"):
            if marker not in execution["needs_review"]:
                execution["needs_review"].append(marker)

    result["execution"] = execution
    result["governance"]["final_e2e_is_profitability_test"] = False
    result["governance"]["production_execution_claimed"] = execution["eligible"]
    return result
