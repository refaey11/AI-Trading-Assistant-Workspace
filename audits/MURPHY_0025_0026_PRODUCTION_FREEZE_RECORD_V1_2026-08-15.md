# Murphy 0025–0026 — Production Freeze Record V1

Date: 2026-08-15
Status: FREEZE CANDIDATE — PRODUCTION FREEZE PENDING

## Scope
- Murphy 0025 — New 4-Week High -> Bullish
- Murphy 0026 — New 4-Week Low -> Bearish

## Locked semantics
- Four-week window = four completed ISO calendar weeks preceding the current ISO week.
- Current week excluded.
- 0025: current High >= preceding four-week High -> PASS/BULLISH.
- 0026: current Low <= preceding four-week Low -> PASS/BEARISH.
- Missing reference -> NOT_EVALUABLE.
- Existing H1 boolean propagation columns are not authoritative row-level triggers.

## Validation evidence completed
- Deterministic replay: 5/5 PASS.
- Full 2016–2024 replay: 55,192 rows; 8/8 checks PASS.
- 0025: 6,024 PASS / 48,801 FAIL / 367 NOT_EVALUABLE.
- 0026: 5,718 PASS / 49,107 FAIL / 367 NOT_EVALUABLE.
- Availability/no-lookahead: 8/8 PASS.
- Future-reference violations: 0.
- 2025 rows in historical replay: 0.

## QA limitation discovered after drafting this record
The 10 rule test cases were specified as a test suite, but they were not all executed as an independent automated unit-test run. Therefore the prior PRODUCTION FROZEN status was premature.

This record is corrected to FREEZE CANDIDATE / PENDING.

## Required final gate
Before Production Freeze, execute the 10 specified rule-level unit tests as an actual test run and record the pass/fail output. If all pass, update this record to PRODUCTION FROZEN.

## Governance locks
- No fixed-bar substitution.
- No new threshold.
- No timeframe invention.
- No 2025 tuning/selection.
- No inference from missing evidence.
- Any semantic/evaluator/feature/bridge change requires a new compatibility audit, replay, availability audit, and re-freeze.