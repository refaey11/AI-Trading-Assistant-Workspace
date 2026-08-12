# Murphy 0006/0007 — Corrected Candidate Dataset V4 Manifest

Date: 2026-08-13
Status: CANONICAL CANDIDATE-ONLY / HISTORICAL QA INPUT

## Dataset
`MURPHY_0006_0007_REAL_DATA_CANDIDATE_EVIDENCE_2016_2024_V4.csv`

## Population
- MURPHY_0006: 166 rows
- MURPHY_0007: 181 rows
- Total: 347 rows

## Date boundary
- Earliest candidate timestamp: 2016-02-08
- Latest candidate timestamp: 2024-12-30
- Hard historical window: 2016-01-01 through 2024-12-31 inclusive
- 2025/2026 candidates: 0

## Provenance
Canonical input lineage:
- PIVOT_SEQUENCE_V2
- TRENDLINE_GEOMETRY_V1
- D1 OHLC / DMI-ADX source used by the workspace run

SHA-256:
`7739a55aba0a61b26ac25849135d147f153a637a55db08801701b41134e85303`

## QA status
- Candidate chronology: verified
- Candidate population counts: verified
- 2025/2026 leakage: absent
- Evidence status: CANDIDATE_ONLY
- No production PASS/FAIL inferred
- No threshold/touch tolerance/reaction magnitude/lookback introduced

## Historical QA rule
This V4 artifact supersedes the stale V2 artifact for historical QA purposes. The V2 artifact remains rejected because it contains post-2024 rows despite its filename.
