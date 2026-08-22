# Execution Engine Compatibility Gate — 2026-08-23

## Finding
The existing Dropbox backtest artifacts include multiple execution contracts and they are not interchangeable.

### Existing legacy/Core backtest contract
`AI_Trading_Assistant_FULL_PROJECT_V1/AI_Trading_Assistant_CORE_V1/backtest/CONTRACT.json` specifies:
- quality gate: >=7
- stop: 2 ATR
- target: 1.5R
- cost: 2 pip round-trip stress
- live_execution: false

### Existing integrated-engine prototype
`ENGINE_AUDIT/AI_Trading_Assistant_INTEGRATED_ENGINE_V1/engine/ENGINE_CONTRACT_V1.json` specifies a prototype risk placeholder of 1% per trade and 1.5R target. Its README explicitly says the engine is an engineering prototype and NOT validated performance.

### Current candidate baseline execution protocol
`AUDITS/SL_TP_CANONICAL_GATE_2026-08-23.md` records the current frozen candidate baseline protocol for Similarity V2 + 4H as:
- threshold 0.52
- SL 0.75 ATR
- TP 2R
This candidate baseline is still NOT OFFICIAL until the uniform end-to-end walk-forward and leakage audit pass.

## Gate decision
Do NOT run 2025 profitability through the legacy 2 ATR / 1.5R engine contract or the integrated prototype contract. Doing so would change execution semantics and invalidate attribution to the frozen Decision Brain path.

## Required next implementation
Add a narrow execution adapter that:
1. consumes only the frozen Decision-Event schema;
2. applies the candidate baseline execution protocol consistently (0.75 ATR stop + 2R target) without changing Decision Brain direction logic;
3. preserves cost/ambiguity policy as an explicit contract input;
4. fails closed on missing entry/exit evidence;
5. emits immutable execution outcomes for Final Backtest metrics.

## OOS boundary
2025 remains evaluation-only. No parameter tuning, threshold selection, SL/TP optimization, or execution-policy selection may use 2025.
