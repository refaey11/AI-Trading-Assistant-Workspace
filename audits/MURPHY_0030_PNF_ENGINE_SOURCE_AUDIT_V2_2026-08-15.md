# Murphy 0030 P&F Engine Source Audit V2

Status: BLOCKED / PRE-IMPLEMENTATION
Date: 2026-08-15

## Source inspected
Candidate engine: gregorian-09/pnf-chart-system, `sources/pnf/chart.cpp` and `headers/pnf/chart.hpp`.

## Confirmed capabilities
- `ChartConfig` supports `ConstructionMethod`, `BoxSizeMethod`, and reversal; default reversal is 3.
- `add_data(high, low, close, time)` dispatches to HighLow construction when configured.
- Engine exposes X/O column state and prices.

## Critical compatibility findings
1. **Box-size semantics are engine-specific.** Percentage scaling is `price * box_size / 100`; Traditional scaling mutates `config_.box_size` based on price bands. This cannot be labeled Murphy without separate source approval.
2. **High/Low reversal ordering is not source-neutral.** `process_high_low()` tests reversal using the high and low, but if either triggers it selects the high-trigger path when `reversal_high || reversal_low` is true. The code does not encode a documented within-bar path policy. For D1 OHLC, the order in which high and low occurred is not present in the input. This is a construction-policy gap, not a Murphy rule decision.
3. **Reversal box size can differ from the box used earlier in the same bar.** `process_high_low()` first calculates a box from `high`, while `is_reversal()` recalculates a box from the tested price. This is especially material for Percentage scaling.
4. **Trendline semantics must not be inherited.** The engine's TrendLineManager uses its own significant-low/high heuristics, lookback, touch tolerance, and break buffer. These are engine behavior, not automatically Murphy semantics.

## Decision
Do not integrate the engine as a production Murphy implementation yet.

Reuse is still preferred, but only behind the project semantic adapter and only after the construction-policy gaps are explicitly resolved.

## Required next gate
Resolve the High/Low within-bar ordering policy and Box Size policy from source evidence or explicitly approved project operationalization. Then run deterministic/prefix/no-lookahead tests. Do not use backtest performance or 2025 to choose construction parameters.
