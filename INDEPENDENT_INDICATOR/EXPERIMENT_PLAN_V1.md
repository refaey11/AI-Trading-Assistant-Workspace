# Independent Indicator Experiment Plan V1

## Goal
Test whether the layered architecture improves trade quality versus simple baselines. Do not optimize toward an arbitrary win-rate target.

## Baselines

A. EMA direction only.

B. EMA + RSI.

C. Supertrend + volume confirmation.

D. Murphy-style direction + Nison-style confirmation (prototype).

E. Full layered prototype: regime + direction + location + confirmation + quality + MTF + risk.

## Required evaluation

For every variant, report:

- Number of trades
- Win rate
- Profit factor
- Expectancy in R
- Net R
- Maximum drawdown in R
- Average winner / average loser
- Median trade R
- NO TRADE percentage
- Long vs short results
- Results by regime
- Results by pair
- Results by timeframe
- Cost-adjusted results

## Anti-overfitting rules

1. Development/calibration: 2016-2023.
2. First out-of-sample test: 2024.
3. Second out-of-sample test: 2025.
4. Do not change parameters after inspecting 2025.
5. No lookahead.
6. MTF data must use confirmed higher-timeframe bars.
7. Volume unavailable must remain unavailable, not converted to zero volume.
8. If a setup has conflicting direction/confirmation, output NO TRADE.
9. Compare the same entry, SL, TP, ambiguity and cost assumptions across variants.

## Success criterion

The prototype is successful only if the layered design demonstrates a stable improvement in expectancy / drawdown / profit factor across unseen periods without requiring extreme parameter tuning. A high win rate by itself is not sufficient.
