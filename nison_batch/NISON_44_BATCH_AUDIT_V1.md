# Nison 44-Rule Batch Audit V1

Built from the integrated rule registry plus the Steve Nison Master KB extracted locally.

## Batch result
- Total rules: 44
- BATCH_READY_CANDIDATE: 23
- SOURCE_LOCK_REVIEW: 15
- CONCEPT_GATE: 6

## Shared primitives
- trend_context
- confirmation_window
- candle_sequence
- ohlc_relationships
- gap_window
- volume_context
- sr_context

## Rule status
- CANDLE_RULE_0001 | Bullish Engulfing | SOURCE_LOCK_REVIEW | ops=trend_context|volume_context|confirmation_window|ohlc_relationships | blockers=near
- CANDLE_RULE_0002 | Bearish Engulfing | SOURCE_LOCK_REVIEW | ops=trend_context|volume_context|confirmation_window|ohlc_relationships | blockers=near
- CANDLE_RULE_0003 | Dark Cloud Cover | SOURCE_LOCK_REVIEW | ops=trend_context|volume_context|confirmation_window|ohlc_relationships | blockers=near
- CANDLE_RULE_0004 | Piercing Pattern | SOURCE_LOCK_REVIEW | ops=trend_context|volume_context|confirmation_window|ohlc_relationships | blockers=near
- CANDLE_RULE_0005 | On Neck | SOURCE_LOCK_REVIEW | ops=trend_context|confirmation_window | blockers=near
- CANDLE_RULE_0006 | In Neck | BATCH_READY_CANDIDATE | ops=trend_context|confirmation_window | blockers=-
- CANDLE_RULE_0007 | Thrusting | BATCH_READY_CANDIDATE | ops=trend_context|confirmation_window|ohlc_relationships | blockers=-
- CANDLE_RULE_0008 | Morning Star | BATCH_READY_CANDIDATE | ops=trend_context|confirmation_window|candle_sequence|ohlc_relationships | blockers=-
- CANDLE_RULE_0009 | Evening Star | BATCH_READY_CANDIDATE | ops=trend_context|confirmation_window|candle_sequence|ohlc_relationships | blockers=-
- CANDLE_RULE_0010 | Morning Doji Star | BATCH_READY_CANDIDATE | ops=trend_context|confirmation_window|candle_sequence|ohlc_relationships | blockers=-
- CANDLE_RULE_0011 | Evening Doji Star | BATCH_READY_CANDIDATE | ops=trend_context|confirmation_window|candle_sequence|ohlc_relationships | blockers=-
- CANDLE_RULE_0012 | Abandoned Baby | BATCH_READY_CANDIDATE | ops=trend_context|confirmation_window|ohlc_relationships | blockers=-
- CANDLE_RULE_0013 | Harami | SOURCE_LOCK_REVIEW | ops=trend_context|confirmation_window|candle_sequence|ohlc_relationships | blockers=near|small_body|long_real_body
- CANDLE_RULE_0014 | Harami Cross | SOURCE_LOCK_REVIEW | ops=trend_context|candle_sequence | blockers=long_real_body
- CANDLE_RULE_0015 | Tweezers Top | SOURCE_LOCK_REVIEW | ops=trend_context|confirmation_window|candle_sequence | blockers=near
- CANDLE_RULE_0016 | Tweezers Bottom | SOURCE_LOCK_REVIEW | ops=trend_context|confirmation_window|candle_sequence | blockers=near
- CANDLE_RULE_0017 | Upside Gap Two Crows | SOURCE_LOCK_REVIEW | ops=trend_context|confirmation_window|candle_sequence|ohlc_relationships | blockers=near
- CANDLE_RULE_0018 | Three Black Crows | SOURCE_LOCK_REVIEW | ops=trend_context|confirmation_window|candle_sequence|ohlc_relationships | blockers=near
- CANDLE_RULE_0019 | Bullish Counterattack Lines | SOURCE_LOCK_REVIEW | ops=trend_context|candle_sequence | blockers=near
- CANDLE_RULE_0020 | Bearish Counterattack Lines | BATCH_READY_CANDIDATE | ops=trend_context|candle_sequence | blockers=-
- CANDLE_RULE_0021 | Three Mountains | BATCH_READY_CANDIDATE | ops=trend_context|candle_sequence | blockers=-
- CANDLE_RULE_0022 | Three Rivers | BATCH_READY_CANDIDATE | ops=trend_context|candle_sequence | blockers=-
- CANDLE_RULE_0023 | Three Buddha Tops | BATCH_READY_CANDIDATE | ops=trend_context|candle_sequence|ohlc_relationships | blockers=-
- CANDLE_RULE_0024 | Three Buddha Bottoms | BATCH_READY_CANDIDATE | ops=trend_context|candle_sequence|ohlc_relationships | blockers=-
- CANDLE_RULE_0025 | Dumpling Top | BATCH_READY_CANDIDATE | ops=trend_context|gap_window | blockers=-
- CANDLE_RULE_0026 | Fry Pan Bottom | BATCH_READY_CANDIDATE | ops=trend_context|gap_window | blockers=-
- CANDLE_RULE_0027 | Tower Top | BATCH_READY_CANDIDATE | ops=trend_context|candle_sequence | blockers=-
- CANDLE_RULE_0028 | Tower Bottom | BATCH_READY_CANDIDATE | ops=trend_context|candle_sequence | blockers=-
- CANDLE_RULE_0029 | Unique Three River Bottom | SOURCE_LOCK_REVIEW | ops=trend_context|candle_sequence | blockers=near
- CANDLE_RULE_0030 | Three Rising Methods | BATCH_READY_CANDIDATE | ops=trend_context|candle_sequence|ohlc_relationships | blockers=-
- CANDLE_RULE_0031 | Three Falling Methods | BATCH_READY_CANDIDATE | ops=trend_context | blockers=-
- CANDLE_RULE_0032 | Three White Soldiers | SOURCE_LOCK_REVIEW | ops=candle_sequence|ohlc_relationships | blockers=near|session_highs|stabilization|most_positive
- CANDLE_RULE_0033 | Advance Block (Stalled Pattern) | SOURCE_LOCK_REVIEW | ops=- | blockers=difficulty
- CANDLE_RULE_0034 | Separating Lines | BATCH_READY_CANDIDATE | ops=trend_context|ohlc_relationships | blockers=-
- CANDLE_RULE_0035 | Tasuki Gap | BATCH_READY_CANDIDATE | ops=trend_context|candle_sequence|ohlc_relationships|gap_window | blockers=-
- CANDLE_RULE_0036 | Gapping Play | BATCH_READY_CANDIDATE | ops=trend_context|candle_sequence|ohlc_relationships|sr_context|gap_window | blockers=-
- CANDLE_RULE_0037 | Side-by-Side White Lines | BATCH_READY_CANDIDATE | ops=trend_context|candle_sequence|ohlc_relationships|gap_window | blockers=-
- CANDLE_RULE_0038 | Windows | BATCH_READY_CANDIDATE | ops=trend_context|candle_sequence|ohlc_relationships|sr_context|gap_window | blockers=-
- CANDLE_RULE_0039 | 06_Multiple_Technical_Techniques | CONCEPT_GATE | ops=confirmation_window|sr_context | blockers=-
- CANDLE_RULE_0040 | 13_Candlestick_Clusters: | CONCEPT_GATE | ops=- | blockers=-
- CANDLE_RULE_0041 | 14_Trend_Lines: | CONCEPT_GATE | ops=trend_context | blockers=-
- CANDLE_RULE_0042 | 15_Support_Resistance: | CONCEPT_GATE | ops=sr_context | blockers=-
- CANDLE_RULE_0043 | 16_False_Breakouts: | CONCEPT_GATE | ops=- | blockers=-
- CANDLE_RULE_0044 | 17_Polarity_Principle: | CONCEPT_GATE | ops=- | blockers=-

## Execution policy
- No threshold is invented from backtest results.
- Nison remains confirmation-only.
- Concept rules 0039-0044 are not candle recognizers; they require context/evidence evaluation.
- BATCH_READY_CANDIDATE is not Frozen; each rule still needs exact source QA, evaluator tests, and historical replay.
