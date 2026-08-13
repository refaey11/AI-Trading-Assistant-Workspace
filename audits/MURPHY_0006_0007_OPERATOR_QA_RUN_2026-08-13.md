# Murphy 0006/0007 Operator QA Run — 2026-08-13

## Scope
2016-2024 only. 2025 excluded.

## Reproduction
- Candidate rows: 347
- 0006: 166
- 0007: 181
- Candidate-day D1 range intersections: 0006=32, 0007=30, total=62

## Deterministic candidate chain under review
- Existing same-family LOW/UP or HIGH/DOWN line with two anchors
- Next confirmed same-family pivot after line availability
- Candidate-day D1 range intersects mathematical line
- Next confirmed opposite-family pivot as reaction event
- Directionally consistent reaction
- Completed post-touch D1 ranges respect the directional line-hold condition
- Confirmation availability = reaction pivot V2 availability timestamp

## Unit tests
5 passed in 0.03s

## Result
- 0006: 8 provisional confirmations
- 0007: 7 provisional confirmations
- total: 15 provisional confirmations

## Confirmation availability examples
0006: LOW::55, LOW::59, LOW::80, LOW::106, LOW::205, LOW::214, LOW::216, LOW::239
0007: HIGH::104, HIGH::172, HIGH::236, HIGH::249, HIGH::256, HIGH::270, HIGH::288

## Status
These are NOT production PASS results. The operational chain remains a compatibility candidate because the source does not explicitly define "next opposite-family confirmed pivot" as the reaction operator or provide a numeric reaction magnitude/duration. Production freeze requires formal contract approval, deterministic unit tests, 2016-2024 historical QA, and no-lookahead verification.

No ATR, pip, percentage touch tolerance, fixed lookback, 3%, or automatic 2-day binding was used.
