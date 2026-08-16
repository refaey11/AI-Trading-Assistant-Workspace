# Nison 0001–0007 Adapter Mapping V1

Status: ADAPTER GATE — NOT FROZEN

## Purpose
Map source-derived clauses to existing project primitives without changing Nison semantics. This document is a compatibility gate, not a production evaluator.

| Rule | Clause family | Existing primitive candidate | Adapter decision | Status |
|---|---|---|---|---|
| 0001 Bullish Engulfing | 2-candle polarity/body containment | Existing candlestick body/polarity primitives may represent the hard geometry | Adapter candidate for hard geometry only; confirmation/context remain separate | PARTIAL |
| 0002 Bearish Engulfing | 2-candle polarity/body containment | Existing candlestick body/polarity primitives may represent the hard geometry | Adapter candidate for hard geometry only; confirmation/context remain separate | PARTIAL |
| 0003 Dark Cloud Cover | 2-candle polarity/penetration | Existing body/open/close primitives may cover hard relationships if source contract matches | No adapter promoted until exact source comparator is verified | BLOCKED |
| 0004 Piercing Pattern | 2-candle polarity/penetration | Existing body/open/close primitives may cover hard relationships if source contract matches | No adapter promoted until exact source comparator is verified | BLOCKED |
| 0005 On Neck | 2-candle polarity/close relationship | Existing body/open/close primitives may cover hard relationship | No adapter promoted until source exactness and tolerance semantics are verified | BLOCKED |
| 0006 In Neck | 2-candle polarity/close relationship | Existing body/open/close primitives may cover hard relationship | No adapter promoted until source exactness and tolerance semantics are verified | BLOCKED |
| 0007 Thrusting | 2-candle polarity/penetration | Existing body/open/close primitives may cover hard relationships | No adapter promoted until exact penetration comparator is source-locked | BLOCKED |

## Hard governance
1. The adapter may only translate an already-approved primitive into the Nison contract.
2. It may not introduce a new threshold, percentage, pip tolerance, ATR multiple, lookback, or scoring rule.
3. Qualitative clauses such as trend, support, strong candle, or high volume remain unmeasurable until an approved operationalization exists.
4. Confirmation remains confirmation; it cannot generate market direction.
5. No 2025 data may be used for tuning, calibration, selection, or optimization.
6. No automatic freeze is granted by this mapping.

## Result
0001–0007 are **not production-ready evaluators yet**. 0001/0002 have the clearest hard-geometry adapter candidates; 0003–0007 require source-exact comparator verification before promotion. This is intentional fail-closed behavior.