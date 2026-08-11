# Murphy 0006–0007 Verification V2

Date: 2026-08-12

## Source-backed findings

The preserved project artifacts confirm:
- MURPHY_0006 and MURPHY_0007 are present in the Rule Registry.
- Both registry entries use the condition: `A third successful touch and reaction confirms the trendline.`
- Existing Trendline Geometry V1 must be reused.
- PIVOT_SEQUENCE_V2 uses confirmed pivots with availability at pivot timestamp + 2 bars and no lookahead before availability.

The preserved Murphy source semantics establish the qualitative trendline distinction:
- uptrend line uses successive reaction lows;
- downtrend line uses successive reaction highs;
- confirmation is associated with a third successful touch/reaction without breaking the trendline.

## Working mapping

The project handoff records the working operational split:
- 0006 → LOW + UP → BULLISH
- 0007 → HIGH + DOWN → BEARISH

However, the authoritative Rule Registry row-level record distinguishing 0006 from 0007 is not currently retrievable in the available search excerpts. Therefore this remains **WORKING RESOLUTION / SOURCE-LOCK PENDING**, not Frozen.

## Compatibility audit

Existing upstream components:
- PIVOT_SEQUENCE_V2: available and availability-aligned.
- TRENDLINE_GEOMETRY_V1: available.

Required evaluator evidence:
1. two valid trendline anchors;
2. LOW/HIGH line family;
3. UP/DOWN direction;
4. third touch;
5. successful reaction;
6. no break;
7. availability timestamp / no-lookahead.

The currently retrievable contract evidence proves the existence of the geometry component and the qualitative source semantics, but does not prove that Geometry V1 emits all seven required fields, especially an operational `successful_reaction` representation.

## Decision

**MURPHY_0006–0007 = MAPPING COMPATIBLE / EVALUATOR NOT CLOSED**

Do not implement a new evaluator yet.

Do not invent:
- touch tolerance;
- reaction distance;
- ATR threshold;
- percentage threshold;
- lookback;
- candle-count confirmation;
- close-vs-wick rule.

## Next action

Retrieve the actual Trendline Geometry V1 contract/output and the original Rule Registry rows. If the existing upstream artifacts expose the required evidence, add only the missing adapter/evaluator and tests. If `successful_reaction` remains undefined, retain NOT_EVALUABLE for that portion and continue forward.

2025 remains OOS and must not be used for tuning or implementation selection.
