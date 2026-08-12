# Murphy 0006–0007 Final Compatibility Audit V3

Date: 2026-08-12
Status: COMPATIBLE UPSTREAM / OPERATOR BLOCKED

## Direct evidence inspected

The full GBPUSD_RULE_EVALUATOR_V2 multipart workspace was reconstructed locally and inspected directly. The following artifacts were read from the archive:

- `MURPHY_0006_TO_0010_EXACT_MAPPING_V1.csv`
- `TRENDLINE_GEOMETRY_CONTRACT_V1.json`
- `TRENDLINE_GEOMETRY_V1_OUTPUT/TRENDLINE_GEOMETRY_BUILD_CONTRACT_V1.json`
- `TRENDLINE_GEOMETRY_V1_OUTPUT/TRENDLINE_GEOMETRY_MANIFEST_V1.csv`
- `TRENDLINE_GEOMETRY_V1_OUTPUT/TRENDLINE_GEOMETRY_QA_V1.csv`
- actual timeframe trendline CSV outputs

## 0006 / 0007 exact mapping

0006:
- Confirmed uptrend line
- successive reaction lows
- two points create tentative line
- third successful touch + reaction confirms trendline
- operator recorded as `third touch followed by reaction away from line`
- status remains `NOT_YET_EVALUABLE`
- reason: successful touch/reaction needs approved operational definition

0007:
- Confirmed downtrend line
- successive reaction highs
- two points create tentative line
- third successful touch + reaction confirms trendline
- operator recorded as `third touch followed by reaction away from line`
- status remains `NOT_YET_EVALUABLE`
- reason: successful touch/reaction needs approved operational definition

## Geometry V1 direct schema

Actual trendline CSV columns:
- line_id
- line_type
- point_1_timestamp
- point_1_price
- point_2_timestamp
- point_2_price
- slope_price_per_second
- direction
- availability_timestamp
- point_1_availability
- point_2_availability
- source_file

Actual Geometry V1 build contract states:
- input = PIVOT_SEQUENCE_V2
- consecutive same-type pivots only
- exact slope = price change / elapsed seconds
- availability = later confirmation timestamp of defining pivots
- breakout detection = excluded
- thresholds_added = false
- 2025_used = false
- no-lookahead: line unavailable before both defining pivots are confirmed

## What Geometry provides

Geometry provides sufficient upstream evidence for:
- two anchors
- LOW/HIGH line family
- UP/DOWN direction
- line availability
- pivot lineage

## What Geometry does not provide

Actual output does not contain:
- third_touch_timestamp
- third_touch_price
- third_touch_detected
- reaction_detected
- reaction_direction
- no_break_valid
- confirmation_timestamp

## Existing break feature search

The workspace contains generic `break_structure_up` / `break_structure_down` features, but the 0008/0009 mapping explicitly says the decisive-break condition still needs an approved definition. No 0006/0007-specific `no_break` contract was found.

Therefore these generic break fields cannot be silently promoted to a 0006/0007 no-break operator.

## Decision

Do not modify Trendline Geometry V1.
Do not bind Murphy general 3% or 2-consecutive-day examples to 0006/0007.
Do not invent touch tolerance, reaction magnitude, lookback, ATR, pip or percentage thresholds.

The correct current architecture is:

PIVOT_SEQUENCE_V2
→ TRENDLINE_GEOMETRY_V1
→ MURPHY_CONFIRMATION_LAYER
→ 0006/0007 EVALUATOR

The upstream compatibility gate is PASS.
The exact confirmation operator gate remains OPEN.

Production status remains:
- MURPHY_0006 = NOT_EVALUABLE
- MURPHY_0007 = NOT_EVALUABLE

The previously created evidence gate is retained as a non-inventive adapter. It can consume explicit upstream evidence but must not manufacture missing touch/reaction/no-break evidence.

## Next authorized implementation step

Create/approve the smallest missing `MURPHY_0006_0007_TOUCH_REACTION_OPERATOR_V1` contract only after an authoritative source/project operator is found. Until then, preserve NOT_EVALUABLE and do not tune on 2025.
