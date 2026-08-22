# Murphy 0006/0007 Runtime Gate Update — 2026-08-22

## Source reviewed
`MURPHY_0006_0007_REAL_DATA_CANDIDATE_EVIDENCE_2016_2024_V4(3).csv`

## Evidence results
- Total rows: 347
- MURPHY_0006: 166 rows
- MURPHY_0007: 181 rows
- Historical window: 2016–2024
- Availability violations (`line_availability_timestamp > candidate_timestamp`): 0
- Candidate before anchor_2 violations: 0
- Reaction candidate before candidate timestamp: 0
- 2025 rows: 0
- `evidence_status`: CANDIDATE_ONLY for all 347 rows
- `no_break_observation`: OBSERVATION_ONLY for all 347 rows

## Runtime gate decision
Status remains **PARTIAL / NOT_RUNTIME_VERIFIED**.

The V4 evidence strengthens availability/no-lookahead provenance and is usable as evidence input, but it does not by itself establish an executable runtime PASS because the rows are explicitly marked CANDIDATE_ONLY and OBSERVATION_ONLY. The existing project audit also requires readable evaluator payloads and verified runtime behavior before promoting a frozen rule to Runtime PASS.

## Existing runtime assets
- Dedicated deterministic CI workflow exists for 0006/0007.
- The workflow invokes `tests/test_murphy_0006_0007_evidence_adapter.py`.
- The workspace audit still records evaluator payload recovery/verification as the prerequisite for a full batch runtime PASS.

## Next gate
Recover/verify the readable 0006/0007 evaluator + evidence adapter source, then run the deterministic test and full runtime entry-point test against the V4 evidence without changing rule semantics or introducing thresholds. 2025 remains OOS.
