# Murphy 0030–0032 — Rule Contract V1

Status: DRAFT / SOURCE-BOUNDED / NOT PRODUCTION FROZEN

## MURPHY_0030 — P&F bullish support

Source mapping: Chapter 11, Point & Figure.

Required evidence:
1. A valid 3-box P&F construction exists.
2. X/O columns are constructed from completed D1 High/Low data using the source High-first/Low-first directional rule.
3. A bullish 45-degree support reference exists, originating from the base of the lowest O column.

Output:
- direction = BULLISH
- evidence_type = PNF_BULLISH_SUPPORT_REFERENCE
- support_origin_column
- support_origin_price
- availability_timestamp
- status = AVAILABLE | NOT_EVALUABLE

Boundary:
0030 is structural context. It does not create an autonomous trade entry.

## MURPHY_0031 — P&F long stop reference

Required evidence:
1. A valid P&F uptrend context exists.
2. The previous O column is available.

Output:
- direction = BULLISH
- stop_relation = BELOW_PREVIOUS_O_COLUMN
- reference_column
- reference_price
- availability_timestamp
- status = AVAILABLE | NOT_EVALUABLE

Boundary:
Murphy gives the placement relation; this contract does not invent a pip/ATR/percentage offset.

## MURPHY_0032 — P&F short stop reference

Required evidence:
1. A valid P&F downtrend context exists.
2. The previous X column is available.

Output:
- direction = BEARISH
- stop_relation = ABOVE_PREVIOUS_X_COLUMN
- reference_column
- reference_price
- availability_timestamp
- status = AVAILABLE | NOT_EVALUABLE

Boundary:
Murphy gives the placement relation; this contract does not invent a pip/ATR/percentage offset.

## Shared gates

- D1 OHLC only when completed/available.
- No future data.
- 2025 excluded from tuning/selection.
- No profitability-based selection of box size.
- No invented box-size formula.
- No invented stop offset.
- No autonomous BUY/SELL decision.
- Missing required P&F construction inputs => NOT_EVALUABLE.

## Remaining production gate

Box-size policy and bootstrap policy must be explicitly approved for the GBPUSD production evaluator. Murphy describes that box size can be varied and describes Kenneth Tower's volatility-screened logarithmic approach, but the project source does not contain Tower's exact screening formula. Therefore the production evaluator must not silently substitute a formula or tune a percentage from historical outcomes.
