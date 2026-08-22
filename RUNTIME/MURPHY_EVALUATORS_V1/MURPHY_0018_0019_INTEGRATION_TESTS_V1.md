# Murphy 0018/0019 integration tests

Source basis: `MURPHY_0016_TO_0020_EXACT_MAPPING_V3.csv`.

Required chain:

`TRENDLINE_GEOMETRY_V1 -> TRENDLINE_CONVERGENCE_V1 -> MURPHY_0018/0019`

## Tested cases

1. Confirmed HIGH + LOW lines, exact gap rate < 0, both slopes < 0 -> 0018 PASS / BULLISH_STRUCTURE.
2. Confirmed HIGH + LOW lines, exact gap rate < 0, both slopes > 0 -> 0019 PASS / BEARISH_STRUCTURE.
3. Missing convergence evidence -> NOT_EVALUABLE.
4. Invalid line types -> NOT_EVALUABLE at adapter.
5. Non-converging gap rate -> evaluator receives `converging=false` and returns FAIL.
6. Adapter uses common availability timestamp and confirmed two-point lines only; no lookahead, tolerance, ATR, percentage, or timeframe selection is added.

Local execution result for the implemented chain: 6/6 PASS.

This records integration semantics only. Runtime count must not be raised until repository-level entry-point registration and full-path execution are verified.
