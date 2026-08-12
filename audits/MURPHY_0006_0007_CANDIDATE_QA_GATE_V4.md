# Murphy 0006/0007 — Candidate QA Gate V4

Date: 2026-08-13
Status: PASS — CANDIDATE QA ONLY

## Dataset under test
`MURPHY_0006_0007_REAL_DATA_CANDIDATE_EVIDENCE_2016_2024_V4.csv`

Canonical population:
- MURPHY_0006: 166
- MURPHY_0007: 181
- Total: 347

## Deterministic QA checks
- Schema: 23 expected columns
- Candidate period: 2016-01-01 through 2024-12-31 inclusive
- Reaction candidate period: same historical window
- Candidate availability >= candidate timestamp
- Reaction timestamp >= candidate timestamp when present
- 0006 mapping = LOW / UP
- 0007 mapping = HIGH / DOWN
- Unique `(rule_id, line_id, candidate_timestamp)` keys
- Evidence status is CANDIDATE_ONLY for every row
- No-break field remains observation-only
- Exact zero-distance contacts = 0

## Result
All candidate QA assertions pass for the V4 dataset.

This gate does NOT establish:
- successful third touch
- successful reaction
- no-break / line holds
- Murphy confirmation
- production PASS/FAIL

No thresholds, tolerances, lookbacks, or tuning parameters were introduced.
2025 remains excluded from tuning/optimization.

## Next gate
The next implementation gate is not another historical tuning pass. It is the source-locked deterministic operator contract for third touch, reaction away from line, and no-break. Until that contract exists, candidate evidence remains `CANDIDATE_ONLY` / production `NOT_YET_EVALUABLE`.
