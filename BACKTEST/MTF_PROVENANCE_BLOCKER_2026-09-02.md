# MTF Provenance Blocker — 2026-09-02

## Purpose
Freeze the current finding before any 2016-2024 profitability run.

## Finding
The legacy `AI_Trading_Assistant_MULTI_TIMEFRAME_READER_V1` is explicitly `RESEARCH_ONLY` and only covers `H4` and `H1`. Its contract states that `M15` is not implemented and must not be fabricated from H1. Therefore it cannot serve as the canonical source for the current six-timeframe Decision Brain contract.

## Current six-timeframe contract
The development replay expects source-backed numeric fields:
- `mtf_trend_score`
- `M5_trend_regime`
- `M15_trend_regime`
- `M30_trend_regime`
- `H1_trend_regime`
- `H4_trend_regime`
- `D1_trend_regime`

## Blocker
The current V5.4 workflow contains an inline mapping from categorical regime tokens (`BULL_TREND`, `BEAR_TREND`, `TRANSITION`, etc.) to numeric values. That mapping is not proven to be the original producer's canonical encoding and therefore cannot be treated as source-backed Decision Brain input provenance.

## Required resolution
Before profitability testing, identify or recover the exact producer/serialized feature contract for the six-TF numeric Brain inputs, including:
1. exact field order;
2. raw-to-feature semantics;
3. categorical-to-numeric encoding, if any;
4. missing-value/imputation policy;
5. scaling/normalization policy, if any;
6. producer lineage and source file lineage;
7. timestamp/as-of semantics.

If the exact producer contract is found and compatible, wire by selection/rename only. If it is not found, the MTF-to-Brain path remains `NOT_EVALUABLE` and the 2016-2024 profitability run must not be declared canonical.

## Guardrail
No change to Decision Brain V1. No change to Murphy/Nison semantics. No tuning. 2025 remains OOS and locked.
