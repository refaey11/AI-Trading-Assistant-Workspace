# Murphy 0006–0007 Source-Safe Candidate Event Classification V1
Date: 2026-08-13
Status: CANDIDATE-ONLY / NOT PRODUCTION

## Purpose
Implement the smallest event classification that can be supported by the existing Chapter 4 semantics and the existing V4 candidate evidence, without introducing any new numeric touch/reaction threshold.

## Source basis
Chapter 4 establishes the qualitative sequence for trendlines: two anchors establish the line; a third successful test/touch followed by reaction confirms the trendline; the line must remain valid/hold. Chapter 4 also states that trendlines must enclose the entire daily price range (High to Low), and discusses general breakout filters. General 3%/2-day examples are not bound automatically to 0006/0007.

## Existing inputs reused
- PIVOT_SEQUENCE_V2
- TRENDLINE_GEOMETRY_V1
- MURPHY_0006_0007_REAL_DATA_CANDIDATE_EVIDENCE_2016_2024_V4.csv

No upstream component was modified.

## Candidate event predicates
These are explicitly CANDIDATE predicates, not production confirmation predicates.

### Third-test candidate
`third_test_candidate = daily_range_intersects_line == TRUE`

Rationale: this is the existing project evidence field that records the D1 range reaching/intersecting the mathematical line. It is NOT asserted to mean "successful touch". No distance/tolerance is added.

### Reaction candidate
`reaction_candidate = third_test_candidate AND reaction_directionally_consistent == TRUE`

Rationale: reuse the existing candidate reaction evidence. No reaction magnitude or duration is invented.

### Line-hold candidate
The existing `no_break_observation` field is retained as observation-only. It is NOT promoted to `no_break_valid` because the current V4 evidence does not expose a source-locked production no-break predicate.

### Production status
Any event lacking an approved deterministic touch/reaction/no-break operator remains `NOT_EVALUABLE` at the production evaluator.

## 2016–2024 result from existing V4 candidate run
Population: 347
- 0006: 166
- 0007: 181

Existing candidate evidence:
- D1 range intersects line: 62 total (0006=32, 0007=30)
- reaction directionally consistent: 340 total (0006=163, 0007=177)
- combined range-intersection + directional reaction: 62 total (0006=32, 0007=30)

Therefore the source-safe candidate classifier produces:

| Rule | Population | Third-test candidate | Reaction candidate | Production confirmation |
|---|---:|---:|---:|---|
| 0006 | 166 | 32 | 32 | NOT_EVALUABLE |
| 0007 | 181 | 30 | 30 | NOT_EVALUABLE |
| Total | 347 | 62 | 62 | NOT_EVALUABLE |

## Important distinction
The 62 combined candidates are NOT PASS. The classification intentionally stops before successful-touch confirmation and production no-break validation.

The earlier exact-touch diagnostic found zero exact mathematical collinear touches. Exact equality is therefore not used as a touch definition.

The earlier 2-day experiment remains exploratory only and is not used here.

## No invented semantics
This artifact does not introduce:
- ATR threshold
- pip tolerance
- percentage tolerance
- reaction magnitude threshold
- reaction duration threshold
- fixed lookback
- fixed timeframe
- automatic 3% binding
- automatic 2-day binding
- 2025 tuning/selection

## Gate result
### CLOSED/usable as candidate evidence
- third-test candidate event from existing D1 range intersection field
- directional reaction candidate from existing reaction evidence

### STILL OPEN for production
- deterministic successful-touch predicate
- deterministic reaction predicate
- deterministic 0006/0007 no-break predicate
- confirmation timestamp semantics
- production evaluator
- 2016–2024 Historical QA
- freeze

## Decision
This is the smallest source-safe event layer that can be derived from the current evidence without inventing semantics. It should feed the existing Confirmation Layer as candidate evidence only. Production evaluator must return NOT_EVALUABLE until the missing operator contract is source-locked.
