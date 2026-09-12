# Range Reversal Ablation V1

## Objective
Determine which components actually create the positive 2025 OOS behavior observed in V1.2 Range Reversal.

## Base setup
- Range regime: ADX < 20 and ATR% >= 0.05
- Location: near support/resistance
- Nison-style candle confirmation
- RSI reversal around 50
- Fixed cost: 0.8 pip round trip
- SL: 1.2 ATR14
- TP: 2R
- Entry: next-bar open
- Ambiguous bar: loss
- No 2025 tuning

## Ablation matrix
1. Full base
2. Remove range regime
3. Remove location
4. Remove Nison confirmation
5. Remove RSI reversal
6. Remove MTF filter (if enabled in the variant)

Each variant must use identical execution and cost assumptions.

## Walk-forward protocol
- Train: 2016–2019, validation 2020, OOS 2021
- Train: 2016–2020, validation 2021, OOS 2022
- Train: 2016–2021, validation 2022, OOS 2023
- Train: 2016–2022, validation 2023, OOS 2024
- Train: 2016–2023, validation 2024, OOS 2025

2025 is untouched until the final walk-forward evaluation.

## Acceptance focus
Do not optimize for win rate alone. Track PF, expectancy in R, net R, maximum drawdown, trade count, and stability across OOS years.

A component is considered useful only if removing it materially weakens robustness rather than merely changing trade frequency.
