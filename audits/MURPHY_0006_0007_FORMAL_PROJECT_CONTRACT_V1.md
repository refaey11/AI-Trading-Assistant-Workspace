# MURPHY 0006/0007 — FORMAL PROJECT CONTRACT V1

Status: FREEZE CANDIDATE / NOT PRODUCTION FROZEN

## Source-derived semantics
- 0006: reaction lows -> UP trendline -> third successful touch/reaction without a meaningful break -> bullish context.
- 0007: reaction highs -> DOWN trendline -> third successful touch/reaction without a meaningful break -> bearish context.
- Murphy's qualitative line-hold semantics are source-derived; the deterministic predicates below are project operationalization and are not verbatim Murphy wording.

## Canonical lineage
PIVOT_SEQUENCE_V2 -> TRENDLINE_GEOMETRY_V1 -> MURPHY_CONFIRMATION_LAYER -> 0006/0007 EVALUATOR

## Deterministic operational contract
1. Order market events by pivot event timestamp.
2. Use pivot availability only as a no-lookahead eligibility gate.
3. Require pivot timestamp >= line availability and pivot availability >= line availability.
4. Select the first eligible same-family pivot as the third-touch candidate; do not skip it to manufacture a later touch.
5. Require D1 range intersection with the trendline at the third-touch timestamp.
6. Select the next eligible opposite-family confirmed pivot after the touch, with availability >= touch availability and direction consistent with the required rebound.
7. For UP/0006, completed-bar low must remain on/above the line between touch and reaction.
8. For DOWN/0007, completed-bar high must remain on/below the line between touch and reaction.
9. Confirmation becomes available at reaction pivot availability, not merely reaction event timestamp.
10. Missing required evidence -> NOT_EVALUABLE.

## Explicit exclusions
No ATR, pip, arbitrary percentage tolerance, arbitrary lookback, automatic 3% filter, automatic 2-day binding, or 2025 tuning/selection.

## Validation evidence
2016–2024 only:
- 0006: 8 confirmations
- 0007: 7 confirmations
- total: 15
- exact row-level reconciliation: 15/15
- operator-only: 0
- reference-only: 0
- availability/lookahead violations: 0
- 2025 confirmations: 0
- reconciled unit tests: 7/7 PASS

## Freeze boundary
This contract records the validated candidate operationalization. It does NOT itself authorize Production Freeze. Production Freeze requires the final historical QA sign-off, availability/no-lookahead sign-off, provenance/freeze manifest, governance approval, and an explicit freeze decision.
