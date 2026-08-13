# Murphy 0006/0007 Event Operator V1 — Reconstruction QA

Date: 2026-08-13
Period: 2016-01-01 through 2024-12-31
2025: excluded

## Purpose

Run the proposed event-based confirmation chain against the actual reconstructed GBPUSD D1 workspace artifacts before any production promotion.

## Inputs reconstructed from the multipart workspace archive

- PIVOT_SEQUENCE_V2_OUTPUT/GBPUSD_D1_STRUCTURE_PIVOT_SEQUENCE_V2.csv
- TRENDLINE_GEOMETRY_V1_OUTPUT/GBPUSD_D1_STRUCTURE_TRENDLINES_V1.csv
- DMI_ADX_V1_OUTPUT/GBPUSD_D1_DMI_ADX_2016_2024.csv (used for D1 OHLC fields only)

The reconstructed pivot population contains 808 rows, Geometry contains 806 lines, and D1 OHLC contains 2,544 rows.

## Population reproduction

The event reconstruction reproduces the known candidate population exactly:

- total = 347
- MURPHY_0006 = 166
- MURPHY_0007 = 181

This matches the existing project candidate-run population.

## Important reproducibility discrepancy

The independently reconstructed event scan produced:

- D1 range/line intersections: 58 for 0006, 55 for 0007 (113 total)
- directional reaction candidates: 140 for 0006, 165 for 0007

The existing V4 candidate artifact / project handoff reports 32 intersections for 0006 and 30 for 0007 (62 total), with 340 directionally consistent reactions.

Therefore the candidate population is reproduced, but the existing V4 screening counts are NOT reproduced by the current independent reconstruction. This is a provenance/reproducibility discrepancy and MUST be resolved before using the new operator for production evaluation.

## Proposed operator test

Using the event-chain proposal with:

- first confirmed same-family pivot after line availability as touch candidate;
- D1 range intersection as touch evidence;
- next confirmed opposite-family pivot as reaction candidate;
- reaction away from the touch price;
- post-touch D1 line-hold using the complete D1 OHLC artifact;
- reaction pivot availability as confirmation availability;

resulted in 25 provisional confirmations:

- 0006 = 14
- 0007 = 11

These are NOT production PASS results.

## Interpretation

The experiment proves that the proposed event chain is executable against the reconstructed workspace data without adding ATR, pip, percentage, fixed lookback, or 3%/2-day thresholds.

It does NOT yet prove that the operator is the exact project-approved interpretation, because:

1. the independent reconstruction does not reproduce the existing V4 intersection screen;
2. "next opposite-family confirmed pivot" is an operational representation, not a verbatim Murphy operator;
3. the project still requires compatibility approval before converting the proposal into production PASS/FAIL.

## Safety controls

- 2025 not used.
- No OOS tuning.
- No 3% binding.
- No 2-day binding.
- No ATR/pip/percentage tolerance.
- No modification of Pivot V2 or Geometry V1.
- Confirmation availability is tied to confirmed reaction availability, not future data.

## Gate

STATUS = OPERATIONAL PROTOTYPE / QA BLOCKED BY REPRODUCIBILITY RECONCILIATION

Next action:
Reconcile the exact V4 candidate-generation predicate against the reconstructed Pivot/Geometry/D1 artifacts. Only after that reconciliation should the event operator be rerun and compared with the project's 62 strong candidates and subsequent no-break evidence.
