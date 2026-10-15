# Murphy 0021–0023 — Evaluator Result Boundary V1

Date: 2026-08-13
Scope: 0021–0023 only
Status: PROPOSED VALIDATION CONTRACT — NOT PRODUCTION FROZEN

## Purpose
Define the smallest lossless boundary between the existing 0021–0023 evaluator and the canonical Rule Adapter. This document does not change evaluator semantics and does not replace the canonical adapter.

## Canonical evaluator result
The boundary carries the evaluator result without recomputation:

- `rule_id`
- `status`: `PASS | FAIL | NOT_EVALUABLE`
- `directional_confirmation`: preserve when supplied; otherwise null/missing
- `confirmation_available_timestamp`: preserve when supplied
- `reason`: preserve source reason

## Boundary invariants
1. `rule_id` is preserved exactly.
2. `status` is preserved exactly.
3. `NOT_EVALUABLE` remains `NOT_EVALUABLE` at this boundary.
4. No direction is inferred when `directional_confirmation` is absent.
5. No strength is inferred.
6. No conflict is inferred.
7. No threshold, lookback, tolerance, proxy, or recalculation is introduced.
8. No 2025 data is used.
9. The evaluator remains the authority for 0021–0023 rule outcome.

## Explicit non-mapping decision
This boundary intentionally does NOT map `NOT_EVALUABLE` to the canonical adapter gate `needs_review` yet. That would be a semantic mapping decision and requires a separate approved compatibility test against the canonical Decision Brain contract.

Likewise, `PASS/FAIL` are not yet written into `NormalizedEvidence.gate` by this boundary. The purpose here is to establish a lossless transport boundary first.

## Required test cases
A conforming implementation must prove:

- PASS + direction survives unchanged.
- FAIL + direction survives unchanged.
- NOT_EVALUABLE + null direction survives unchanged.
- Missing optional direction remains missing.
- Unknown strength/conflict remain absent.
- Rule IDs cannot be altered.

## Next gate
After this boundary is implemented and unit-tested, perform a compatibility test against the canonical Rule Adapter schema. Only if the mapping is source-safe and contract-safe may an integration mapping be implemented.

## Freeze rule
This boundary document grants no Production Freeze. The existing requirement remains: adapter integration must reconcile against the existing 122,943-row independent evaluator result set with zero mismatches before Freeze.