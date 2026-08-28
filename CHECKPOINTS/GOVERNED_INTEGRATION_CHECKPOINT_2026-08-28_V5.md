# Governed Integration Checkpoint V5 — 2026-08-28

Branch: `backtest-only-2026-08-28`

## Current state

- Development window: 2016–2024 only.
- 2025: LOCKED / OOS.
- Decision Brain V1: reused unchanged.
- Murphy semantics: unchanged; canonical source-backed fan-in preserved.
- Nison semantics: confirmation / contradiction only.
- Historical Context Memory: evidence-only.
- Historical Outcome Memory: evidence-only.
- Similarity V2: historical evidence only; cannot generate direction.
- Context-Aware Retrieval V2: context/interpretation only; cannot generate direction.
- TIZ: process-only boundary; missing process evidence => NOT_EVALUABLE; no direction generation.
- Risk: hard gate; missing execution inputs rejected; no synthetic SL/TP/ATR/equity.

## Critical fixes now in branch

1. Nison canonical compiler is bounded-memory/streaming and preserves multi-rule timestamps.
2. Nison source hashing is incremental rather than whole-file `read_bytes()`.
3. Governed workflow is manual-dispatch only; no push-triggered governed backtest.
4. Gate and full backtest are separately selectable, with the full backtest guarded by an explicit `status == PASS` assertion.

## Required sequence from here

`Real source acquisition`
`→ Murphy canonical stream`
`→ Nison canonical stream`
`→ Integration Gate V4`
`→ PASS`
`→ 2016–2024 Backtest`

No full backtest should run before the Integration Gate returns PASS.

## Not claimed

- No Integration Gate PASS has been claimed in this checkpoint.
- No 2016–2024 full backtest run has been claimed.
- No 2025 data has been used for tuning.
