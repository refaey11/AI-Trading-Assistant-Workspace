# Final OOS Performance Gate V1

Date: 2026-08-23

## Purpose
Define the single governed performance gate before any 2025 result is described as the Final Decision Brain performance result.

## Source-of-truth constraints
- 2025 remains OOS and evaluation-only.
- No OOS tuning, calibration, threshold/operator selection, or protocol changes.
- Frozen Murphy/Nison semantics are not reopened to improve performance.
- TIZ remains process-only; Similarity remains evidence-only; Risk remains a hard execution gate.

## Required uniform walk-forward
### Fold A
- Calibration: 2016-01-01 through 2023-12-31
- OOS: 2024-01-01 through 2024-12-31

### Fold B
- Calibration: 2016-01-01 through 2024-12-31
- OOS: 2025-01-01 through 2025-12-31

The two folds must use exactly the same:
- signal definition
- retrieval/index construction rules
- feature definitions and availability timestamps
- selection/k policy
- SL/TP model
- ambiguity policy
- execution timing
- transaction-cost model
- missing-evidence handling

## Leakage audit
The runner must prove, per OOS timestamp:
1. Only information available at or before the decision timestamp enters the feature/memory/index state.
2. Outcome/future-window columns are never used to construct the query, feature vector, retrieval index, weights, thresholds, or direction.
3. Any normalization/statistics/selection fit is based only on the calibration window for that fold.
4. OOS data cannot influence operator selection, k, risk parameters, thresholds, or candidate ranking.
5. Cross-year boundary state is carried only from previously completed observations.

## Final report contract
Publish Fold A, Fold B, and combined results with at least:
- trade/decision count
- PASS/FAIL/NOT_EVALUABLE counts
- win rate
- profit factor
- expectancy in R
- net P&L/R
- maximum drawdown
- transaction costs
- ambiguity counts and policy
- availability rate
- skipped/missing-evidence counts
- leakage-audit result

## Current evidence limitation
`TRUE_BACKTEST_V2` is not sufficient as the final performance result. Its stored configuration states that costs were not yet applied, and the existing official-baseline audit says the stored candidate results use different protocols/risk models/sample handling and therefore are not yet an official baseline.

## Gate status
BLOCKED until the executable uniform walk-forward + leakage-audit runner and its governed historical inputs are available and the two OOS folds complete successfully under one protocol.

## Next implementation step
Build or recover the existing project walk-forward runner before creating any new Decision Brain performance logic. Prefer auditing and integrating the existing implementation over rebuilding it from scratch.
