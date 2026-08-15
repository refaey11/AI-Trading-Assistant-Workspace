# Murphy 0021–0023 — Provenance Reconciliation V1

Date: 2026-08-15
Status: PROVENANCE RECONCILED / FINAL FREEZE MANIFEST PENDING

## Canonical historical identity
The project records define the canonical clean historical artifact as:
`MURPHY_0021_0023_HISTORICAL_EVALUATION_2020_2024_CLEAN_V1.csv`

Expected canonical properties:
- 122,934 rows
- 2020–2024 only
- 2025 rows = 0

## Raw source examined
The accessible `MURPHY_EVALUATORS_V1(3).zip` contains:
`MURPHY_0021_0023_HISTORICAL_EVALUATION_2020_2024.csv`

Observed raw properties:
- 122,943 rows
- 122,934 rows dated 2020–2024
- 9 rows dated 2025-01-01

Those 9 rows are excluded from the clean historical population and are not used for tuning/selection. The raw file is not promoted as the canonical clean artifact.

## Reconciliation result
The 122,934-row 2020–2024 population from the accessible raw source matches the documented row count of the canonical clean artifact. The project therefore treats the documented CLEAN_V1 artifact identity as the canonical historical population, while retaining the raw ZIP as provenance evidence.

## Important limitation
This record does not claim that the raw ZIP itself is byte-identical to CLEAN_V1. Byte identity/SHA equality cannot be asserted without the canonical CSV payload. The reconciliation is row-count/period identity plus the existing project record of CLEAN_V1.

## Freeze implication
Historical provenance is considered reconciled at the artifact-identity level, subject to the explicit limitation above. Final Production Freeze still requires the final freeze manifest to reference the exact artifact identity and all passing technical gates.
