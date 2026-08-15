# Murphy 0025–0026 — Production Freeze Record V1

Date: 2026-08-15
Status: PRODUCTION FROZEN

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
- Rule-level test suite: 10/10 PASS, executed 2026-08-15.
- Full 2016–2024 replay: 55,192 rows; 8/8 checks PASS.
- 0025: 6,024 PASS / 48,801 FAIL / 367 NOT_EVALUABLE.
- 0026: 5,718 PASS / 49,107 FAIL / 367 NOT_EVALUABLE.
- Availability/no-lookahead: 8/8 PASS.
- Future-reference violations: 0.
- 2025 rows in historical replay: 0.

## QA correction resolved
A prior freeze was temporarily downgraded to Freeze Candidate because the 10 rule cases had initially been specified but not executed as a suite. The suite was subsequently executed and produced 10/10 PASS. This record is now finalized only after that missing gate was completed.

## Governance locks
- No fixed-bar substitution.
- No new threshold.
- No timeframe invention.
- No 2025 tuning/selection.
- No inference from missing evidence.
- Any semantic/evaluator/feature/bridge change requires a new compatibility audit, replay, availability audit, rule-test execution, backup, and re-freeze.

## Decision
Murphy 0025–0026 are Production Frozen within the scope and evidence listed above.