# Independent Murphy + Nison Signal Prototype V1

This is an **isolated research prototype**. It does not modify the main Decision Brain logic and does not replace the governed Murphy/Nison evidence pipeline.

## Design borrowed from successful indicator architectures

1. **Regime gate** — trend / range / transition.
2. **Primary direction** — Murphy-style market structure and trend context.
3. **Location** — swing support/resistance and breakout/retest context.
4. **Confirmation** — Nison-style candlestick confirmation; confirmation cannot create direction by itself.
5. **Quality filters** — volume, momentum and volatility.
6. **MTF agreement** — higher-timeframe direction must agree with the setup.
7. **Confidence score** — combines independent confirmations instead of relying on one indicator.
8. **Risk gate** — ATR stop and minimum R:R.
9. **Output** — BUY / SELL / NO TRADE.

## Important separation

- This branch is independent from the production Decision Brain.
- It does not reopen or change frozen Murphy/Nison rules.
- It does not use 2025 for tuning.
- It is fail-closed: conflicting or incomplete evidence produces NO TRADE.
- The Nison layer in the Pine prototype is explicitly **Nison-inspired price-action confirmation**, not a claim that all 44 governed Nison rules are reproduced in Pine.

## Signal flow

```text
PRICE
  -> REGIME
  -> MURPHY DIRECTION
  -> STRUCTURE / LOCATION
  -> NISON-STYLE CONFIRMATION
  -> VOLUME / MOMENTUM
  -> MTF AGREEMENT
  -> SCORE
  -> R:R GATE
  -> BUY / SELL / NO TRADE
```

## Initial six-timeframe ladder

The prototype defaults to:

- 5m chart
- 15m confirmation
- 30m confirmation
- 1H confirmation
- 4H context
- 1D context

Higher-timeframe requests use confirmed bars (`lookahead_off`) to avoid future leakage.

## What we will measure

Do not optimize for win rate alone. The research harness should report:

- Win rate
- Profit factor
- Expectancy per trade
- Net R / P&L
- Maximum drawdown
- Average winner / loser
- Trade count
- NO TRADE rate
- Results by regime
- Results by pair and timeframe
- Results before and after realistic costs

The first objective is to discover whether the layered architecture has a real edge. An 80% win-rate target is not assumed.
