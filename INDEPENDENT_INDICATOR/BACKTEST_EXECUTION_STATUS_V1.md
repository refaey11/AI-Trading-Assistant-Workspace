# Independent Murphy-Nison Indicator — Backtest Execution Status V1

## Scope
- Branch: `prototype/independent-murphy-nison-indicator-v1`
- Development window: 2016–2024
- OOS window: 2025 (reserved; no tuning)
- Data source: governed GBPUSD HISTDATA M1 archives in Dropbox
- Comparison: Baseline / Murphy-only / Murphy+Nison / Layered V1
- Metrics: trades, win rate, profit factor, expectancy, Net R, max drawdown, avg win/loss, no-trade rate

## Data inventory verified
Dropbox contains GBPUSD M1 archives including 2017–2025 and the project workspace contains the backtest runner, six-timeframe source adapter, and existing GitHub Actions workflows for the governed 2016–2024 backtest.

## Execution state
The independent comparison is prepared for execution, but this commit does not claim numerical backtest results. Raw Dropbox ZIP bytes are not directly mounted into the current execution runtime through the connector. Existing historical backtest outputs are not reused as results for the new independent indicator.

## Guardrails
- No lookahead.
- Higher-timeframe confirmation must use closed data / lookahead off.
- 2025 is OOS and must not be used for parameter tuning.
- Do not modify the main Decision Brain or reopen frozen Murphy/Nison work.
- Any result must identify exact data source, period, costs, and strategy version.

## Next execution step
Run the existing backtest runner against the verified GBPUSD raw M1 archives, aggregate required timeframes, then produce the four-system comparison table and 2025 OOS holdout report.
