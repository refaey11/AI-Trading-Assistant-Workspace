# Murphy 0021–0023 — Evaluator → Adapter Contract Test Matrix V1

Status: TEST SPECIFICATION / NO PRODUCTION SEMANTIC CHANGE

This matrix tests the lossless EvaluatorResult boundary first. It does not assert an unapproved mapping into `NormalizedEvidence`.

| Input | Expected boundary result |
|---|---|
| rule_id=0021, status=PASS, directional_confirmation=UP | source_rule_id=0021, status=PASS, direction=UP, availability preserved |
| rule_id=0022, status=FAIL, directional_confirmation=DOWN | source_rule_id=0022, status=FAIL, direction=DOWN, availability preserved |
| rule_id=0023, status=NOT_EVALUABLE, directional_confirmation=null | source_rule_id=0023, status=NOT_EVALUABLE, direction remains absent/null, availability=false when evaluator marks unavailable |
| any result with missing optional direction | preserve missing direction; do not infer |
| any result with unknown strength/conflict | preserve absent; do not synthesize |

## Required invariants
1. `rule_id` is preserved exactly.
2. `status` is preserved exactly.
3. `NOT_EVALUABLE` never becomes PASS or FAIL.
4. No direct `gate = status` assertion is made at this stage.
5. Adapter/boundary performs no rule calculation.
6. No threshold, lookback, tolerance, or proxy is introduced.
7. No strength or conflict is synthesized.
8. No 2025 data is used.
9. Historical reconciliation must report zero mismatches before Production Freeze.

## Next test gate
After the boundary tests execute successfully, a separate compatibility test must determine whether and how the boundary can be represented by the canonical `NormalizedEvidence` schema. That mapping is not approved by this matrix.

This matrix is not a Production Freeze approval.