# MURPHY 0006–0007 — FORMAL OPERATIONAL CONTRACT V1

Date: 2026-08-14
Status: FORMAL OPERATIONAL CONTRACT CANDIDATE — GOVERNANCE/FREEZE REVIEW REQUIRED

## 1. Scope

Rules:
- MURPHY_0006: reaction LOWs + UP trendline -> bullish confirmation.
- MURPHY_0007: reaction HIGHs + DOWN trendline -> bearish confirmation.

This contract formalizes the reconciled project operationalization. It does not claim every operational detail is verbatim Murphy text.

## 2. Source semantics

Murphy Chapter 4 source semantics:
- Up trendline connects successive reaction lows.
- Down trendline connects successive reaction highs.
- Two points establish a tentative trendline.
- A third successful touch and reaction without breaking confirms the trendline.
- Trendline validity increases with additional successful tests without breaking.
- Trendline should contain the daily price range.
- Murphy discusses price/time filters as general break-filter concepts.

## 3. Existing canonical inputs

Reuse:
- PIVOT_SEQUENCE_V2
- TRENDLINE_GEOMETRY_V1
- GBPUSD D1 OHLC 2016–2024
- existing Evidence Adapter / Generic Evaluator architecture

Do not rebuild Pivot or Geometry.

## 4. Event ordering and availability

### 4.1 Market chronology
All event chains are ordered by `pivot_timestamp`.

### 4.2 Eligibility
A pivot is eligible only when:
- `pivot_timestamp >= line_available_at`
- `pivot_available_at >= line_available_at`

`available_at` is an information-availability gate, not market-event ordering.

## 5. Third-touch operator

For the applicable rule:
- 0006 expected family = LOW, direction = UP.
- 0007 expected family = HIGH, direction = DOWN.

Select the FIRST eligible same-family confirmed pivot after line availability.

Do not skip the first same-family candidate to manufacture a later third touch.

The candidate must have D1 range intersection with the trendline at the pivot timestamp.

If the first eligible same-family candidate does not touch the line:
- third_touch_detected = false
- no later same-family pivot may replace it.

## 6. Reaction operator

After the accepted third touch, select the next eligible opposite-family confirmed pivot satisfying:
- reaction timestamp >= touch timestamp
- reaction availability >= touch availability
- direction is consistent with the rule's required rebound.

0006:
- reaction must be bullish/away from the UP trendline.

0007:
- reaction must be bearish/away from the DOWN trendline.

If no eligible reaction exists, confirmation remains NOT_EVALUABLE.

## 7. No-break / line-hold operator

Between the accepted third touch and reaction, inspect completed D1 bars using the existing line-hold operationalization.

For UP trendline / 0006:
- completed-bar low must remain on/above the trendline.

For DOWN trendline / 0007:
- completed-bar high must remain on/below the trendline.

Any confirmed violation rejects the candidate.

IMPORTANT: this is the project's deterministic operationalization of Murphy's qualitative “without breaking / line-hold” semantics. It is NOT represented as verbatim Murphy wording.

## 8. Confirmation availability

Confirmation becomes available at `reaction_available_at`.

Never use the reaction timestamp itself as information availability if the pivot is not yet confirmed.

No confirmation may become available before:
- third-touch availability
- reaction availability

## 9. Missing evidence

Missing required evidence returns `NOT_EVALUABLE`.
Do not infer missing touch, reaction, or no-break evidence.

## 10. Explicit exclusions

This contract does NOT introduce:
- ATR tolerance
- pip tolerance
- arbitrary percentage tolerance
- fixed lookback
- automatic 3% filter
- automatic 2-day filter
- 2025 data
- tuning against historical outcomes

Murphy's 3% and 2-day examples remain general break-filter evidence concepts unless a separate project contract explicitly binds them.

## 11. Existing QA evidence

The supplied reconciled local operator was validated against the existing 2016–2024 provisional confirmation artifact:
- 0006: 8 confirmations
- 0007: 7 confirmations
- total: 15
- exact row-level match: 15/15
- operator-only: 0
- reference-only: 0
- availability-before-reaction violations: 0
- 2025+ confirmations: 0
- reconciled unit tests: 7/7 PASS

These are QA evidence, not a production freeze.

## 12. Remaining freeze gates

Before Production Frozen:
1. governance approval of this operational contract;
2. formal evaluator integration;
3. final deterministic test suite;
4. 2016–2024 historical QA sign-off;
5. availability/no-lookahead audit sign-off;
6. provenance/freeze manifest;
7. explicit production-freeze decision.

2025 remains OOS and must not be used for tuning or operator selection.
