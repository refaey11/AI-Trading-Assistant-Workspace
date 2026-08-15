# Murphy Shared Point & Figure Feature Contract V1

Status: DRAFT / PRE-FREEZE
Date: 2026-08-15

## Purpose

Provide one shared Point & Figure evidence layer for Murphy rules 0030-0032. This is a feature contract, not a trading rule and not a tuning artifact.

## Source-faithful semantics currently established

- MURPHY_0030 identity: P&F bullish support.
- P&F structure uses X/O columns.
- Murphy describes 3-box reversal construction using High/Low.
- Bullish Support Line is a structural 45-degree guide rising from the low of the lowest O-column; price above it represents bullish major-trend context.
- Murphy/Chapter 11 discusses multiple box-size/scaling choices and does not provide a GBPUSD-specific deterministic box-size value or a complete reproducible Kenneth Tower screening formula in the audited text.

## Non-negotiable governance

1. Do not choose box size by backtest performance.
2. Do not use 2025 for parameter selection or tuning.
3. Do not silently substitute ATR, pips, percentage, or another scaling method and label it as Murphy source semantics.
4. Any construction parameter not directly supported by the source must be explicitly labeled as project operationalization and frozen before historical evaluation.
5. Availability and chronology must be testable; no future-bar information may enter a P&F state.
6. A shared P&F engine may be reused by 0030-0032, but each rule retains its own semantic/operator contract.

## Current status

- Shared P&F feature candidate: FOUND externally.
- Internal approved P&F construction contract: NOT YET FROZEN.
- MURPHY_0030: blocked at construction-contract boundary.
- Do not advance 0030 to evaluator freeze until the construction contract is approved.

## Next gate

Resolve box-size/scaling and timeframe/sampling policy from an authoritative, reproducible source or an explicitly approved project operationalization. Then run deterministic/no-lookahead harness before rule-specific evaluation.
