# Murphy 0021–0023 — Adapter Test Matrix V1

Status: TEST SPECIFICATION — PENDING IMPLEMENTATION

| Test | Input status | Direction | Expected available | Expected gate | Expected direction | Expected conflict | Expected hint |
|---|---|---|---|---|---|---|---|
| T1 | PASS | BULLISH | true | pass | bullish | neutral | bullish |
| T2 | PASS | BEARISH | true | pass | bearish | neutral | bearish |
| T3 | FAIL | NONE | true | fail | neutral | contradicts | neutral |
| T4 | PASS | BULLISH | true | pass | bullish | neutral | bullish |
| T5 | FAIL | NONE | true | fail | neutral | contradicts | neutral |
| T6 | NOT_EVALUABLE | UNKNOWN | false | needs_review | neutral | insufficient | neutral |
| T7 | PASS | BEARISH | true | pass | bearish | neutral | bearish |
| T8 | unsupported status | UNKNOWN | false | needs_review | neutral | insufficient | neutral |
| T9 | PASS | missing/unknown direction | true | pass | neutral | neutral | neutral |
| T10 | any | any | unchanged | unchanged | unchanged | unchanged | unchanged |

## Assertions
- `confidence_delta` remains 0 for all tests.
- No test may infer the opposite direction from FAIL.
- NOT_EVALUABLE must never become PASS or FAIL.
- No test may introduce a timeframe, threshold, OI proxy, or historical outcome.
- 2025 metadata must not trigger tuning or selection.

## Scope
These tests validate only the evaluator-result-to-Decision-Brain evidence bridge. They do not replace evaluator unit tests or historical QA.
