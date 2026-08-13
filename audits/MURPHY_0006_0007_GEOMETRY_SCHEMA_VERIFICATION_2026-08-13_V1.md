# Murphy 0006–0007 — Geometry V1 Schema Verification V1
Date: 2026-08-13
Status: VERIFIED / CONFIRMATION UPSTREAM GATE REMAINS OPEN

## Source inspected
Reconstructed canonical GBPUSD_RULE_EVALUATOR_V2 workspace transfer (241-file workspace, ~597,678,846 bytes) was successfully reassembled and ZIP integrity-checked before inspection.

Inspected:
- `TRENDLINE_GEOMETRY_CONTRACT_V1.json`
- `TRENDLINE_GEOMETRY_V1_OUTPUT/TRENDLINE_GEOMETRY_BUILD_CONTRACT_V1.json`
- `TRENDLINE_GEOMETRY_V1_OUTPUT/TRENDLINE_GEOMETRY_MANIFEST_V1.csv`
- `TRENDLINE_GEOMETRY_V1_OUTPUT/TRENDLINE_GEOMETRY_QA_V1.csv`
- `TRENDLINE_GEOMETRY_V1_OUTPUT/GBPUSD_D1_STRUCTURE_TRENDLINES_V1.csv`

## Actual Geometry V1 contract
The canonical Geometry contract defines derived outputs:
- `line_id`
- `line_type` HIGH/LOW
- point 1 timestamp/price
- point 2 timestamp/price
- `slope_price_per_time`
- `direction` UP/DOWN/FLAT from exact slope sign
- `availability_timestamp`

It explicitly states:
- candidate line requires two same-type pivots;
- no tolerance/minimum-touch-count/angle/breakout threshold may be introduced unless an existing source/project contract defines it;
- slope is descriptive geometry, not a trading signal;
- breakout detection is excluded from Geometry V1;
- line availability is the later confirmation timestamp of the two defining pivots;
- no 2025 tuning/threshold selection.

## Actual D1 output schema
`GBPUSD_D1_STRUCTURE_TRENDLINES_V1.csv` columns are:
`line_id,line_type,point_1_timestamp,point_1_price,point_2_timestamp,point_2_price,slope_price_per_second,direction,availability_timestamp,point_1_availability,point_2_availability,source_file`

The actual rows confirm the Geometry producer emits anchors, family, direction, slope, and availability.

## QA status
Geometry QA shows `slope_ok=True`, `availability_ok=True`, `chronology_ok=True`, `type_ok=True`, and `no_2025=True` across the listed outputs, including D1.

## Comparison to Murphy Confirmation Layer
The existing Murphy Confirmation Layer / evaluator contract expects upstream evidence for:
- `third_touch`
- `reaction_bounce`
- `no_break`
- `confirmation_available_timestamp`

Geometry V1 does NOT emit those fields.

Specifically:
- `third_touch`: NOT emitted.
- `reaction_bounce`: NOT emitted.
- `no_break`: NOT emitted; breakout detection is explicitly excluded from Geometry V1.
- confirmation availability: Geometry emits only the line availability timestamp, not a successful third-test confirmation timestamp.

## Critical finding
The previous statement that the blocker was merely 'unverified Geometry schema' is now resolved.

We have now verified the actual schema.

The result is:

**GEOMETRY V1 COMPATIBILITY: PASS for its defined scope.**
**MURPHY CONFIRMATION UPSTREAM FACTS: NOT PROVIDED BY GEOMETRY V1.**

Therefore the missing layer is genuinely above Geometry, exactly as the Confirmation Layer architecture specifies.

## What this does NOT authorize
This verification does NOT authorize inventing:
- touch tolerance
- pip/percentage threshold
- ATR threshold
- reaction magnitude/duration threshold
- lookback
- automatic 3%/2-day binding

It also does not authorize modifying Geometry V1.

## Next action
Use the existing Geometry output + existing Pivot V2 + completed D1 price data to evaluate whether the source-backed Murphy semantics can be operationalized in the separate Confirmation Layer without introducing unsupported parameters.

If a deterministic source-safe predicate cannot be derived, the affected confirmation fields remain `NOT_EVALUABLE`.

2025 remains OOS and is not used for operator selection or tuning.