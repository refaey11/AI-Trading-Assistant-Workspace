# CORE PROFITABILITY EVAL RUN — 2026-08-23

## Status
EVALUATION_ONLY — diagnostic run, **not** an official 2025 baseline and **not** a canonical three-book result.

## Input
- 2025 GBPUSD fresh M1 source: 372,632 rows.
- Existing 2025 Murphy rule smoke stream: 55,944 rule evaluations.
- Existing assembled event timestamps: 6,225.
- Core-eval eligible timestamps after joining market state and requiring a single unambiguous Murphy directional confirmation: 2,688.
  - BUY: 1,411
  - SELL: 1,277
- Nison in the current assembled stream: NOT_EVALUABLE (no authoritative Nison evidence attached).
- TIZ: optional/unverified in this evaluation path.

## Frozen execution protocol used for this diagnostic
- Entry: event close.
- Stop: 0.75 ATR20.
- Target: 2R.
- Outcome horizon: 4 hours of subsequent M1 data.
- Same-bar ambiguity: none observed in this run.
- Costs/slippage: not applied.
- Concurrent-position portfolio rules: not modeled; outcomes are evaluated independently per event.

## Result
- Events evaluated: 2,688
- TP: 858
- SL: 1,550
- Timeout: 280
- Total R: +166R
- Profit factor (TP=+2R, SL=-1R): 1.1071
- TP hit rate: 31.92%
- Maximum sequential outcome drawdown: -40R

## Interpretation / governance
This is **not** the official Decision Brain profitability result. The upstream 2025 smoke stream currently covers only the currently available Murphy rule evaluations, not the full 78-rule Decision Brain runtime, and it carries no authoritative Nison evidence. The run therefore validates the isolated core-evaluation mechanics only; it must not be used for tuning, promoted to the official baseline, or represented as the final three-book backtest.

2025 remains OOS and evaluation-only.
