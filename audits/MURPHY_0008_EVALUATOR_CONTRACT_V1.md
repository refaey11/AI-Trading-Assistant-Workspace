# Murphy 0008 — Deterministic Evidence Evaluator Contract V1

Status: EXPERIMENTAL VALIDATION — NOT PRODUCTION FROZEN

## Purpose
Evaluate only the frozen 0008 validation path. Do not create a second breakout engine.

## Inputs
- GBPUSD D1 OHLC, 2016–2024 only.
- PIVOT_SEQUENCE_V2 confirmed LOW pivots with availability chronology.
- Frozen PF-H1 singleton Support boundary.
- Frozen PF-B1 two-successive-D1-close decisive-break operator.

## Event state machine
1. `SUPPORT_AVAILABLE`: confirmed LOW pivot is available before break observation.
2. `BREAK_CANDIDATE`: a completed D1 close is strictly below the Support boundary.
3. `DECISIVE_BREAK_CONFIRMED`: the immediately following completed D1 close is also strictly below the same Support boundary.
4. `RETEST_OBSERVATION`: starts only after the confirmation close.
5. `ROLE_REVERSAL_EVIDENCE`: a later D1 bar intersects the Support boundary and closes strictly below it.
6. `NOT_EVALUABLE`: required Support/chronology evidence is unavailable or ambiguous.

## Output
Each event must include:
- rule_id = MURPHY_0008
- support pivot identity
- support price
- support availability timestamp
- candidate break timestamp
- confirmation timestamp
- confirmation status
- retest timestamp/status when observed
- role-reversal evidence timestamp/status when observed
- provenance references
- evaluator version

## Deterministic constraints
- No future pivots may redefine a past Support boundary.
- No same-bar confirmation from the first close.
- Retest cannot occur on or before the confirmation bar.
- No clustering/equality tolerance.
- No ATR/pips/percentage thresholds.
- No hidden lookback.
- No 2025 input.
- Event counts are not trading-performance metrics.

## Required validation
- Unit tests for every state transition.
- Availability/no-lookahead tests.
- 2016–2024 fresh replay.
- Missing-input `NOT_EVALUABLE` tests.
- Role-reversal chronology tests.
- Provenance/evidence backup.

## Freeze boundary
This contract is an experimental evaluator contract. Production freeze requires all validation gates to pass and an explicit production-freeze decision.
