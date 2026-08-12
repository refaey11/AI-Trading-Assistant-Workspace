# Murphy 0021–0023 Closure Audit V2

Date: 2026-08-12

## Evidence source

Workspace/File Library artifact:
`GBPUSD_RULE_EVALUATOR_V2_WORKSPACE_PART_02_OF_03.zip.part`

Located artifacts:
- `MURPHY_EVALUATORS_V1/MURPHY_0021_0023_EVALUATOR_CONTRACT_V1.json`
- `MURPHY_EVALUATORS_V1/murphy_0021_0023_evaluator.py`
- `MURPHY_EVALUATORS_V1/MURPHY_0021_0023_UNIT_TESTS_V1.csv`
- `MURPHY_EVALUATORS_V1/MURPHY_0021_0023_HISTORICAL_EVALUATION_2020_2024.csv`
- `MURPHY_EVALUATORS_V1/MURPHY_0021_0023_HISTORICAL_SUMMARY_V1.csv`

## Contract verification

The contract declares `IMPLEMENTED_AND_UNIT_TESTED` for rules 0021–0023.

Operationalization uses:
- completed current close vs previous completed close for price direction;
- existing project `volume_direction`;
- existing CFTC futures `oi_direction`;
- no added thresholds;
- no OI proxy;
- Runtime/Dynamic MTF rather than a hard-coded execution timeframe;
- CME British Pound futures 096742 for OI;
- `2025_used = false`.

## Unit-test artifact verification

All listed cases are marked `True` in the preserved test CSV:

0021:
- bullish: True
- bearish: True
- no confirmation: True

0022:
- pass: True
- wrong OI: True
- missing OI: True

0023:
- pass: True
- wrong price: True

## Important limitation

This audit verifies the preserved workspace test artifact and its recorded outcomes. It does **not** claim a fresh execution of the Python evaluator in this chat runtime, because the uploaded workspace is available as a split archive/reference rather than as an executable mounted source tree.

Therefore:
- preserved unit-test artifact = VERIFIED PASS;
- fresh runtime execution = NOT PERFORMED;
- semantic freeze = NOT CLAIMED.

## Historical evidence

The contract confirms the 2020–2024 historical evaluation and summary artifacts exist. The current retrieved excerpts do not expose the complete row-level historical metrics, so no performance metric is promoted or invented here.

## Decision

**0021–0023 = ARTIFACT-VERIFIED TEST PASS / SEMANTIC FREEZE PENDING**

Next action is not to rebuild these evaluators. It is to retrieve/execute the existing evaluator in an executable workspace and perform the remaining historical/semantic QA, then integrate through the existing Rule Adapter.

2025 remains OOS and untouched.
