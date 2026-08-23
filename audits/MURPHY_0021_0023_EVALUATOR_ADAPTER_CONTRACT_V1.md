# Murphy 0021–0023 — Evaluator → Rule Adapter Contract V1

Date: 2026-08-13
Status: PROPOSED / VALIDATION GATE — MAPPING NOT YET APPROVED

## Purpose
Define the smallest interface between the existing 0021–0023 evaluator and the existing Rule Adapter without changing evaluator semantics, adding thresholds, or changing historical evidence.

## Source-backed evaluator output
The existing evaluator is the authority for rule outcome. Its result fields include:
- `rule_id`
- `status`: `PASS | FAIL | NOT_EVALUABLE`
- `directional_confirmation`
- `reason`
- availability information when supplied by the evaluator lineage

The adapter boundary must consume these results; it must not recompute them.

## Critical compatibility finding
The canonical `NormalizedEvidence` schema currently requires:
- `direction`
- `strength`
- `available`
- `gate`
- `conflict`

Its gate vocabulary is narrower than the evaluator vocabulary and does not include `NOT_EVALUABLE` as a native gate value. The existing Adapter also derives direction/strength from registry-rule inputs.

Therefore this contract MUST NOT claim a direct field-for-field mapping such as `gate = status`.

## Approved boundary behavior for this validation stage
Create a lossless evaluator-result boundary carrying:
- `source_rule_id = rule_id`
- `status` unchanged
- `directional_confirmation` unchanged when present
- availability information unchanged
- `reason` unchanged

At this stage:
- `PASS` is not yet written into `NormalizedEvidence.gate`.
- `FAIL` is not yet written into `NormalizedEvidence.gate`.
- `NOT_EVALUABLE` is not converted to `needs_review`, `fail`, or `pass`.
- No `strength` is inferred.
- No `conflict` is inferred.
- No direction is inferred when the evaluator does not supply one.

## No semantic changes
This contract does not alter:
- 0021/0022/0023 rule semantics
- Volume evidence
- CFTC futures OI evidence
- availability timestamps
- historical period
- 2025 OOS exclusion

## Required validation gates
1. Unit-test the lossless boundary for PASS, FAIL, and NOT_EVALUABLE.
2. Verify `rule_id` is preserved exactly.
3. Verify `directional_confirmation` is preserved when present.
4. Verify no new threshold, lookback, tolerance, proxy, strength, or conflict is introduced.
5. Perform a separate compatibility test against the canonical Adapter/Decision Brain contract before any mapping into `NormalizedEvidence`.
6. Reconcile the approved integration against the existing 122,943-row independent evaluator result set.
7. Any mismatch blocks Production Freeze.

## Status
This is a contract proposal for validation. It does not itself grant Production Freeze.
