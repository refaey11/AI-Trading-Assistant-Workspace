# Opportunity Discovery — 2026-09-12

## Purpose

This is an analytical discovery pass over the recovered governed V5.4 source artifact. It does not modify Murphy, Nison, Decision Brain, Risk, MTF, Memory, or 2025 OOS data.

## Source

Recovered governed source artifact: `current-stack-development-backtest-2016-2024-v5-4` (2016-2024 development window).

Observed source-backed Murphy stream:
- 87,225 Murphy rows.
- 30,678 PASS rows in the governed stream.
- 34 Murphy rules are runtime-eligible, but the recovered historical producer stream contains only 11 composite `pass_rule_id` forms, representing partial source coverage.

Nison:
- 2,428,448 rows.
- 44 governed rule IDs.
- 0 PASS rows in this recovered development artifact.
- Therefore Nison cannot currently provide positive confirmation in this artifact; absence/failure is not treated as a contradiction in V5.4.

## Raw opportunity diagnostic

Using the existing frozen V5.4 execution geometry (0.75 ATR stop / 2R target), event-at-close entry, subsequent H1 event-driven exits, and no inferred 2025 data:

- 29,163 Murphy directional candidate rows reached the raw outcome diagnostic after ATR availability checks.
- 28,783 closed outcomes were realized in the diagnostic.
- Win rate: 33.19%.
- Profit Factor: 0.993.
- Expectancy: -0.0044R.
- Total: -127R.

This is a diagnostic only and is NOT an official profitability claim. It intentionally does not replace the full Decision Brain runtime.

## Important discovery

The raw stream is not uniformly bad. Existing governed context fields contain subsets with materially different outcome distributions.

A simple walk-forward discovery was performed:
- Discovery/calibration: 2016-2021.
- Untouched validation period: 2022-2024.
- Conditions were selected only from existing categorical evidence fields; no numeric threshold optimization was performed.
- Minimum calibration sample: 200 trades.

### Strongest repeatable candidates found

| Existing evidence condition | 2016-2021 trades | Train Exp R | Train PF | 2022-2024 trades | Test Exp R | Test PF |
|---|---:|---:|---:|---:|---:|---:|
| volatility_state=HIGH + mtf_context=strong_bearish | 256 | +0.359 | 1.657 | 190 | +0.405 | 1.762 |
| volatility_state=HIGH + H4_trend_regime=-1 | 281 | +0.260 | 1.448 | 282 | +0.287 | 1.503 |
| trend=BEAR_TREND + H4_trend_regime=1 | 250 | +0.164 | 1.268 | 231 | +0.260 | 1.448 |
| direction=SELL + volatility_state=HIGH | 401 | +0.249 | 1.427 | 347 | +0.210 | 1.353 |
| trend=BEAR_TREND + volatility_state=HIGH | 385 | +0.247 | 1.422 | 375 | +0.200 | 1.333 |
| trend=BULL_TREND + volatility_state=HIGH | 204 | +0.250 | 1.429 | 148 | +0.196 | 1.326 |
| volatility_state=HIGH + H4_trend_regime=1 | 212 | +0.316 | 1.563 | 141 | +0.191 | 1.318 |
| volatility_state=HIGH + D1_trend_regime=1 | 233 | +0.326 | 1.585 | 150 | +0.160 | 1.261 |

## Interpretation

The important result is not that one filter is now declared a production strategy. The important result is that the existing stack already contains **conditional edge candidates** without changing the book rules.

The first two candidates are especially interesting because they reproduce positive expectancy and PF > 1 in both the discovery period and the later 2022-2024 validation period with hundreds of trades.

This changes the engineering target:

**Do not keep trying to make the entire Murphy candidate stream profitable. Build the opportunity funnel so the existing evidence can identify which governed contexts deserve execution, then validate those contexts on untouched OOS data.**

## Required next gate

1. Preserve these candidates as discovery observations only.
2. Do NOT tune them on 2025.
3. Recover/verify the governed 2025 Murphy producer boundary.
4. Evaluate the frozen candidate definitions once on 2025 as untouched OOS.
5. If they survive, integrate them as an evidence-ranking/execution eligibility layer without changing Murphy/Nison semantics.
6. Apply the official cost/slippage contract and full Decision Brain runtime before any profitability claim.

## Governance

- 2025 remains OOS and read-only.
- No synthetic evidence.
- No rule semantic changes.
- Nison does not generate direction.
- Memory/Similarity does not generate direction.
- TIZ does not generate direction.
- Risk remains a hard gate.
- This report is analytical discovery, not a production strategy or profitability claim.
