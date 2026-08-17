# Nison First Batch Execution Report V1

Date: 2026-08-17
Branch: nison-batch-v1

## Scope
First implementation pass for the seven rules currently classified as BATCH_READY_CANDIDATE in NISON_44_BATCH_AUDIT_V1.

## Implemented shared evaluator contracts
- CANDLE_RULE_0012 Abandoned Baby: consumes approved `is_doji`, `gap_up`, `gap_down` primitives; no invented doji threshold.
- CANDLE_RULE_0021 Three Mountains: consumes a source-locked structure comparator; otherwise NOT_EVALUABLE.
- CANDLE_RULE_0023 Three Buddha Tops: consumes a source-locked structure comparator; otherwise NOT_EVALUABLE.
- CANDLE_RULE_0024 Three Buddha Bottoms: consumes a source-locked structure comparator; otherwise NOT_EVALUABLE.
- CANDLE_RULE_0034 Separating Lines: exact equal-open + opposite candle-color structure.
- CANDLE_RULE_0035 Tasuki Gap: consumes approved gap and close-gap primitives.
- CANDLE_RULE_0038 Windows: consumes approved gap-up/gap-down primitives.

## Unit test result
Local pytest run: 4 passed.

## Governance result
- No invented numeric thresholds.
- No Nison directional authority added.
- Qualitative comparators remain injectable/NOT_EVALUABLE until source-locked.
- This is evaluator/unit-test progress, NOT historical QA or Freeze.

## Next execution gate
Run these evaluators against the canonical OHLCV + Market Reader primitives. Then produce per-rule PASS/FAIL/NOT_EVALUABLE counts and availability/no-lookahead results. Historical QA and Freeze remain separate gates.
