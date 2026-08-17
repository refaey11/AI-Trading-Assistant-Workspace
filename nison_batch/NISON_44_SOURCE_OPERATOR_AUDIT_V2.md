# Nison 44 — Source/Operator Audit V2

Date: 2026-08-17
Branch: nison-batch-v1

## What was actually inspected
- `AI_Trading_Assistant_MASTER_KB_V1.zip`
- `AI_Trading_Assistant_TRADING_RULES_V2.zip`
- `AI_Trading_Assistant_NISON_CANDLE_CONFIRMATION_V1.zip`
- `AI_Trading_Assistant_NISON_CONTEXT_ENGINE_V1.zip`

The canonical Nison registry was cross-checked against the Master KB formation-rule files. This is an audit artifact, not a freeze declaration.

## Result
- 44 Nison rules found in `MASTER_TRADING_RULES_V2.json`.
- 38 rules have a directly matched Master KB `02_Formation_Rules` source file.
- 6 rules (0039–0044) are context/technique entries rather than individual candlestick formation files.
- Of the 38 formation rules, 33 contain qualitative language that requires either an approved project comparator or a `NOT_EVALUABLE` boundary.
- 5 formation rules have no qualitative token detected in their formation-rule text: 0021 Three Mountains, 0023 Three Buddha Tops, 0024 Three Buddha Bottoms, 0034 Separating Lines, and 0035 Tasuki Gap. This does NOT mean they are frozen; confirmation/context and other gates still apply.

## Existing implementation audit
The existing `NISON_CANDLE_CONFIRMATION_V1` package contains only 9 operational patterns and explicitly says its definitions are engineering prototypes, not exact Steve Nison canonical criteria. Therefore it must be reused only where compatible and must not be promoted wholesale to canonical Nison logic.

## Existing 0035–0038 artifacts
0035–0038 already have dedicated evaluators/tests and historical QA artifacts. Reuse them; do not rebuild them. Their unresolved source/contract boundaries remain governed by their existing reports.

## Canonical governance
- Nison = confirmation only; it cannot create market direction by itself.
- No invented thresholds/tolerances/timeframes.
- Qualitative source language is not converted into backtest-tuned numbers.
- Missing/unsupported required evidence returns `NOT_EVALUABLE`.
- 2025 remains OOS and is not used for tuning, selection, or operator choice.
- Unit tests do not equal production freeze.

## Immediate batch execution targets
1. Build/reuse shared candle primitives for the 38 formation rules.
2. Bind source-backed exact conditions first.
3. Mark qualitative clauses explicitly as unresolved rather than guessing.
4. Treat 0039–0044 as context gates, not candle recognizers.
5. Run deterministic contract tests before any historical QA.
6. Run 2016–2024 historical QA only for rules whose required inputs are fully source/contract locked.

## Important
This audit corrects the previous assumption that the Nison project lacked source-level formation material. The Master KB contains formation-rule files for the core Nison pattern set. The remaining problem is operationalization of qualitative clauses and confirmation/context contracts, not absence of the book material.