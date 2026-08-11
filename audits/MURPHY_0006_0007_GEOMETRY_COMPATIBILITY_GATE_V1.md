# Murphy 0006-0007 Geometry Compatibility Gate V1

Date: 2026-08-12

## Verified existing artifacts

The Workspace contains an existing Trendline Geometry V1 implementation and generated trendline outputs. The recent Workspace audit lists:
- `GBPUSD_RULE_EVALUATOR_V2/TRENDLINE_GEOMETRY_V1_OUTPUT/TRENDLINE_GEOMETRY_QA_V1.csv`
- `GBPUSD_RULE_EVALUATOR_V2/TRENDLINE_GEOMETRY_V1_OUTPUT/TRENDLINE_GEOMETRY_BUILD_CONTRACT_V1.json`
- `GBPUSD_RULE_EVALUATOR_V2/TRENDLINE_GEOMETRY_V1_OUTPUT/TRENDLINE_GEOMETRY_MANIFEST_V1.csv`
- multiple `*_STRUCTURE_TRENDLINES_V1.csv` outputs across M5/M15/M30/H1/H4/D1 and years 2016-2026.

## Compatibility target

MURPHY_0006:
- line family: reaction LOWs
- line direction: UP
- decision direction: BULLISH

MURPHY_0007:
- line family: reaction HIGHs
- line direction: DOWN
- decision direction: BEARISH

The Murphy source semantics require two anchor points for a tentative line and a third successful touch/reaction, without breaking the line, for confirmation.

## Gate finding

The searchable Workspace/File Library evidence proves the Geometry V1 artifact family exists, but the currently retrievable contract/manifest snippets do not expose fields proving that Geometry V1 itself emits explicit `third_touch`, `successful_reaction`, or `no_break` evidence.

Therefore this gate cannot honestly be marked PASS yet. The correct status is:

**MAPPING_COMPATIBLE / OPERATIONAL_EVIDENCE_UNPROVEN**

## Rules

- Do not rebuild Trendline Geometry V1.
- Do not add ATR/percentage/price-distance tolerance.
- Do not infer successful reaction from generic price movement unless the existing Geometry contract explicitly defines it.
- Do not use 2025 for tuning or implementation selection.
- Do not modify Murphy 0003/0004.

## Required closure evidence

To move the gate to PASS, retrieve the exact Geometry V1 contract/output schema and verify that its emitted evidence can represent:
1. two valid anchors;
2. trendline direction/family;
3. third touch;
4. successful reaction/bounce;
5. no break;
6. availability timestamp with no lookahead.

If those fields are absent, keep the third-touch operator `NOT_EVALUABLE` and continue with the next Murphy rule group rather than inventing a new Geometry component.
