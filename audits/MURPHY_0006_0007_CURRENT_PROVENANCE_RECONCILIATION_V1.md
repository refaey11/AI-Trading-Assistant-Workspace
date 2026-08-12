# Murphy 0006/0007 — Current Provenance Reconciliation V1

Date: 2026-08-13
Status: RECONCILED / PRODUCTION GATE REMAINS OPEN

## Scope
Reconcile the current Workspace/File Library state, prior handoff, GitHub source audit, and real-data candidate artifact before further implementation.

## Findings

### 1. Qualitative source semantics are already closed in the 2026-08-12 handoff
The project handoff records:
- 0006 = reaction LOW family -> UP trendline -> two anchors -> third test/touch -> successful reaction/rebound -> line holds without meaningful break -> BULLISH.
- 0007 = reaction HIGH family -> DOWN trendline -> two anchors -> third test/touch -> successful reaction/rebound -> line holds without meaningful break -> BEARISH.
The handoff also states that general Murphy 3% / 2-consecutive-day examples are not automatically bound to 0006/0007.

### 2. Original Rule Registry records remain unrecovered
The older source-semantics audit and current searchable project-state artifacts do not contain the authoritative original database rows for MURPHY_0006 / MURPHY_0007. GitHub repository search also did not return an original rule-record file establishing the distinction.

Therefore the qualitative handoff resolution is retained as WORKING/PROJECT RESOLUTION, but the authoritative Rule Registry source-lock is still not independently reproduced from the original row.

### 3. Existing Geometry V1 remains reusable
No Geometry rebuild is authorized. The existing PIVOT_SEQUENCE_V2 -> TRENDLINE_GEOMETRY_V1 lineage remains the upstream primitive.

### 4. Candidate CSV provenance conflict detected
The File Library artifact named `MURPHY_0006_0007_REAL_DATA_CANDIDATE_EVIDENCE_2016_2024_V2.csv` contains visible 2025 and 2026 candidate timestamps despite its filename claiming 2016–2024. Examples include 0007 candidates in April/May/June 2026 and 0006 candidates in January–March 2025.

Therefore that uploaded/library artifact MUST NOT be treated as the corrected 2016–2024 historical population. The later QA correction recorded on GitHub supersedes it for historical QA.

### 5. Corrected historical QA population remains the governed population
The GitHub QA correction records:
- 0006 = 166 candidates
- 0007 = 181 candidates
- total = 347
- in-window reaction candidates = 346
- 0 exact zero-distance contacts
- all candidates within 2016-01-01 through 2024-12-31
- evidence status = CANDIDATE_ONLY
- no thresholds/touch tolerances/reaction thresholds/no-break rules introduced.

## Gate decision

Do not use the stale File Library CSV for scoring, tuning, or confirmation.
Do not promote candidate evidence to PASS/FAIL.
Do not invent a touch tolerance, reaction threshold, lookback, or 3%/2-day binding.

Next action is NOT to rebuild the data layer. Instead, preserve the corrected 347-row population and continue the source-backed Confirmation Layer audit. The remaining production blocker is the exact deterministic touch/reaction/no-break operator contract and independent source-lock of the original rule records.
