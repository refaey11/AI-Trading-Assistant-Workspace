# Murphy 0008 — PF-B1 Implementation Progress

Date: 2026-08-22

## Scope
Progress toward a source-faithful runtime implementation of Murphy 0008 using the supplied PF-H1/PF-B1 candidate artifacts.

## Verified source data
- PF-H1 horizontal-level candidates: 2,392 (2016-2024)
- PF-H1 roles: 1,198 SUPPORT / 1,194 RESISTANCE
- PF-B1 raw breakout candidates: 2,335 (2020-2024)
- PF-B1 availability violations: 0
- 2016-2019 PF-B1 replay: NOT_RUN because the runnable OHLC event series is not exposed in the artifact set
- 2025: excluded

## Candidate operator
Use only an already-approved/available PF-H1 boundary and the first completed-bar PF-B1 close beyond it. No ATR, percentage, pip, volume, or multi-day threshold is imported.

## 0008 role-reversal requirement
0008 still requires the later rally/retest and confirmation that broken support acts as resistance. The supplied PF-B1 event dataset does not expose an approved downstream retest/role-reversal producer, so that stage returns NOT_EVALUABLE until such evidence is supplied.

## Implementation status
- Candidate evaluator: ADDED
- Deterministic unit tests: ADDED
- Production-frozen PF-B1 governance contract: NOT YET PROMOTED
- 0008 Runtime Implemented: NO
- 0008 remains outside the Runtime count until governance promotion and readable end-to-end evidence exist.

## Next action
1. Promote the minimal PF-B1 candidate contract through governance without adding numeric thresholds.
2. Recover/produce approved retest/role-reversal evidence for 0008.
3. Run 2016-2024 QA on the complete 0008 path.
4. Wire the candidate into the repository runtime entry point only after the contract is approved.
