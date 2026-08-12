# Murphy 0006/0007 — Real-Data Candidate QA V2

Status: QA-IN-PROGRESS / CANDIDATE-ONLY
Date: 2026-08-13

## Canonical inputs
- PIVOT_SEQUENCE_V2: 808 rows
- TRENDLINE_GEOMETRY_V1: 806 rows
- D1 OHLC: 2,544 bars
- Period evaluated: 2016–2024
- 2025: excluded from tuning/optimization

## Candidate population
- MURPHY_0006: 197 candidates
- MURPHY_0007: 206 candidates
- Total: 403 candidates

## Raw observations
- 0006 daily-range/line intersections: 32
- 0007 daily-range/line intersections: 30
- 0006 directionally-consistent reaction candidates: 193
- 0007 directionally-consistent reaction candidates: 203

## Interpretation
These are candidate/evidence observations only. They do NOT establish a successful third touch, successful reaction, no-break confirmation, or production rule PASS.

## Important provenance correction
A malformed/partial CSV previously existed at the candidate-evidence path. It was removed from the branch and replaced by a canonical rebuild process. The rebuilt local dataset contains 403 rows and was generated from the canonical pivot, geometry, and D1 OHLC files.

## QA gates still open
1. Verify candidate chronology and availability constraints.
2. Verify no lookahead through anchor/candidate/reaction availability ordering.
3. Verify 0006/0007 mapping remains LOW+UP / HIGH+DOWN.
4. Verify candidate rows are unique and deterministic.
5. Keep no-break as OBSERVATION_ONLY until a source-backed operator exists.
6. Do not promote candidate evidence to PASS/FAIL without an approved deterministic operator.

## Reproducibility
Local rebuilt dataset SHA-256:
`5169513a7cc48ad4204186ceb65a9b0032bb05e8b24a580ce43aea07271442e4`

## Next step
Run the QA checks above against the canonical rebuilt dataset, then record the QA result before any confirmation promotion.
