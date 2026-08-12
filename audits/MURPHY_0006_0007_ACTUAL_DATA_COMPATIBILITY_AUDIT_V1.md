# Murphy 0006–0007 Actual Data Compatibility Audit V1

Date: 2026-08-12
Status: GEOMETRY/PIVOT INPUTS COMPATIBLE; RAW BAR EVIDENCE NOT PRESENT IN FULL PROJECT ZIP

## Direct inspection

Inspected `/mnt/data/GBPUSD_RULE_EVALUATOR_V2_FULL.zip` directly.

Verified actual V2 artifacts:
- `PIVOT_SEQUENCE_V2_OUTPUT/GBPUSD_D1_STRUCTURE_PIVOT_SEQUENCE_V2.csv`
- `TRENDLINE_GEOMETRY_V1_OUTPUT/GBPUSD_D1_STRUCTURE_TRENDLINES_V1.csv`
- corresponding H1/H4/M15/M5 trendline outputs exist.

## Actual fields

PIVOT_SEQUENCE_V2 D1 contains:
- pivot_timestamp
- pivot_type
- pivot_price
- availability_timestamp
- source_row
- availability_row
- confirmation_status
- source_file
- sequence_index

TRENDLINE_GEOMETRY_V1 D1 contains:
- line_id
- line_type
- point_1_timestamp / price
- point_2_timestamp / price
- slope_price_per_second
- direction
- availability_timestamp
- point_1_availability
- point_2_availability
- source_file

## Direct finding

The trendline geometry output does NOT contain third-touch, reaction, no-break, or confirmation-event fields.

The Full Project ZIP also does not contain the underlying `D1/GBPUSD_D1_STRUCTURE.csv` raw OHLC file referenced by the pivot outputs. Therefore the current accessible archive cannot directly evaluate the Murphy Chapter 4 requirement that the trendline enclose the complete daily High-to-Low range after line availability.

## Collinearity diagnostic (not an operator)

Using the available V2 pivot data, three successive same-type pivots were checked for exact geometric collinearity with the line through the first two.

Results:
- D1: 804 triples, 0 exact collinear within 1e-10 price units.
- H4: 4507 triples, 0 exact collinear within 1e-10.
- H1: 17785 triples, 2 exact collinear within 1e-10.

This is diagnostic evidence only. It MUST NOT be used as a touch definition. Exact equality is not a source-approved successful-touch operator.

## Consequence

The existing Geometry/Pivot data can provide the line, anchors, direction, and availability chronology. It cannot by itself provide a source-safe deterministic third-touch/reaction/no-break event.

The raw OHLC data (especially D1 for the Chapter 4 daily-range rule) or an existing approved event producer is required before implementing production touch/reaction detection.

## No invention

Do not add:
- ATR tolerance
- percentage touch tolerance
- pip tolerance
- fixed lookback
- fixed timeframe
- 3%/2-day automatic 0006/0007 binding
- exact-collinearity as touch

2025 remains OOS and was not used.
