# Nison 0001–0007 Canonical Clause Decomposition V1

Status: SOURCE-DERIVED DECOMPOSITION — NOT FROZEN

This artifact records what the current Nison source files actually state. It does not assign project primitives, thresholds, tolerances, lookbacks, or evaluators unless those are explicitly present in the source.

## 0001 — Bullish Engulfing (C101)
Source: `01_Trading_Knowledge_Database/01_Candlestick_Patterns/02_Double_Candles/C101_Bullish_Engulfing/`

### Formation clauses
- Must appear after a downtrend.
- Two candles.
- First candle is bearish.
- Second candle is bullish.
- Second real body completely engulfs first real body.
- Shadows do not need to be engulfed.
- Larger second candle = stronger signal.
- Small first candle = stronger reversal.

### Confirmation clauses
- Never buy immediately; wait for confirmation.
- Bullish confirmation: strong bullish candle OR break above engulfing high.
- Best location: support, demand zone, end of downtrend, moving-average support.
- High volume = higher probability.
- Avoid sideways markets, weak volume, and no trend.
- Entry is BUY after confirmation.

### Operational status
Exact candle-count/colour/body-engulfment relations are source-stated. `Strong bullish candle`, `downtrend`, `support`, `demand zone`, `high volume`, and the strength statements remain qualitative unless an approved compatible primitive/adapter exists. No threshold is invented here.

## 0002 — Bearish Engulfing (C102)
### Formation clauses
- Must appear after an uptrend.
- Two candles.
- First candle is bullish.
- Second candle is bearish.
- Second real body completely engulfs first real body.
- Shadows do not need to be engulfed.
- Larger second candle = stronger signal.
- Small first candle = stronger reversal.

### Confirmation clauses
- Never sell immediately; wait for confirmation.
- Bearish confirmation: strong bearish candle OR break below engulfing low.
- Best location: resistance, supply zone, end of uptrend, moving-average resistance.
- High volume = higher probability.
- Avoid sideways markets, weak volume, and no trend.
- Entry is SELL after confirmation.

### Operational status
Exact two-candle/body relations are source-stated. Qualitative context/strength clauses remain unresolved without compatible approved primitives.

## 0003 — Dark Cloud Cover (C103)
### Formation clauses
- Must appear after an uptrend.
- Two candles.
- First candle is a long bullish candle.
- Second candle opens above previous high.
- Second candle closes below the midpoint of the previous bullish body.
- Second candle does not completely engulf the first body.
- Deeper penetration = stronger signal.

### Confirmation clauses
- Never sell immediately; wait for confirmation.
- Bearish confirmation: strong bearish candle OR break below Dark Cloud Cover low.
- Best location: resistance, supply zone, end of uptrend.
- High volume = higher probability.
- Avoid sideways markets, weak volume, and no trend.
- Entry is SELL after confirmation.

### Operational status
The open/close/midpoint relations are source-stated. `long`, `uptrend`, `strong`, `deeper`, resistance/supply, and volume quality remain qualitative unless an approved primitive exists.

## 0004 — Piercing Pattern (C104)
### Formation clauses
- Must appear after a downtrend.
- Two candles.
- First candle is a long bearish candle.
- Second candle opens below previous low.
- Second candle closes above the midpoint of the previous bearish body.
- Second candle does not engulf the first body.
- Deeper penetration = stronger signal.

### Confirmation clauses
- Never buy immediately; wait for confirmation.
- Bullish confirmation: strong bullish candle OR break above Piercing Pattern high.
- Best location: support, demand zone, end of downtrend.
- High volume = higher probability.
- Avoid sideways market, weak volume, and no trend.
- Entry is BUY after confirmation.

### Operational status
The midpoint/open/engulfment relations are source-stated. Qualitative terms remain unresolved.

## 0005 — On Neck (C105)
### Formation clauses
- Existing downtrend.
- First candle: long bearish body.
- Second candle opens below previous low.
- Second candle is bullish.
- Second candle closes near previous close.
- Second candle must not close above the midpoint of the previous body.
- Invalid after an uptrend, if second candle closes above midpoint, or if second candle engulfs previous candle.

### Trading clauses
- Pattern meaning: bearish continuation, not a reversal.
- Entry: sell after bearish confirmation.
- Stop: above high of second candle.
- Target: previous swing low.
- Risk/reward ≥ 1:2.
- Trail stop if momentum remains bearish.

### Operational status
`near previous close`, `long`, downtrend, bearish confirmation, previous swing low, and momentum remain qualitative/contextual. The explicit midpoint/engulfment invalidations are source-stated.

## 0006 — In Neck (C106)
### Formation clauses
- Existing downtrend.
- First candle: long bearish body.
- Second candle opens below previous low.
- Second candle is bullish.
- Second candle closes slightly above previous close.
- Second candle remains below midpoint of previous body.
- Invalid after uptrend, above-midpoint close, Piercing Pattern formation, or engulfment.

### Trading clauses
- Pattern meaning: bearish continuation, not a reversal.
- Entry: sell after bearish confirmation.
- Stop: above high of second candle.
- Target: previous swing low.
- Risk/reward ≥ 1:2.
- Trail stop while bearish momentum continues.

### Operational status
`slightly above`, long, downtrend, bearish confirmation, swing low, and momentum require compatible operationalization. Explicit relational invalidations are source-stated.

## 0007 — Thrusting (C107)
### Formation clauses
- Existing downtrend.
- First candle: long bearish body.
- Second candle opens below previous low.
- Second candle is bullish.
- Second candle closes well into the previous bearish body.
- Second candle must remain below midpoint of previous body.
- Invalid after uptrend, above-midpoint close, Piercing Pattern formation, or engulfment.

### Trading clauses
- Pattern meaning: bearish continuation, not a reversal.
- Entry: sell after bearish confirmation.
- Stop: above high of second candle.
- Target: previous swing low.
- Risk/reward ≥ 1:2.
- Trail stop if bearish momentum continues.

### Operational status
`well into`, long, downtrend, bearish confirmation, swing low, and momentum remain qualitative. The explicit midpoint/Piercing/engulfment constraints are source-stated.

## Batch decision
- 0001–0007 now have source-derived clause decomposition.
- No new threshold, tolerance, lookback, scoring rule, or direction generator was introduced.
- Next gate: map only exact/compatible clauses to existing approved primitives and adapters; leave unresolved qualitative clauses NOT_EVALUABLE.
- Historical QA must occur only after an evaluator contract is closed; 2025 remains OOS and cannot be used for tuning/selection/calibration/optimization.
- No production freeze granted.