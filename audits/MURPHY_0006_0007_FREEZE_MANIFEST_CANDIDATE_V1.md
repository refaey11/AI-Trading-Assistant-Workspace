# Murphy 0006/0007 — Freeze Manifest Candidate V1

Status: CANDIDATE / NOT PRODUCTION FROZEN

## Scope
Murphy 0006 and 0007 only. 2025 is excluded from tuning and operator selection.

## Source semantics
- 0006: reaction lows -> UP trendline -> third successful touch/reaction -> bullish confirmation.
- 0007: reaction highs -> DOWN trendline -> third successful touch/reaction -> bearish confirmation.
- Murphy Chapter 4 establishes the qualitative third-test/reaction/without-breaking semantics.

## Canonical upstream lineage
PIVOT_SEQUENCE_V2 -> TRENDLINE_GEOMETRY_V1 -> MURPHY_CONFIRMATION_LAYER -> 0006/0007 evaluator.
Existing upstream components are reused; no rebuild is authorized.

## Candidate deterministic operationalization
1. Order market events by pivot timestamp.
2. Use pivot availability only as the no-lookahead eligibility gate.
3. Select the first eligible same-family pivot; do not skip it to manufacture a later touch.
4. Require D1 range intersection at the touch timestamp.
5. Select the next eligible opposite-family confirmed pivot with directional reaction.
6. Require completed D1 line-hold evidence between touch and reaction.
7. Confirmation availability = reaction pivot availability.
8. Missing evidence => NOT_EVALUABLE.

## Explicit exclusions
No ATR tolerance, pip tolerance, arbitrary percentage tolerance, fixed lookback, automatic 3% filter, automatic 2-day filter, or 2025 tuning.

## QA evidence currently recorded in project artifacts
- 0006: 8 provisional confirmations
- 0007: 7 provisional confirmations
- Total: 15
- Reference/operator exact match: 15/15
- Operator-only: 0
- Reference-only: 0
- Availability/leakage violations: 0
- 2025+ confirmations: 0
- Reconciled unit tests: 7/7 PASS

## Important evidence boundary
The 15/15 result is QA/reconciliation evidence against the existing confirmation artifact. It is not by itself proof that a fresh end-to-end 2016–2024 rerun has been executed from raw Pivot V2 + Geometry V1 inputs in the current runtime. The project record explicitly distinguishes this limitation.

## Freeze gates
- Governance approval: PENDING
- Formal evaluator integration: PENDING
- Final deterministic suite: PENDING
- Fresh 2016–2024 end-to-end QA sign-off: PENDING
- Availability/no-lookahead sign-off: PENDING
- Provenance/freeze manifest: THIS CANDIDATE MANIFEST
- Explicit production-freeze decision: PENDING

## Decision
Do not merge this manifest as a production freeze and do not label 0006/0007 Production Frozen until every pending gate above is independently evidenced and approved.

## Next exact action
Run the candidate operator against the canonical Pivot V2 + Geometry V1 datasets for 2016–2024, produce a reproducible evaluator artifact, reconcile it against the 15 provisional confirmations, and attach the run/provenance hashes to the final freeze manifest. Keep 2025 untouched.
