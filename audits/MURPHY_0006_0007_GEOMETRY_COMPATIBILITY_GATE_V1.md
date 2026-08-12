# Murphy 0006-0007 Geometry Compatibility Gate V1

Date: 2026-08-12

## Verified existing artifacts

The Workspace contains an existing Trendline Geometry V1 implementation and generated trendline outputs. The Workspace audit lists:
- `GBPUSD_RULE_EVALUATOR_V2/TRENDLINE_GEOMETRY_V1_OUTPUT/TRENDLINE_GEOMETRY_QA_V1.csv`
- `GBPUSD_RULE_EVALUATOR_V2/TRENDLINE_GEOMETRY_V1_OUTPUT/TRENDLINE_GEOMETRY_BUILD_CONTRACT_V1.json`
- `GBPUSD_RULE_EVALUATOR_V2/TRENDLINE_GEOMETRY_V1_OUTPUT/TRENDLINE_GEOMETRY_MANIFEST_V1.csv`
- multiple `*_STRUCTURE_TRENDLINES_V1.csv` outputs across M5/M15/M30/H1/H4/D1 and years 2016-2026.

## Source-locked compatibility target

MURPHY_0006:
- line family: reaction LOWs
- line direction: UP
- decision direction: BULLISH

MURPHY_0007:
- line family: reaction HIGHs
- line direction: DOWN
- decision direction: BEARISH

The John Murphy Chapter 4 source and recovered Master Rule Database rows establish two anchors for a tentative line and a third successful touch/reaction without a break for confirmation.

## Evaluator contract now implemented

The PR branch evaluator now consumes upstream geometry facts only and enforces:
- authoritative rule-ID binding: 0006 -> UP/BULLISH; 0007 -> DOWN/BEARISH;
- at least two anchors;
- third touch;
- successful reaction/bounce;
- no-break evidence;
- confirmation availability timestamp.

It does not invent a touch tolerance, ATR threshold, percentage threshold, or lookback. Missing required evidence returns `NOT_EVALUABLE`.

Unit tests cover both positive directions, missing reaction, break-after-touch, ID/direction mismatch, missing evidence, and insufficient anchors.

## Geometry gate finding

The existing Geometry V1 artifact family is verified to exist, but the currently retrievable Workspace/File Library representation still does not expose the exact row-level schema/contract fields proving that Geometry V1 itself emits explicit `third_touch`, `successful_reaction`, `no_break`, and confirmation availability fields.

Therefore the **upstream Geometry compatibility gate remains OPEN** even though the evaluator-side contract is source-correct and CI passes.

Current status:

**SOURCE-LOCKED SEMANTICS / EVALUATOR CONTRACT READY / GEOMETRY OUTPUT SCHEMA UNPROVEN**

## CI

The Murphy 0006-0007 Source Contract workflow completed successfully for commit `328ce00dfed6a6242f7415d57cd088fd512f9e0d` (run 15).

## Required closure evidence

To move the Geometry gate to PASS, retrieve the exact Geometry V1 contract/output schema and verify that its emitted evidence can represent:
1. two valid anchors;
2. trendline direction/family;
3. third touch;
4. successful reaction/bounce;
5. no break;
6. availability timestamp with no lookahead.

If the existing Geometry output does not contain these semantics, keep the affected operator `NOT_EVALUABLE` and do not create a replacement Geometry component.

## Controls

- Do not rebuild Trendline Geometry V1.
- Do not add ATR/percentage/price-distance tolerance.
- Do not infer successful reaction from generic price movement unless the existing Geometry contract explicitly defines it.
- Do not use 2025 for tuning or implementation selection.
- Do not modify Murphy 0003/0004.
