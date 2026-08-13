# Murphy 0021–0023 — Evaluator → Adapter Contract Test Matrix V1

Status: TEST SPECIFICATION / NO PRODUCTION SEMANTIC CHANGE

| Input | Expected adapter result |
|---|---|
| rule_id=0021, status=PASS, directional_confirmation=UP | source_rule_id=0021, gate=PASS, direction=UP, available=true |
| rule_id=0022, status=FAIL, directional_confirmation=DOWN | source_rule_id=0022, gate=FAIL, direction=DOWN, available=true |
| rule_id=0023, status=NOT_EVALUABLE, directional_confirmation=null | source_rule_id=0023, gate=NOT_EVALUABLE, available=false |
| any result with missing optional direction | preserve missing direction; do not infer |
| any result with unknown strength/conflict | preserve absent; do not synthesize |

## Required invariants
1. `rule_id` is preserved exactly.
2. `status` is preserved exactly.
3. `NOT_EVALUABLE` never becomes PASS or FAIL.
4. Adapter performs no rule calculation.
5. Adapter introduces no threshold, lookback, tolerance, or proxy.
6. Adapter does not use 2025 data.
7. Historical reconciliation must report zero mismatches before Production Freeze.

This matrix is derived from the proposed V1 contract and is not itself a Production Freeze approval.