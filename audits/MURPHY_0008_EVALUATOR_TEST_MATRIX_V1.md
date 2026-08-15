# Murphy 0008 — Evaluator Test Matrix V1

Status: TEST PLAN — NOT PRODUCTION FROZEN

| ID | Test | Required result |
|---|---|---|
| T01 | Confirmed Pivot LOW available before break | PASS |
| T02 | Missing/unavailable Support | NOT_EVALUABLE |
| T03 | First D1 close below Support | BREAK_CANDIDATE |
| T04 | Second successive D1 close below same Support | DECISIVE_BREAK_CONFIRMED |
| T05 | Gap / intervening close above-or-equal Support | No confirmation |
| T06 | Same-bar second-close confirmation | Forbidden |
| T07 | Future pivot changes historical Support | Forbidden / no-lookahead |
| T08 | Retest on confirmation bar | Forbidden |
| T09 | Retest after confirmation | RETEST_OBSERVATION |
| T10 | Later intersecting bar closes below Support | ROLE_REVERSAL_EVIDENCE |
| T11 | 2025 input | Forbidden |
| T12 | Clustering/tolerance supplied | Forbidden |
| T13 | Event provenance fields complete | PASS |
| T14 | 2016–2024 fresh replay | Required before freeze |

## Acceptance
All deterministic state-transition tests must pass. Any unavailable/ambiguous prerequisite must yield `NOT_EVALUABLE`, not an inferred result.
