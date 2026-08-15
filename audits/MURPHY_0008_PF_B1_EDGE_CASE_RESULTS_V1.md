# Murphy 0008 — PF-B1 Edge-Case Results V1

Status: EXPERIMENTAL / NOT FROZEN
Policy under test: two successive completed D1 closes below support.

| Case | Expected | Result |
|---|---|---|
| Intrabar low below support, close above | NOT_CONFIRMED | PASS |
| One close below, next close back above | NOT_CONFIRMED | PASS |
| Two successive completed D1 closes below | CONFIRMED | PASS |
| First close below, second bar unavailable | NOT_EVALUABLE | PASS |
| Support becomes available only after alleged break | REJECT / no confirmation | PASS |
| Retest occurs on confirmation bar | Confirmation may exist; retest evidence excluded | PASS |

## Temporal rule
The confirmation event becomes available only at the close of the second qualifying D1 bar. Any downstream rally/retest evidence must use bars strictly after that confirmation bar.

## Important limitation
These are deterministic contract/edge-case tests, not a claim that the policy is the final Murphy 0008 production rule. Historical policy selection must not be tuned from outcome performance. 2025 remains excluded/OOS.

## Gate status
Edge-case logic: PASS.
No-lookahead contract: PASS at specification level.
Production implementation integration: NOT YET COMPLETE.
Governance freeze: BLOCKED.
