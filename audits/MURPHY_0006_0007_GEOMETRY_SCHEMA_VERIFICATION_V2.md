# Murphy 0006–0007 — Trendline Geometry Schema Verification V2
Date: 2026-08-12

## Scope
Compatibility verification of the existing `TRENDLINE_GEOMETRY_V1` against the source-locked Murphy 0006/0007 evaluator contract.

## Workspace evidence confirmed
The Workspace inventory confirms the existing geometry module and artifacts:
- `GBPUSD_RULE_EVALUATOR_V2/TRENDLINE_GEOMETRY_V1_OUTPUT/TRENDLINE_GEOMETRY_QA_V1.csv`
- `GBPUSD_RULE_EVALUATOR_V2/TRENDLINE_GEOMETRY_V1_OUTPUT/TRENDLINE_GEOMETRY_BUILD_CONTRACT_V1.json`
- `GBPUSD_RULE_EVALUATOR_V2/TRENDLINE_GEOMETRY_V1_OUTPUT/TRENDLINE_GEOMETRY_MANIFEST_V1.csv`
- timeframe-specific `*_STRUCTURE_TRENDLINES_V1.csv` outputs.

The Workspace also confirms the existing Pivot Sequence lineage: confirmed pivots, two confirming bars, availability at pivot timestamp + 2 bars, and no-lookahead before availability.

## What the current searchable Workspace content proves
It proves the Geometry V1 component exists and produces trendline outputs across multiple timeframes/years. It does NOT expose the row-level schema/content of the Geometry V1 contract sufficiently to prove that the generated outputs explicitly contain all of:
1. two valid anchors;
2. LOW/HIGH anchor family;
3. UP/DOWN trendline type;
4. third-touch identity;
5. successful reaction/bounce;
6. no-break-at-confirmation;
7. confirmation availability timestamp.

## GitHub evaluator compatibility
The existing 0006/0007 source-contract evaluator consumes exactly these upstream facts and deliberately does not invent tolerances, ATR thresholds, percentages, or lookbacks.

## Gate result
**OPERATIONAL EVIDENCE STILL UNPROVEN**

Do not mark 0006/0007 Production Frozen and do not run historical QA as if the source-defined operator were fully executable until the actual Geometry V1 schema is independently inspected.

## Required next step
Retrieve/open the actual `TRENDLINE_GEOMETRY_BUILD_CONTRACT_V1.json` and representative `*_STRUCTURE_TRENDLINES_V1.csv` files from the Workspace transfer (not merely the inventory audit). Inspect their exact columns/fields and map them one-to-one to the evaluator inputs.

If all required fields exist, bind the evaluator to them and run tests + 2016–2024 historical QA. If any field is absent, retain the corresponding portion as `NOT_EVALUABLE` and do not invent a replacement.

## Controls
- Existing Trendline Geometry V1 must not be rebuilt.
- 2025 remains OOS and untouched.
- No thresholds/tolerances/lookbacks/proxies were invented.
