# Murphy 0006–0007 2-Day Candidate Test V1

Date: 2026-08-13
Input: `MURPHY_0006_0007_REAL_DATA_CANDIDATE_EVIDENCE_2016_2024_V4.csv`
Rows: 347
Scope: 2016–2024 only

## Population
- MURPHY_0006: 166 candidates
- MURPHY_0007: 181 candidates
- Total: 347
- evidence_status: 347/347 `CANDIDATE_ONLY`

## Existing evidence results
- daily_range_intersects_line = TRUE: 62 / 347
  - 0006: 32
  - 0007: 30
- reaction_directionally_consistent = TRUE: 340 / 347
- reaction_directionally_consistent = FALSE: 6 / 347
- reaction_directionally_consistent missing: 1 / 347
- rows satisfying existing touch/range AND directional-reaction evidence: 62 / 347
  - 0006: 32
  - 0007: 30

## No-break limitation
The uploaded candidate CSV contains `no_break_observation`, but every row is `OBSERVATION_ONLY`. It does not contain the daily close series required to independently evaluate the proposed `2 consecutive daily closes beyond the trendline` rule.

Therefore this file alone cannot truthfully produce final PASS/FAIL for the 2-day no-break policy.

## Important result
The candidate population confirms that the existing upstream evidence can narrow the 347 candidates to 62 rows satisfying the currently recorded line/range interaction plus directional reaction evidence. However, this is NOT confirmation because the source-backed 2-day no-break predicate cannot be recomputed from this CSV alone.

## Required next input
To complete the deterministic test, provide the corresponding GBPUSD D1 OHLC/close data covering the candidate periods (2016–2024), or an existing project artifact containing those completed daily closes. No external market-data substitution should be used without a provenance/compatibility audit.

## Freeze status
0006/0007 remain `NOT_YET_EVALUABLE` for production confirmation until the 2-day no-break predicate is actually evaluated on completed D1 closes.

2025 remains OOS and must not be used for tuning.
