# Nison 0001–0010 Canonical Reconciliation Matrix

Date: 2026-08-22

## Source basis
- Canonical Nison closure/progress matrices from the project File Library.
- Current GitHub runtime and CircleCI validation.
- 2025 remains LOCKED OOS and is excluded from tuning/selection.

## Important interpretation
The canonical project state distinguishes frozen knowledge/source scopes from rule-level production closure. Therefore, “38 frozen candlestick pattern scopes” does not by itself mean every runtime evaluator is production-frozen.

## Rule matrix

| Rule | Pattern | Canonical source/contract | Existing artifact | Historical 2016–2024 | Availability / no-lookahead | Confirmation | Invalidation | Current production status |
|---|---|---|---|---|---|---|---|---|
| 0001 | Bullish Engulfing | SOURCE CONTRACT PRESENT | EXISTING_LIFECYCLE | PARTIAL — production replay reconciliation needed | PARTIAL — insufficient production-close evidence | EXPLICIT | EXPLICIT | NOT FROZEN |
| 0002 | Bearish Engulfing | SOURCE CONTRACT PRESENT | EXISTING_LIFECYCLE | PARTIAL — production replay reconciliation needed | PARTIAL — insufficient production-close evidence | EXPLICIT | EXPLICIT | NOT FROZEN |
| 0003 | Dark Cloud Cover | SOURCE CONTRACT PRESENT | REPLAY_EXISTS | PARTIAL — production replay reconciliation needed | PARTIAL — insufficient production-close evidence | EXPLICIT_BREAK | EXPLICIT | NOT FROZEN |
| 0004 | Piercing Pattern | SOURCE CONTRACT PRESENT | REPLAY_EXISTS | PARTIAL — production replay reconciliation needed | PARTIAL — insufficient production-close evidence | EXPLICIT_BREAK | EXPLICIT | NOT FROZEN |
| 0005 | On Neck | SOURCE CONTRACT PRESENT | REPLAY_EXISTS | PARTIAL — production replay reconciliation needed | PARTIAL — insufficient production-close evidence | DIRECTIONAL | EXPLICIT | NOT FROZEN |
| 0006 | In Neck | SOURCE CONTRACT PRESENT | REPLAY_EXISTS | PARTIAL — production replay reconciliation needed | PARTIAL — insufficient production-close evidence | DIRECTIONAL | EXPLICIT | NOT FROZEN |
| 0007 | Thrusting | SOURCE CONTRACT PRESENT | REPLAY_EXISTS | PARTIAL — production replay reconciliation needed | PARTIAL — insufficient production-close evidence | DIRECTIONAL | EXPLICIT | NOT FROZEN |
| 0008 | Morning Star | SOURCE CONTRACT PRESENT | REPLAY_EXISTS | PARTIAL — production replay reconciliation needed | PARTIAL — insufficient production-close evidence | DIRECTIONAL | ALTERNATIVE | NOT FROZEN |
| 0009 | Evening Star | SOURCE CONTRACT PRESENT | REPLAY_EXISTS | PARTIAL — production replay reconciliation needed | PARTIAL — insufficient production-close evidence | DIRECTIONAL | ALTERNATIVE | NOT FROZEN |
| 0010 | Morning Doji Star | SOURCE CONTRACT PRESENT | REPLAY_EXISTS | PARTIAL — production replay reconciliation needed | PARTIAL — insufficient production-close evidence | DIRECTIONAL | ALTERNATIVE | NOT FROZEN |

## Runtime/CI status
- Current GitHub runtime exists for 0001–0010.
- CircleCI Run #10 passed after confirmation-gate integration and smoke-test correction.
- CI PASS is runtime/structural validation only; it does not close historical, availability/no-lookahead, provenance, or production-freeze gates.

## Required next closure sequence
1. Reconcile each runtime evaluator against the canonical source contract.
2. Reconcile confirmation and invalidation semantics without inventing thresholds/operators.
3. Execute complete 2016–2024 replay/QA using canonical historical data.
4. Execute timestamp availability and no-lookahead checks.
5. Verify 2025 remains untouched and outside tuning/selection.
6. Only then issue a rule-level production freeze manifest.

## Governance
Do not rebuild already-existing project knowledge. Audit and integrate existing artifacts first. Do not promote an evaluator to production from field presence or CI success alone. Nison remains confirmation/context evidence and not a standalone directional decision maker.
