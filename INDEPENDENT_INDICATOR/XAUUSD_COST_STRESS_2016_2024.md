# XAUUSD Cost Stress — Indicator V2 — 2016–2024

## Scope
- Data: XAUUSD M1 master uploaded by the project owner.
- Development window: 2016–2024 only.
- 2025+: excluded from signal generation, tuning, and evaluation.
- Base research result: 8,658 completed trades, +327.0R, PF 1.058.

## Cost model
This is a fixed round-trip price-cost sensitivity model:
net_R = base_R - cost_price / (0.75 * ATR14 at entry).

It is a sensitivity test, not a historical bid/ask replay. The M1 master has OHLC only; it does not contain historical bid/ask spreads or execution slippage.

## Results
| Round-trip cost | Price units | Pips at 0.01 pip size | Net R | PF | 2024 OOS |
|---:|---:|---:|---:|---:|---:|
| 0.0 | 0.000 | 0.0 | +327.00 | 1.058 | +61.00 |
| 0.3 pips | 0.003 | 0.3 | +215.11 | 1.038 | +52.92 |
| 0.5 pips | 0.005 | 0.5 | +140.52 | 1.024 | +47.54 |
| 0.7 pips | 0.007 | 0.7 | +47.28 | 1.008 | +40.81 |
| 0.9 pips | 0.009 | 0.9 | -8.66 | 0.999 | +36.77 |
| 1.0 pips | 0.010 | 1.0 | -45.95 | 0.992 | +34.08 |
| 1.5 pips | 0.015 | 1.5 | -232.43 | 0.961 | +20.61 |
| 2.0 pips | 0.020 | 2.0 | -418.91 | 0.932 | +7.15 |

## Break-even
The fixed round-trip cost that consumes the entire +327R gross edge is approximately:
- 0.008768 price units
- 0.8768 XAUUSD pips

Any average all-in round-trip cost above this level makes the research edge negative under this model.

## Exness context
Exness currently documents XAUUSD with a 100 troy ounce contract and 0.01 pip size. Its help center lists XAUUSD commission at $3.50 per lot per side on Raw Spread accounts and $5.50 per lot per side on Zero accounts. Those commissions are equivalent to about 7 pips and 11 pips round-trip respectively for a 100-ounce lot, before spread/slippage, so those account types are incompatible with this prototype's tiny raw edge under this simple cost model.

Exness also states that gold spreads are floating and can widen, and its public commodity page says gold spreads start from 0.3 pips. A starting/minimum spread is not the same thing as an historical average.

## Gate interpretation
- This prototype is NOT live-ready.
- The gross +327R result is not sufficient.
- The Standard/commission-free path still requires historical bid/ask/tick-level execution replay.
- Raw Spread/Zero fail the simple commission stress by a very large margin.
- No 2025 data was used for tuning.

## Recommended next validation
Obtain Exness historical tick/bid-ask data for the same 2016–2024 timestamps and rerun the exact signal stream with:
1. actual spread at entry,
2. actual spread at exit,
3. conservative slippage,
4. the frozen 0.75 ATR / 2R risk contract,
5. separate 2016–2023 calibration and 2024 OOS reporting.
