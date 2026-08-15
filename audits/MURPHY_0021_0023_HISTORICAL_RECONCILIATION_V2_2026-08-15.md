# Murphy 0021–0023 — Historical Reconciliation V2

Date: 2026-08-15

## Execution performed
The existing workspace bridge `ADAPTER_BRIDGE_0021_0023/evaluator_to_evidence_bridge.py` was executed against the existing historical artifact:
`MURPHY_EVALUATORS_V1/MURPHY_0021_0023_HISTORICAL_EVALUATION_2020_2024.csv`.

Deterministic bridge unit tests: 5/5 PASS.
Full historical rows checked: 122,943.
Lossless bridge failures: 0.

## Critical finding
The artifact filename and evaluator contract state `2020_2024` / `2025_used=false`, but the CSV contains 9 rows dated `2025-01-01`.

Therefore:
- 122,934 rows are genuinely dated 2020–2024.
- 9 rows are dated 2025-01-01.
- The 9 rows are one row for each rule/timeframe combination: D1/H1/H4 × 0021/0022/0023.
- The 2025 contamination/spill is real and must not be silently removed from the canonical artifact.

## Freeze decision
PRODUCTION FREEZE: NOT GRANTED.

The bridge itself passes the available rows, but the historical/provenance gate is blocked because the artifact's claimed OOS boundary conflicts with its actual contents.

## Required resolution
1. Recover or inspect the artifact generator/manifest/lineage that produced the CSV.
2. Determine why 2025-01-01 rows were appended to a file labeled 2020_2024.
3. Re-run or regenerate the authoritative historical artifact from the verified source range, preserving the original evaluator semantics.
4. Re-run bridge reconciliation on the corrected authoritative artifact.
5. Run availability/no-lookahead checks.
6. Only then perform final freeze review.

## Governance
- Do not tune or change 0021–0023 to alter historical counts.
- Do not use the 9 rows for tuning or selection.
- 2025 remains OOS.
- A derived 122,934-row clean copy may be used for diagnosis only; it is NOT the canonical replacement until provenance is reconciled.
