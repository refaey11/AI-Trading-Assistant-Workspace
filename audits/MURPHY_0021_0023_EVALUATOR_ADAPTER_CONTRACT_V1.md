# Murphy 0021–0023 — Evaluator → Rule Adapter Contract V1

Date: 2026-08-13
Status: PROPOSED / VALIDATION GATE

## Purpose
Define the smallest interface between the existing 0021–0023 evaluator and the existing Rule Adapter without changing evaluator semantics, adding thresholds, or changing historical evidence.

## Source-backed evaluator output
The existing evaluator is the authority for rule outcome. Its result fields include:
- rule_id
- status: PASS / FAIL / NOT_EVALUABLE
- directional_confirmation
- reason

The adapter must consume these results; it must not recompute them.

## Adapter normalization
For each evaluator result, the adapter may normalize only the existing result into the existing adapter vocabulary:
- source_rule_id = rule_id
- gate = status
- direction = directional_confirmation when present
- available = true only when the evaluator result is not NOT_EVALUABLE
- strength = absent unless already supplied by an approved upstream source
- conflict = absent unless already supplied by an approved upstream source

No inferred strength, conflict, threshold, lookback, or direction may be created by the adapter.

## Critical status rule
NOT_EVALUABLE remains NOT_EVALUABLE/available=false. It must never be converted to PASS or FAIL.

## No semantic changes
This contract does not alter:
- 0021/0022/0023 rule semantics
- Volume evidence
- CFTC futures OI evidence
- availability timestamps
- historical period
- 2025 OOS exclusion

## Validation required before production freeze
1. Unit-test the mapping for PASS, FAIL, and NOT_EVALUABLE.
2. Verify rule_id is preserved exactly.
3. Verify directional_confirmation is preserved when present.
4. Verify no new threshold or inferred field is introduced.
5. Reconcile adapter outputs against the existing 122,943-row independent evaluator result set.
6. Any mismatch blocks freeze.

## Status
This is a contract proposal for validation. It does not itself grant Production Freeze.