# Development Backtest Execution Checkpoint — 2026-08-27

## Current truth
- The latest verified CI run confirms the pushed Nison-development workflow itself completed successfully, but that workflow is a governance/test workflow, not the profitability backtest.
- The repository currently has a BACKTEST readiness specification, but no verified end-to-end runner that executes the current 34 Murphy + 44 Nison stack through the Decision Brain and produces audited P&L/Win Rate/Profit Factor/Drawdown metrics for 2016–2024.
- Therefore no final profitability result is claimed yet.

## Next execution target
Build/run the actual development backtest path using existing contracts only:
GBPUSD H1 2016–2024 -> current Murphy evidence + current Nison evidence -> governed 78-rule event stream -> Decision Brain -> Three-Book Decision -> Risk/Execution -> bar-level trade simulation -> audited performance metrics.

## Governance locks
- Development window: 2016–2024.
- 2025 is OOS/evaluation-only and must not be used for tuning or calibration.
- Murphy remains the directional context source.
- Nison remains confirmation/contradiction only.
- Similarity/Historical Memory remain evidence only and cannot create direction.
- TIZ remains process/psychology context; do not invent directional logic from it.
- Risk remains a hard execution gate.
- Do not rebuild or alter existing rule semantics just to increase trade count.
- Do not use legacy 2016–2018 profitability artifacts as the result for the current 78-rule system.

## Acceptance requirements before profitability claim
- Unified timestamped 2016–2024 event stream.
- Explicit as-of / no-lookahead checks.
- Memory candidate availability/lookahead audit.
- Explicit MTF consumption audit.
- Execution funnel from eligible event -> executable decision -> executed trade.
- Frozen transaction-cost/slippage contract applied.
- Reproducible artifact + manifest stored.

## Status
EXECUTION_TARGET_DEFINED — proceed to the real 2016–2024 backtest runner; do not stop at readiness or governance tests.
