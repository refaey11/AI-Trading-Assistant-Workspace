# Murphy 0006/0007 Confirmation Availability QA V1

Period: 2016-2024 only. 2025 excluded.

## Canonical upstream
- PIVOT_SEQUENCE_V2
- TRENDLINE_GEOMETRY_V1
- D1 OHLC evidence

## Reproduction
The official candidate population is reproduced as 166 MURPHY_0006 and 181 MURPHY_0007 rows. The official strong-candidate screen reproduces exactly:
- 0006: 32 D1 range intersections
- 0007: 30 D1 range intersections
- total: 62

## Event chain tested
1. two existing same-family anchors
2. next confirmed same-family pivot after line formation
3. candidate-day D1 range intersects the mathematical line
4. next confirmed opposite-family pivot provides the reaction event
5. reaction is directionally consistent with the existing candidate evidence semantics
6. completed D1 bars between touch and reaction do not violate the directional line-hold condition
7. confirmation availability is the reaction pivot V2 availability timestamp, not the reaction pivot timestamp

## Result
- 0006: 32 strong candidates; 8 satisfy the line-hold condition; 8 provisional confirmations
- 0007: 30 strong candidates; 7 satisfy the line-hold condition; 7 provisional confirmations
- total: 15 provisional confirmations

## No-lookahead
The confirmation timestamp is taken from the reaction pivot's V2 availability timestamp. The reaction itself is not considered available merely because its pivot timestamp has occurred.

## Important status
These 15 are NOT production-frozen PASS results. The line-hold step is an operationalization of the source semantics and must still pass provenance/contract approval before production promotion.

No ATR, percentage tolerance, pip tolerance, fixed lookback, 3%, or automatic 2-day binding was introduced.
