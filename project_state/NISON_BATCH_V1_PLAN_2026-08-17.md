# NISON BATCH V1 — 2026-08-17

## Objective
Process the 44 Steve Nison confirmation rules as one batch without rebuilding existing project knowledge and without inventing source semantics.

## Rule inventory
- 44 Nison rules are present in `INTEGRATED_RULE_REGISTRY_V1.json`.
- Rule IDs are `CANDLE_RULE_0001` through `CANDLE_RULE_0044`.
- Integration role: `confirmation`.

## Shared operator layer
The batch is mapped onto reusable operators instead of one bespoke evaluator per rule:
- `trend_context`
- `candle_count`
- `candle_color`
- `open_relation`
- `close_relation`
- `body_geometry`
- `high_low_relation`
- `window_gap`
- `support_resistance`
- `swing_structure`
- `candle_sequence`
- `confirmation_state`

## Evaluator contract
Every rule must resolve to exactly one of:
- `PASS`
- `FAIL`
- `NOT_EVALUABLE`

`NOT_EVALUABLE` is not converted into a guess. It carries the blocking reason and remains neutral at the Decision Brain boundary.

## Critical source-locked blockers
- `CANDLE_RULE_0035` Tasuki Gap: source supports partial retracement/window remaining open, but no arbitrary numeric tolerance may be invented.
- `CANDLE_RULE_0036` Gapping Play: strong directional move and successful Window test are qualitative and require source-locked operationalization.
- `CANDLE_RULE_0037` Side-by-Side White Lines: source says approximately same open and similar body size; no invented numeric comparator.
- `CANDLE_RULE_0033` Advance Block: stalled/difficulty language is qualitative and needs source-locked operationalization.
- `CANDLE_RULE_0039`–`0044`: these are methodology/confluence/context concepts, not standalone candle recognizers; they must become contextual evidence rather than fabricated candle triggers.

## Existing work to reuse
Rules `0035`–`0038` already have evaluator/test work in the workspace. This batch must extend/reconcile that work rather than replace it.

## Safety invariants
1. Nison remains confirmation-only.
2. Nison evidence cannot create direction.
3. No lookahead.
4. No tuning on 2025 OOS.
5. No invented numeric thresholds where the source is qualitative.
6. Existing frozen artifacts are not rewritten.

## Next execution stage
Build the shared operator contract and batch evaluator matrix for all 44 rules, then run deterministic unit/contract tests and isolate only the genuinely source-blocked rules for review.
