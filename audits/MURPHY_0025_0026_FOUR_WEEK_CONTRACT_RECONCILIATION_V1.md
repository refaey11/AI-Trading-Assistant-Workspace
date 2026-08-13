# Murphy 0025–0026 — Four-Week Contract Reconciliation V1

Status: BLOCKED PENDING CONTRACT RECONCILIATION — NO EVALUATOR IMPLEMENTED
Date: 2026-08-13

## Source / project facts
- MURPHY_0025 = Four-week breakout: price reaches a new four-week high.
- MURPHY_0026 = Four-week breakdown: price reaches a new four-week low.
- Existing FOUR_WEEK_LOOKBACK_V1 is the required reusable feature. No new lookback may be built.
- Project status remains SOURCE/FEATURE COMPATIBLE / VALIDATION PENDING; evaluator, tests, and historical QA are not complete.

## Canonical feature artifacts found in the supplied Workspace archive
`FOUR_WEEK_LOOKBACK_V1_OUTPUT/FOUR_WEEK_LOOKBACK_CONTRACT_V1.json` states:
- preceding four completed calendar weeks;
- current week excluded;
- no fixed-bar substitution;
- outputs include four_week_high, four_week_low, new_four_week_high, new_four_week_low and lookback_reference_end.

`FOUR_WEEK_LOOKBACK_V1_OUTPUT/FOUR_WEEK_LOOKBACK_BUILD_CONTRACT_FINAL_V1.json` states:
- four completed ISO calendar weeks preceding current ISO week;
- current week excluded;
- price basis = HIGH for four-week high and LOW for four-week low;
- 2025 not used.

## Critical unresolved contradiction
The earlier feature contract contains:
`price_field = close`

The final build contract contains:
`price_basis = high for four-week high; low for four-week low`

The rule mapping artifacts describe the operator as `current price >= highest price in the preceding four-week window` for 0025 and `current price <= lowest price in the approved preceding four-week window` for 0026, without resolving whether current price means close or the bar's high/low.

Therefore the exact Feature → Operator contract is NOT yet source-locked.

## Decision
Do NOT implement 0025/0026 evaluator yet.
Do NOT choose close vs high/low by convention.
Do NOT create a 20-bar/20-day substitute.
Do NOT tune the choice using historical performance.
Do NOT use 2025.

## Required next gate
Reconcile the conflicting `price_field=close` vs `price_basis=high/low` definitions against the authoritative Murphy source / Master Rule Database and record one canonical contract. Then:
1. reuse FOUR_WEEK_LOOKBACK_V1;
2. implement only the smallest missing evaluator;
3. add deterministic tests for high/low breakout and non-break cases;
4. run 2016–2024 historical QA;
5. perform availability/leakage checks;
6. keep 2025 locked OOS;
7. only then consider Freeze.

This audit is documentation only. It does not change existing feature artifacts or rule semantics.