# Murphy 0021–0023 Freeze Candidate Gate V1

Date: 2026-08-12

## Evidence reviewed

Existing artifact `MURPHY_EVALUATORS_V1` contains:
- `murphy_0021_0023_evaluator.py`
- `MURPHY_0021_0023_EVALUATOR_CONTRACT_V1.json`
- `MURPHY_0021_0023_UNIT_TESTS_V1.csv`
- `MURPHY_0021_0023_HISTORICAL_EVALUATION_2020_2024.csv`
- `MURPHY_0021_0023_HISTORICAL_SUMMARY_V1.csv`

## Evaluator contract

- 0021: price direction is completed close vs previous completed close; volume uses existing `volume_direction`; bullish/bearish confirmation requires volume UP.
- 0022: price UP + volume UP + CFTC British Pound futures OI UP.
- 0023: price DOWN + volume UP + CFTC British Pound futures OI UP.
- No thresholds were added.
- No spot-FX OI proxy is used.
- OI scope is CME British Pound futures 096742.
- Runtime/Dynamic MTF is used; no hard-coded execution timeframe.
- `2025_used=false`.

## Unit tests

All eight recorded tests pass:
- 0021 bullish
- 0021 bearish
- 0021 no confirmation
- 0022 pass
- 0022 wrong OI fail
- 0023 pass
- 0023 wrong price fail
- 0022 missing OI

## Historical QA

Historical evaluation covers 2020–2024. Summary contains D1, H1, and H4 results for all three rules.

D1:
- 0021: PASS 826, FAIL 727, NOT_EVALUABLE 2
- 0022: PASS 189, FAIL 1094, NOT_EVALUABLE 272
- 0023: PASS 192, FAIL 1091, NOT_EVALUABLE 272

H1:
- 0021: PASS 15011, FAIL 16216, NOT_EVALUABLE 159
- 0022: PASS 4006, FAIL 26920, NOT_EVALUABLE 460
- 0023: PASS 3987, FAIL 26939, NOT_EVALUABLE 460

H4:
- 0021: PASS 4764, FAIL 3258, NOT_EVALUABLE 18
- 0022: PASS 1314, FAIL 6413, NOT_EVALUABLE 313
- 0023: PASS 1222, FAIL 6505, NOT_EVALUABLE 313

## Gate decision

These three rules are promoted to **FREEZE CANDIDATE / QA PASS**, not Production FROZEN, because the available handoff explicitly requires exact source semantics, operator, TF role, gate logic, evaluator, tests, and historical evidence, and warns that evaluator existence alone does not establish semantic freeze.

No new operator, threshold, timeframe, or proxy is introduced by this gate.

## OOS control

2025 is untouched and remains OOS. No tuning or implementation selection is performed from OOS data.

## Next action

Add these candidates to the official Murphy freeze manifest only after source-rule semantic verification is attached to the manifest. Then continue 0024–0026 using existing Feature Engineering V2 and exact mapping artifacts; do not invent derived features.