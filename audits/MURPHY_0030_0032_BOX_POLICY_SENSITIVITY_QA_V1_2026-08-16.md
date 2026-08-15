# Murphy 0030–0032 — Box Policy Sensitivity QA V1

Date: 2026-08-16
Status: DIAGNOSTIC / NOT PRODUCTION FROZEN

## Data
Canonical GBPUSD D1 file:
- 2,544 daily rows
- 2016-01-03 through 2024-12-31

Source file is the project D1 dataset; 2025 is excluded from all policy selection and diagnostics.

## Calibration
Three-calendar-year calibration block:
- 2016-01-03 through 2018-12-31
- 934 daily log-return observations
- sample standard deviation of daily log returns: 0.006257356643053344
- proposed project box percentage: 0.6257356643053344%

This is a project operationalization only. It is not claimed to be Kenneth Tower's exact conversion formula.

## Pre-declared sensitivity diagnostic
The following percentages were inspected only as a structural sensitivity set:
- 0.50%
- 0.6257356643% (proposal)
- 0.75%
- 1.00%

No value was selected using trade count, P&L, win rate, or 2025.

## 2019–2024 logarithmic P&F construction results
Using D1 High/Low construction and 3-box reversal:

| Box % | Columns | X columns | O columns |
|---:|---:|---:|---:|
| 0.50% | 137 | 68 | 69 |
| 0.6257356643% | 89 | 44 | 45 |
| 0.75% | 71 | 35 | 36 |
| 1.00% | 45 | 22 | 23 |

The bullish-support structural origin from the lowest O-column was approximately:
- 0.50% → 1.03553
- 0.6257356643% → 1.03814
- 0.75% → 1.03807
- 1.00% → 1.04060

This shows that the structural origin is relatively stable across the first three diagnostics, while chart sensitivity changes substantially with box size.

## Interpretation
The sensitivity run is NOT an optimization and does not prove that 0.6257356643% is the correct Murphy/Tower value. It only demonstrates that the proposed project policy is computationally usable and that box size materially affects P&F sensitivity.

## Next gates
1. CI execution of the new logarithmic P&F unit tests.
2. Independent fresh 2019–2024 0030–0032 evaluator run using the proposal.
3. Availability/no-lookahead audit.
4. Provenance/freeze review.
5. Only after approval: 2025 OOS evaluation.

Until all gates pass, 0030–0032 remain NOT_EVALUABLE / PROPOSAL_PENDING.
