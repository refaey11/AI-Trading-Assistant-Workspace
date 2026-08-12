# Murphy 0006–0007 — Direct Trendline Geometry Schema Verification Final Gate V1
Date: 2026-08-12

## Direct workspace extraction
The complete three-part `GBPUSD_RULE_EVALUATOR_V2` Workspace transfer was reconstructed locally from the uploaded split files and opened as a valid 241-entry ZIP.

The exact existing Trendline Geometry artifacts were inspected directly:
- `TRENDLINE_GEOMETRY_CONTRACT_V1.json`
- `TRENDLINE_GEOMETRY_V1_OUTPUT/TRENDLINE_GEOMETRY_BUILD_CONTRACT_V1.json`
- `TRENDLINE_GEOMETRY_V1_OUTPUT/TRENDLINE_GEOMETRY_MANIFEST_V1.csv`
- `TRENDLINE_GEOMETRY_V1_OUTPUT/TRENDLINE_GEOMETRY_QA_V1.csv`
- representative `*_STRUCTURE_TRENDLINES_V1.csv` output(s)

## Exact Geometry V1 schema
A representative trendline output contains exactly:
- `line_id`
- `line_type`
- `point_1_timestamp`
- `point_1_price`
- `point_2_timestamp`
- `point_2_price`
- `slope_price_per_second`
- `direction`
- `availability_timestamp`
- `point_1_availability`
- `point_2_availability`
- `source_file`

The Geometry contract declares derived outputs for the same two-point line geometry and explicitly defines availability as the later confirmation timestamp of the two defining pivots.

## Critical contract finding
`TRENDLINE_GEOMETRY_CONTRACT_V1.json` explicitly states:
- a candidate line requires two pivots of the same type;
- no tolerance, minimum-touch count, angle threshold, or breakout threshold may be introduced unless another existing project/source contract defines it;
- slope is descriptive geometry, not a trading signal;
- this module does not choose timeframe.

`TRENDLINE_GEOMETRY_V1_OUTPUT/TRENDLINE_GEOMETRY_BUILD_CONTRACT_V1.json` additionally states:
- line generation is consecutive pivots of the same type only;
- breakout detection is excluded;
- thresholds added = false;
- line availability = later confirmation timestamp of the two defining pivots;
- lookahead control = line cannot be available before both defining pivots are confirmed.

## Murphy 0006–0007 compatibility
The schema directly supports:
- two anchors: YES
- LOW/HIGH family: YES (`line_type`)
- UP/DOWN direction: YES (`direction`)
- availability/no-lookahead for the two-point line: YES

The schema does NOT directly support:
- third touch: NO
- successful reaction/bounce: NO
- no-break at third test: NO

No `third_touch`, `successful_reaction`, `reaction_bounce`, `no_break`, or equivalent explicit field exists in the inspected Geometry output schema.

## Source interpretation boundary
John Murphy Chapter 4 requires the third successful touch/reaction without breaking to confirm the trendline. Therefore the source semantics are source-locked, but the current Geometry V1 provider does not contain the operational evidence required to evaluate that confirmation event.

The Geometry contract's explicit prohibition on introducing a minimum-touch count/tolerance also prevents us from silently deriving a new confirmation operator inside the existing Geometry module.

## Final gate decision
**0006–0007 = SOURCE-LOCKED / GEOMETRY PARTIAL / THIRD-TOUCH OPERATOR BLOCKED**

This is a clean blocker, not a source ambiguity.

## What is authorized next
A separate Murphy-compatible derived evidence layer may be designed ONLY after a source-backed operational definition of successful touch/reaction/no-break is established without inventing a threshold. The existing Trendline Geometry V1 must remain unchanged.

Until such an approved contract exists:
- do not mark 0006/0007 FROZEN;
- do not run official historical QA for the third-touch confirmation rule;
- do not use 2025 for tuning/selection;
- do not change the existing Geometry engine.

## Existing PR #2 status
PR #2's generic evaluator can remain as a contract-level adapter, but it must not be treated as production-ready because its required third-touch/reaction/no-break inputs are not emitted by the existing Geometry V1 provider.
