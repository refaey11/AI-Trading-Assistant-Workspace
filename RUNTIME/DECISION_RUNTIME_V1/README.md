# Decision Runtime V1

Purpose: provide one canonical event-driven orchestration boundary over the existing governed modules without rewriting their semantics.

## Flow

MARKET SNAPSHOT -> EXISTING EVIDENCE ADAPTERS -> DECISION BRAIN -> THREE-BOOK GATE -> EXECUTION PLAN

This runtime does not create new book-rule semantics. It normalizes existing outputs and fails closed on missing/incompatible evidence.

## Modes

- BACKTEST: deterministic replay of historical snapshots.
- PAPER: live market data with no broker order.
- DEMO: MT5 demo execution.
- LIVE: MT5 real execution, only after paper/demo validation.

## Initial implementation scope

GBPUSD first. Existing Murphy/Nison/TIZ/Similarity/Market/Risk components remain source-of-truth. The runtime owns orchestration, event identity, provenance, and mode selection.
