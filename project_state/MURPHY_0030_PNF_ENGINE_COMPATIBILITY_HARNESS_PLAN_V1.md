# MURPHY 0030 — P&F ENGINE COMPATIBILITY HARNESS PLAN V1
Date: 2026-08-15
Status: PRE-EXECUTION / NO TUNING

## Objective
Compatibility-test the discovered external P&F implementation against Murphy Chapter 11 semantics and the project's availability/no-lookahead rules before any integration or evaluator work.

## Candidate
Candidate identified in prior audit: `pnf-chart-system` / Python package `pypnf`.
Documented capabilities include High-Low construction, configurable box size/scaling, reversal, X/O columns, trendlines, and a bullish support line output. This is a candidate only; it is not project-approved.

## Source constraints to test
1. Murphy 3-box / 3-point reversal construction.
2. High/Low construction path.
3. X/O columns.
4. 45-degree bullish support line.
5. Bullish structural context while price remains above the bullish support line.
6. Rule identity remains `MURPHY_0030 = P&F bullish support`.
7. Do not map 0030 to S-7 without separate provenance.

## Project constraints
- Do not rebuild an engine before compatibility testing the candidate.
- Do not choose box size by historical performance.
- Do not use 2025 for box-size/operator selection.
- Do not import ATR/pip/percentage conventions and label them as Murphy semantics.
- Any non-source construction parameter must be explicitly labeled project operationalization and frozen before evaluation.
- Missing/unsupported evidence must return NOT_EVALUABLE.
- Every emitted event must have an availability timestamp that cannot precede the information used to construct it.

## Harness tests
### A. Construction equivalence
- Verify X/O column direction and continuation logic.
- Verify 3-box reversal behavior on synthetic monotonic/reversal sequences.
- Verify High/Low method consumes only the appropriate high or low at each state transition.
- Verify deterministic output from identical input.

### B. Trendline semantics
- Verify bullish support line is a 45-degree structural line in the 3-box representation.
- Verify line origin/adjustment behavior against Murphy's Chapter 11 description.
- Verify state classification above/below the line does not invent a trading signal.

### C. Availability / no-lookahead
- Every column state must be reproducible using only completed input bars available at that timestamp.
- No future column, future reversal, or future trendline adjustment may alter a prior emitted event.
- Replaying a prefix of the data must produce the same historical prefix of P&F states.

### D. Box-size boundary
- Do not select a GBPUSD value from performance.
- Record the engine's supported scaling methods.
- Record which methods are directly compatible with Murphy's text.
- Leave the policy unresolved until an authoritative source or explicit project operationalization is approved.

### E. Determinism
- Same data + same frozen configuration => identical columns, trendline state, event timestamps, and availability timestamps.

## Acceptance gate
The candidate may proceed to adapter design only if A, B, C, and E pass and D has an explicitly governed configuration boundary.

## Current conclusion
The external candidate is promising because it exposes the exact structural primitives needed by 0030, but capability is not equivalence. No production integration or evaluator freeze is authorized yet.

## Next action
Execute this harness against canonical project GBPUSD OHLC. Use the existing project data path; do not create a new data source and do not tune parameters from outcomes.
