# Murphy 0021–0023 — Canonical Adapter Mapping Proposal V1
Date: 2026-08-15
Status: PROPOSAL — NOT PRODUCTION FROZEN

## Source-backed inputs
The evaluator is already implemented and unit-tested for MURPHY_0021, MURPHY_0022 and MURPHY_0023. It uses completed-close price direction, existing volume_direction, and CFTC British Pound futures OI direction; no thresholds or spot-FX OI proxy are added; runtime timeframe is Dynamic MTF; 2025 is excluded.

## Objective
Map evaluator output into the existing Rule Adapter without changing evaluator semantics or duplicating rules.

## Non-negotiable boundary
The evaluator result must first be preserved losslessly. The adapter must not infer fields that the evaluator did not provide.

Preserve:
- rule_id
- status: PASS | FAIL | NOT_EVALUABLE
- directional_confirmation (when present)
- reason (when present)
- confirmation/availability timestamp (when present)

## Proposed canonical mapping
This is the smallest candidate mapping and requires approval before implementation:

### PASS
- available = true, only when required evaluator inputs were available at the evaluator's availability timestamp.
- direction = directional_confirmation only when explicitly present; otherwise neutral.
- gate = pass.
- conflict = supports when an explicit directional confirmation is present; otherwise neutral.
- decision_hint = directional_confirmation when explicit; otherwise neutral.
- confidence_delta = 0.

### FAIL
- available = true only when the evaluator had the required inputs and deterministically established the rule condition was not satisfied.
- direction = directional_confirmation only if the evaluator explicitly supplied one; otherwise neutral.
- gate = fail.
- conflict = contradicts only when an explicit directional confirmation is present and the failure is a contradiction under the approved rule contract; otherwise insufficient/neutral as approved.
- decision_hint = no_trade.
- confidence_delta = 0.

### NOT_EVALUABLE
- available = false.
- gate = needs_review.
- conflict = insufficient.
- direction = explicit directional_confirmation only if present; otherwise neutral.
- decision_hint = neutral (not a trade direction).
- confidence_delta = 0.

## Important qualification
The above PASS/FAIL/NOT_EVALUABLE mapping is a proposal, not an approved contract. In particular, the project must approve the semantic relationship between evaluator status and adapter gate before production implementation. No status mapping should be silently assumed to be authoritative.

## Prohibited changes
- No new threshold.
- No new timeframe.
- No OI proxy.
- No historical tuning.
- No 2025 tuning/selection.
- No modification of evaluator semantics.
- No Decision Brain rebuild.
- No Similarity override.

## Required validation after approval
1. Implement only the approved mapping in the existing adapter layer.
2. Run deterministic adapter tests covering PASS, FAIL and NOT_EVALUABLE for 0021, 0022 and 0023.
3. Verify direction is never invented.
4. Verify missing evidence cannot become PASS.
5. Reconcile the full historical result artifact row-for-row.
6. Run availability/no-lookahead checks.
7. Produce final provenance/freeze manifest.
8. Production Freeze only after every gate passes.
