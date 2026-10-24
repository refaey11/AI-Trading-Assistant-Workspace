# Multi-Pair Decision Brain — Execution Plan V1

## Purpose
Extend the existing project without rebuilding it. This document is a gated implementation plan, not a claim that multi-pair execution or profitability has already been verified.

## Initial scope
- XAUUSD
- EURUSD
- GBPUSD
- USDJPY
- USDCAD

## Current confirmed blockers
1. `BACKTEST/MTF_SIX_TF_SOURCE_ADAPTER_V1.py` declares `CANONICAL_SYMBOL = "GBPUSD"` and rejects other requested symbols. This adapter is not multi-pair ready.
2. `BACKTEST/EXECUTABLE_TRADING_ADAPTER_V1.py` is a separate EMA/RSI/ATR strategy adapter. Its outputs must not be represented as the full 34 Murphy + 44 Nison governed Decision Brain.
3. The existing GBPUSD adapter summary reports 2025 OOS profit factor 0.8684, expectancy -0.0917R and total -10R, with costs not applied. This is not evidence of live readiness.
4. Dropbox search confirmed likely source files by names/metadata for all five symbols, but complete schemas, data integrity, and runtime compatibility have not yet been validated.

## Required implementation gates
### Gate A — source inventory
For each symbol, resolve one canonical OHLC source and the relevant MTF/market-state sources. Record exact paths, headers, row counts, date coverage, duplicate timestamps, missing values, symbol identity and file hashes. Do not choose among duplicate candidates silently.

### Gate B — symbol-neutral adapters
Replace hard-coded symbol assumptions with an explicit validated symbol argument/configuration. Keep symbol identity in every report and trade output. Preserve strict source validation and fail closed on ambiguity.

### Gate C — Decision Brain integration
Route data into the existing governed brain and allowlist. Verify the 34 Murphy + 44 Nison rule governance, Trading in the Zone process gate, evidence-only historical/similarity memory, and hard Risk Engine gate. Do not substitute the EMA/RSI/ATR baseline for the governed brain.

### Gate D — deterministic tests
Run unit/schema tests and a small smoke test per symbol. Verify timestamps, no-lookahead/as-of joins, no duplicate bars, next-bar entry semantics, fail-closed intrabar ambiguity, and risk rejection behavior.

### Gate E — evaluation
Development: 2016–2024 only. Locked OOS: 2025 only, never used to tune. Include spread, commission, slippage and symbol-appropriate execution assumptions. Report each symbol independently and aggregate only after per-symbol reports pass validation.

## Acceptance criteria
- All five symbols pass source and schema validation.
- No hidden GBPUSD-only assumptions remain in the path being tested.
- The governed brain, rather than a proxy strategy, is proven to consume the intended evidence.
- Risk hard gate and evidence-only memory constraints have tests.
- 2025 remains locked and untouched during tuning.
- Reports state costs, exclusions, failures and unresolved data gaps.
- No live-readiness or profitability claim unless reproducible cost-inclusive results support it.

## Status at creation
- Branch created from current `main`.
- This plan is committed separately to avoid modifying or replacing existing engine code before tests identify the exact integration points.
- No runtime backtest was executed by this document.
