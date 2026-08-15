# Murphy 0025–0026 Rule Test Suite V1

Date: 2026-08-15
Status: TEST SPEC LOCKED / FULL EVALUATOR REPLAY PENDING

## Deterministic cases
- 0025: high above four-week high -> PASS/BULLISH
- 0025: high equal to four-week high -> PASS/BULLISH
- 0025: high below four-week high -> FAIL/NEUTRAL
- 0025: missing four-week reference -> NOT_EVALUABLE
- 0026: low below four-week low -> PASS/BEARISH
- 0026: low equal to four-week low -> PASS/BEARISH
- 0026: low above four-week low -> FAIL/NEUTRAL
- 0026: missing four-week reference -> NOT_EVALUABLE
- Current week must not enter its own four-week reference.
- 2025 must not enter historical QA/tuning.

## Independent replay result
- 55,192 H1 rows inspected.
- 54,825 rows had a four-week reference.
- 0025 row-level PASS: 6,024.
- 0026 row-level PASS: 5,718.
- 2025 rows: 0.
- Deterministic replay checks: 5/5 PASS.

## Rule operators
0025: current high >= preceding four completed ISO weeks high.
0026: current low <= preceding four completed ISO weeks low.

The existing H1 boolean feature columns are not treated as authoritative row-level triggers because they are weekly-event propagation and do not match the exact row-level operator in every row.

This artifact does not grant Production Freeze.