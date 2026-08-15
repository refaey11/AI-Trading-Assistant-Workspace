# Murphy 0030 P&F Prefix / No-Lookahead Test Plan V1

Status: TEST PLAN / NOT PASSED
Date: 2026-08-15

## Objective
Prove that the selected P&F construction and Murphy semantic adapter cannot use future source bars to alter previously emitted state.

## Tests
### T1 Determinism
Run identical canonical input twice with identical frozen parameters. Serialized P&F and adapter outputs must be byte-equivalent.

### T2 Prefix replay
For cutoff T, run the full input through T and separately run the same input truncated at T. All states emitted at or before T must match exactly.

### T3 Future-suffix invariance
For a set of historical cutoffs, append progressively larger future suffixes. Previously emitted states must not change.

### T4 Fold isolation
For each walk-forward fold, calculate box policy only from calibration data. OOS data must not affect the frozen box parameter.

### T5 Intrabar ordering gate
D1 OHLC does not encode whether High or Low occurred first. The evaluator must not silently assume an ordering. If the selected engine requires ordering, the construction remains unresolved unless an approved deterministic policy is established independently of OOS performance.

### T6 Adapter isolation
Engine-specific trendline heuristics, lookback rules, touch tolerances, and break buffers must not enter Murphy evidence unless independently source-approved.

## Pass criteria
All applicable tests pass. Any failed or untestable gate keeps 0030 in PRE-FREEZE / NOT_EVALUABLE status.

## Prohibited behavior
- No tuning based on OOS or profitability.
- No changing the box formula after seeing evaluator results.
- No future-confirmed pivot represented as available before confirmation.
- No silent intrabar ordering assumption.
