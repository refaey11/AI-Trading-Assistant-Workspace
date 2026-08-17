# Murphy 0005 — Source-Bound Evaluator Contract V1

Status: IMPLEMENTATION-READY / NOT FROZEN

## Source lock
Rule: MURPHY_0005
Name: Sideways regime filter
Chapter: 4 — Trend Definition
Required condition: Peaks and troughs move horizontally within a relatively tight price band.
Direction: NO_TRADE
Decision logic: Trend-following approaches are vulnerable in sideways markets; treat regime as non-trending until evidence changes.

## Contract boundary
This artifact translates the source into a gate contract only. It does not invent a numeric definition for "relatively tight price band", lookback, tolerance, or threshold.

## Evaluation
- If the existing PIVOT_SEQUENCE_V2 producer supplies source-compatible peak/trough structure AND an approved project operator explicitly establishes the sideways regime: PASS.
- If the operator establishes a non-sideways regime: FAIL for the sideways-regime condition.
- If required peak/trough evidence or the approved operator is unavailable: NOT_EVALUABLE.

## Safety
- No proxy metric is introduced.
- No new threshold/tolerance/lookback is introduced.
- No historical outcome is used to define semantics.
- 2025 remains OOS and cannot be used for tuning/selection/calibration.
- This rule is a regime/context gate and does not independently create a trade direction.

## Freeze gate
Production freeze still requires: existing-producer binding, deterministic tests, availability/no-lookahead verification, and historical QA on the approved OOS-safe evaluation window.
