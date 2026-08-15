# MURPHY 0030 — P&F COMPATIBILITY GATE RESULT V1
Date: 2026-08-15
Status: COMPATIBILITY GATE OPEN — NOT FROZEN

## What was verified
1. The project mapping file `MURPHY_0026_TO_0030_EXACT_MAPPING_V3.csv` contains two source-verified conditions for MURPHY_0030:
   - X/O Point & Figure structure.
   - Bullish P&F support trendline as structural reference.
   Both are marked NOT_EVALUABLE because a verified P&F feature schema was not present in that earlier workspace snapshot.
2. The project's `TRENDLINE_GEOMETRY_CONTRACT_V1.json` explicitly says ordinary trendlines are not substitutes for a P&F feature and that no angle/threshold may be invented without an existing source/project contract.
3. The external candidate `gregorian-09/pnf-chart-system` is currently documented as supporting High/Low construction, X/O columns, configurable reversal, multiple box-size methods, and trend-line updates. Its current PyPI release is 0.2.0 and the package is MIT licensed.
4. The candidate documentation shows `ConstructionMethod.HighLow`, `BoxSizeMethod.Traditional`, and `reversal = 3` as supported configuration choices. These capabilities are evidence of compatibility potential, not proof of semantic equivalence.

## Gate decision
PASS for candidate discovery.
FAIL for production integration/freeze.

## Exact remaining blockers
- No approved GBPUSD box-size/scaling policy has been established from Murphy or a formally approved project operationalization.
- Candidate source code has not yet been executed in the project runtime; the local environment does not currently have `pypnf` installed and outbound package installation is unavailable.
- Therefore no claim is made yet about exact column-by-column equivalence or availability/no-lookahead behavior.

## Required next step
Obtain the candidate source as a local vendored/audit artifact or otherwise execute it in an environment with the package available, then run the synthetic HighLow/3-box harness and prefix-replay/no-lookahead tests defined in `MURPHY_0030_PNF_ENGINE_COMPATIBILITY_HARNESS_PLAN_V1.md`.

Do not tune box size, do not use 2025 for parameter selection, and do not map 0030 to S-7 without separate provenance.

## Rule state
MURPHY_0030 remains IN PROGRESS / COMPATIBILITY AUDIT. Do not advance to 0031.
