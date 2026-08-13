# Murphy 0006–0007 2-Day Execution Result V1

Date: 2026-08-13
Scope: 2016–2024 only; 2025 excluded.

## Inputs actually found in workspace
- `MURPHY_0006_0007_REAL_DATA_CANDIDATE_EVIDENCE_2016_2024_V4.csv`: 347 rows.
- `GBPUSD_D1_DMI_ADX_2016_2024.csv`: 2,544 D1 rows with OHLC + close.

## Candidate population
- 0006: 166
- 0007: 181
- Total: 347
- Strong upstream evidence (daily range intersects line AND directional reaction): 62
  - 0006: 32
  - 0007: 30

## Executed no-break test
For each of the 62 strong candidates, the mathematical trendline was evaluated on the completed D1 closes from the candidate timestamp through the recorded reaction-candidate timestamp. A meaningful break was defined according to the project binding proposal as two consecutive D1 closes beyond the line in the break direction:
- UP line: close below line.
- DOWN line: close above line.

Result: 20 / 62 strong candidates had two consecutive D1 closes beyond the line before or at the recorded reaction candidate timestamp.
- 0006: 11 / 32
- 0007: 9 / 30

Therefore 42 / 62 passed this specific no-break screen:
- 0006: 21 / 32
- 0007: 21 / 30

## Critical interpretation
This is NOT a final Murphy PASS/FAIL result. It is an execution result for the proposed 2-day no-break operator applied to the existing candidate evidence.

The remaining production gaps are:
1. The project has not frozen the 2-day policy as original 0006/0007 source text; it remains an explicit operational binding.
2. `successful touch` and `reaction` are still operationalized through existing candidate evidence rather than a source-defined numeric magnitude/tolerance.
3. The test window used the recorded reaction-candidate timestamp as the upper bound. This must be explicitly accepted as the confirmation-event boundary before production freeze.

## Decision
The 2-day operator is technically executable with existing workspace data. It produces a concrete separation of the 62 strong candidates into 42 no-break survivors and 20 break failures. Do not label the 42 as final rule PASS until the remaining binding/confirmation semantics are frozen.

No tuning was performed and no 2025 data was used.
