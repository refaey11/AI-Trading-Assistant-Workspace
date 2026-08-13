# Murphy 0006–0007 — Source-Safe Full Evidence Matrix V1
Date: 2026-08-13

## Objective
Compare the existing 2016–2024 candidate evidence against the Chapter 4 qualitative sequence without inventing a touch/reaction/no-break threshold.

## Source-backed sequence
Murphy Chapter 4 establishes the qualitative sequence:
1. two anchors establish a tentative trendline;
2. a third successful test/touch with reaction confirms the line;
3. the line must hold without a meaningful break;
4. Chapter 4 also states that the trendline must enclose the entire daily price range (High to Low).

## Existing V4 evidence
Source artifact: `MURPHY_0006_0007_REAL_DATA_CANDIDATE_EVIDENCE_2016_2024_V4.csv`
Population:
- total = 347
- 0006 = 166
- 0007 = 181

Existing combined candidate screen:
- daily_range_intersects_line = TRUE: 62 total
  - 0006 = 32
  - 0007 = 30
- reaction_directionally_consistent = TRUE: 340 total
- reaction_directionally_consistent = FALSE: 6
- missing reaction direction: 1
- combined range intersection + directional reaction = 62

## Matrix result
The 62 combined cases are the strongest source-safe candidate set currently exposed by V4 for a third-test/reaction event. They are NOT confirmations.

Why they cannot be promoted:
- `daily_range_intersects_line` is candidate/intersection evidence; it does not itself prove Murphy's "successful touch" predicate.
- `reaction_directionally_consistent` is directional reaction evidence; it does not define a source-approved reaction magnitude or duration.
- `no_break_observation` is recorded as `OBSERVATION_ONLY`, not as a deterministic `no_break_valid=true` production fact. Therefore the matrix cannot truthfully mark line-hold/no-break as confirmed.
- `evidence_status` remains `CANDIDATE_ONLY`.

## Important examples
V4 contains real cases with range intersection + directional reaction, e.g. 0006 rows around 2023-04-17 and 2023-04-19, and 0007 rows such as 2019-06-12. These demonstrate that the candidate event is observable in the existing data layer, but they do not establish a production operator.

## Decision
No production PASS/FAIL is authorized from this matrix.
The correct production state remains `NOT_EVALUABLE` until an authoritative operational contract defines:
- successful third-touch predicate;
- successful reaction predicate (including any required magnitude/duration, if any);
- 0006/0007-specific no-break/line-hold predicate;
- final confirmation availability timestamp semantics.

## Controls
- No ATR threshold.
- No pip/percentage touch tolerance.
- No invented lookback/timeframe.
- No automatic 3%/2-day binding.
- No 2025 tuning/selection.
- Existing Pivot V2, Geometry V1, Evidence Adapter, and Evaluator architecture are reused; none are rebuilt.

## Conclusion
The evidence matrix successfully isolates the 62 strongest candidate events, but it does NOT close the operational gate. The remaining blocker is now precisely the source-locked definition of "successful" touch/reaction and deterministic line-hold confirmation, not data availability or upstream architecture.