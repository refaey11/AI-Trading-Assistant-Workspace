# Murphy 0033 — Source Reconciliation V2

Status: SOURCE-RESOLVED / CONTRACT-CANDIDATE / NOT FROZEN

## Rule identity
- Rule ID: MURPHY_0033
- Working name: Candlestick context filter
- Book: *Technical Analysis of the Financial Markets* — John J. Murphy
- Chapter 12: Japanese Candlesticks
- Section: Filtered Candle Patterns
- Direction: NEUTRAL / contextual evidence

## Source reconciliation
Murphy's Chapter 12 contains the filtered-candle-pattern section. The section explicitly attributes the filtering concept to Greg Morris (1991), while Murphy presents and explains the technique in the chapter. Therefore:

- Murphy attribution: chapter/source presentation and integration in Murphy's book.
- Concept attribution: Greg Morris, as explicitly stated by Murphy.
- This is not a contradiction and must not be recorded as if Murphy originated the filtering concept.

## Source-bounded semantics
1. Short-term market trend must be identified before a candle pattern can exist.
2. Traditional technical analysis / oscillator context is used to improve candle-pattern reliability and remove bad or premature patterns.
3. The worked example uses Stochastics %D.
4. Stochastics %D uses 20 as oversold and 80 as overbought; the areas below 20 and above 80 are the presignal areas.
5. Candle patterns are considered only when %D is in the presignal area; a pattern with %D around 65 is ignored.
6. Only reversal candle patterns are considered by the filtering concept.
7. Murphy states that other oscillators such as RSI, CCI, and Williams %R can also be used.

## Project implementation boundary
The following are SOURCE-BOUNDED candidates, not backtest-derived parameters:
- Oscillator profile: Stochastic %D (worked example).
- Presignal zones: %D < 20 or %D > 80.
- Pattern class: reversal candles only.
- Context requirement: short-term trend + oscillator presignal context.

The alternatives (RSI, CCI, Williams %R) remain compatible source alternatives and must not silently replace the worked Stochastic profile.

## Architecture
Murphy 0033 provides contextual evidence only. Nison remains the existing candlestick confirmation layer. The rule must not independently create a BUY/SELL direction.

Expected evidence states:
- CONFIRMED: reversal candle + valid short-term context + oscillator presignal context.
- CONFLICT: reversal candle conflicts with required context.
- NOT_EVALUABLE: required context/operator input is unavailable.

## Freeze gates
Still required before production freeze:
1. Rule-specific evaluator implementation.
2. Deterministic unit tests.
3. No-lookahead/prefix replay tests.
4. Historical QA on 2016–2024 only.
5. Provenance and availability checks.
6. Canonical registry/freeze commit.

2025 must remain OOS and must not be used for parameter tuning.

## Decision
0033 is no longer blocked on source discovery. The source semantics and attribution are reconciled. The next work item is implementation of the source-bounded evaluator and tests; production freeze remains blocked until all freeze gates pass.
