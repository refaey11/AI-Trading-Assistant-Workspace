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
The execution workflow has now been added under `.github/workflows/independent-murphy-nison-backtest.yml`. It is designed to acquire the governed H1, Murphy, Nison, and market-state inputs from Dropbox using the existing repository secret and execute the existing independent runner. No numerical result is claimed until the workflow completes and its artifact is inspected.

## Guardrails
- No lookahead.
- Higher-timeframe confirmation must use closed data / lookahead off.
- 2025 is OOS and must not be used for parameter tuning.
- Do not modify the main Decision Brain or reopen frozen Murphy/Nison work.
- Any result must identify exact data source, period, costs, and strategy version.

## Next execution step
Inspect the newly triggered GitHub Actions run and its artifact. If the runner is blocked by source schema or secret availability, fix only that blocker; do not rebuild the project.
