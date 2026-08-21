# Canonical Pipeline Order — Provenance Recovery — 2026-08-21

## Scope
Resolve the previously unproven execution order between the recovered Knowledge Alignment Adapter, the Risk Boundary, and the existing Decision Brain using canonical backup evidence rather than inference.

## Canonical source inspected
`AI_TRADING_ASSISTANT_COMPLETE_MILESTONE_BACKUP_79RULE_RISK_20260821T022022Z.zip`

Relevant recovered artifacts:
- `local/KNOWLEDGE_ALIGNMENT_CONTRACT_V1.json`
- `local/knowledge_alignment_adapter.py`
- `local/KNOWLEDGE_ALIGNMENT_TO_RISK_ENGINE_BOUNDARY_INTEGRATION_TEST_V1.json`
- `github/governance/KNOWLEDGE_ALIGNMENT_TO_RISK_ENGINE_COMPATIBILITY_CONTRACT_V1.md`

## Direct evidence of order
The recovered Knowledge Alignment Contract states:

`risk`: hard gate downstream of alignment

`decision_brain`: final synthesis downstream

Its output schema sets:

`next_layer = risk_engine_then_existing_decision_brain`

The recovered executable `knowledge_alignment_adapter.py` emits that same `next_layer` value on every return path, including process-blocked, insufficient-evidence, needs-review, contradiction, and aligned/Murphy-only outcomes.

## Canonical recovered order

Market / normalized evidence + existing book evidence
→ Knowledge Alignment Adapter
→ Risk Engine / Risk Boundary hard gate
→ Existing Decision Brain final synthesis

This order is a provenance finding from the recovered canonical artifacts. It is not inferred from the active GitHub search.

## Boundary evidence
The recovered integration test reports:
- status: PASS
- passed: 8
- total: 8
- live execution: NOT_EXECUTION_READY

The recovered governance compatibility contract describes the boundary as `COMPATIBLE_FOR_RESEARCH_BOUNDARY_INTEGRATION_ONLY`.

## Important limitation
This finding does NOT prove that the active workspace currently has a complete runnable implementation of the full chain. The active workspace previously failed to show the canonical adapter and test runtime through indexed search.

Therefore:
- canonical historical order: CONFIRMED
- active end-to-end runtime order: NOT YET VERIFIED
- active end-to-end runtime PASS: NOT CLAIMED
- live execution readiness: NOT CLAIMED

## Correction to earlier uncertainty
The earlier statement that the order was not yet proven in the active repository remains true for the active runtime. However, the canonical backup now directly proves the historical intended/recovered contract order. The two claims must not be conflated.

## Next controlled action
Perform a component-presence and field-contract audit for the exact canonical order:

Knowledge Alignment Adapter → Risk Boundary → Existing Decision Brain

Determine which canonical components are already active, which can be restored as exact recovered artifacts, and which runtime dependencies remain missing. Do not reorder the pipeline without a new governed version.

## Governance
- No BUY/SELL generator created.
- No directional rule added.
- No risk threshold invented.
- No tuning performed.
- 2025 remains locked Out-of-Sample and cannot be used for tuning, calibration, threshold selection, or implementation selection.
