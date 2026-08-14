# Murphy 0006/0007 Formal Operational Contract V1

Status: CANDIDATE / GOVERNANCE REVIEW — NOT PRODUCTION FROZEN

## Scope
This contract formalizes the already-reconciled operational candidate for Murphy 0006 and 0007 without modifying PIVOT_SEQUENCE_V2 or TRENDLINE_GEOMETRY_V1.

## 1. Rule mapping
- MURPHY_0006: LOW reaction/pivot family + UP trendline + BULLISH direction.
- MURPHY_0007: HIGH reaction/pivot family + DOWN trendline + BEARISH direction.

## 2. Upstream requirements
Use existing canonical:
- PIVOT_SEQUENCE_V2
- TRENDLINE_GEOMETRY_V1
- GBPUSD D1 completed-bar OHLC

Preserve availability timestamps and no-lookahead.

## 3. Event ordering
Order market events by pivot/event timestamp, not by availability timestamp. Availability is an eligibility gate only.

Require pivot timestamp >= line availability and pivot availability >= line availability.

## 4. Third-touch operator
After two valid anchors, select the first eligible same-family confirmed pivot as the third-touch candidate.

The candidate must have D1 range intersection with the trendline at the pivot timestamp.

Do not skip the first same-family candidate to manufacture a later third touch. If the first eligible candidate does not touch the line, no later same-family pivot may replace it.

## 5. Reaction operator
After the accepted third touch, select the next eligible opposite-family confirmed pivot satisfying:
- reaction timestamp >= touch timestamp;
- reaction availability >= touch availability;
- direction consistent with the required rebound.

0006: bullish reaction away from the UP trendline.
0007: bearish reaction away from the DOWN trendline.

If no eligible reaction exists, confirmation remains NOT_EVALUABLE.

## 6. No-break / line-hold operator
Between accepted third touch and reaction, inspect completed D1 bars using the existing line-hold operationalization.

0006 / UP: completed-bar low must remain on/above the trendline.

0007 / DOWN: completed-bar high must remain on/below the trendline.

Any confirmed violation rejects the candidate.

This is the project's deterministic operationalization of Murphy's qualitative "without breaking / line-hold" semantics. It is not represented as verbatim Murphy wording.

## 7. Confirmation availability
Confirmation becomes available at reaction_available_at, never merely at reaction timestamp when the reaction pivot is not yet confirmed.

No confirmation may become available before third-touch availability or reaction availability.

## 8. Missing evidence
Missing required evidence returns NOT_EVALUABLE. Do not infer missing touch, reaction, or no-break evidence.

## 9. Explicit exclusions
This contract does not introduce:
- ATR tolerance
- pip tolerance
- arbitrary percentage tolerance
- fixed lookback
- automatic 3% filter
- automatic 2-day filter
- 2025 data
- tuning against historical outcomes

Murphy's general 3% and 2-day break-filter examples are not automatically bound to 0006/0007.

## 10. Existing QA evidence
The reconciled local operator has existing 2016–2024 QA evidence:
- 0006: 8 confirmations
- 0007: 7 confirmations
- total: 15
- exact row-level match to the existing confirmation artifact: 15/15
- operator-only: 0
- reference-only: 0
- availability-before-reaction violations: 0
- 2025+ confirmations: 0
- reconciled unit tests: 7/7 PASS

These are QA evidence, not a production freeze.

## 11. Freeze gates
Before Production Frozen:
1. governance approval of this operational contract;
2. formal evaluator integration;
3. final deterministic test suite;
4. 2016–2024 historical QA sign-off;
5. availability/no-lookahead audit sign-off;
6. provenance/freeze manifest;
7. explicit production-freeze decision.

2025 remains OOS and must not be used for tuning or operator selection.
