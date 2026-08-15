# MURPHY 0030 — P&F SOURCE / OPERATOR RECONCILIATION V3
Date: 2026-08-15
Status: SOURCE-ALIGNED / BOX-SCALE POLICY STILL OPEN

## Source findings
Murphy Chapter 11 supports the following construction facts:
- The 3-point reversal method is the relevant P&F framework for the trendline section.
- The 3-point reversal construction uses daily High/Low data: in an X column, continue using the daily high; only when no further X can be added is the daily low checked for a 3-box reversal. The inverse applies in an O column.
- P&F trendlines on these 3-point-reversal charts are drawn at 45 degrees.
- The Basic Bullish Support Line is drawn upward/right from under the lowest O column; while prices remain above it, the major trend is considered bullish.
- Murphy describes changing box size as a way to change sensitivity: 5-point and 10-point examples are shown, with the larger box producing fewer signals and being more suitable for long-term analysis; a smaller 3-point example produces more signals and is described as better for shorter-term trading.
- Murphy states that a value must be assigned to each box and notes that Chartcraft subscribers receive charts with the box values already assigned.

## Rule 0030 boundary
Project rule identity remains:
MURPHY_0030 = P&F bullish support.

The source therefore supports a structural evidence interpretation: a valid 3-point-reversal P&F bullish support line with price remaining above the line is bullish major-trend context.
This does NOT by itself convert 0030 into an autonomous BUY signal.

Do not map 0030 to S-7. S-7 is a distinct Murphy sell signal: downside breakout below a bullish support line.

## Exact remaining gap
Murphy's Chapter 11 examples demonstrate box-size choices, but the reviewed source does not provide a GBPUSD-specific box value or a reproducible formula that selects one for GBPUSD.
Therefore:
- do not choose 1/3/5/10 pips/points by backtest performance;
- do not invent an ATR or hidden lookback;
- do not claim a project-selected value is verbatim Murphy;
- do not use 2025 for selection.

## Next gate
1. Keep the 3-point reversal + High/Low + 45-degree bullish-support semantics source-locked.
2. Resolve the box-scale policy as a separate governed project operationalization only if necessary for deterministic GBPUSD implementation.
3. Compatibility-test the candidate shared P&F engine against the source-locked construction semantics.
4. Only then build the 0030 evaluator and run deterministic/no-lookahead tests.

## Status
SOURCE SEMANTICS: CLOSED
0030 STRUCTURAL OPERATOR: SOURCE-ALIGNED CANDIDATE
BOX-SCALE POLICY: OPEN / GOVERNANCE REQUIRED
P&F IMPLEMENTATION: NOT PRODUCTION-APPROVED
0030 EVALUATOR: NOT STARTED
FREEZE: BLOCKED
