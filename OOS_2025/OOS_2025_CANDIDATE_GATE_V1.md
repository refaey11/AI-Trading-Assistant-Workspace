# OOS 2025 Candidate Gate V1

Status: FROZEN / EVALUATION-ONLY

## Purpose
Evaluate only the three candidates frozen from 2016-2024 discovery against untouched 2025 OOS evidence. This gate does not select, tune, or optimize candidates.

## Frozen candidates
1. HIGH volatility + strong_bearish MTF
2. HIGH volatility + H4_trend_regime=-1
3. SELL + HIGH volatility

## Required evidence
- 2025 Murphy producer evidence
- 2025 GBPUSD H1/M1 price source
- as-of market-state context
- as-of MTF context including H4
- frozen execution geometry: 0.75 ATR stop / 2R target

## Hard rules
- 2025 is OOS and cannot be used for tuning.
- Candidate definitions are immutable during this evaluation.
- No numeric threshold search.
- No semantic changes to Murphy/Nison/TIZ.
- Nison does not generate direction; an opposite directional PASS may reject a setup when authoritative Nison evidence exists.
- Missing authoritative evidence is NOT_EVALUABLE, not a failure and not an inferred value.
- No profitability claim until lookahead, execution, and evidence provenance gates pass.

## Acceptance output
For each candidate report: events, evaluated, TP, SL, ambiguous/timeout/open, win rate, expectancy R, profit factor, total R, drawdown, and year-independent diagnostics. Report PASS/FAIL/NOT_EVALUABLE separately from profitability.

## Current known 2025 evidence
Dropbox contains `MURPHY_2025_FULL_EVIDENCE.csv` and multiple 2025 Murphy candidate streams. Existing project preflight also confirms 2025 price data and Murphy smoke evaluations, but its canonical three-book path was blocked by missing authoritative Nison/TIZ/Risk maps. Therefore this gate must not relabel the prior +166R diagnostic as an official Decision Brain result.
