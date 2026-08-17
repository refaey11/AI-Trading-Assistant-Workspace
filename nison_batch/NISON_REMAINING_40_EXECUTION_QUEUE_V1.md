# Nison Remaining 40 — Execution Queue V1
Date: 2026-08-17

## Objective
Process the remaining Nison rules as a batch, reusing existing candle/context primitives and preserving source semantics.

## Rules in scope
CANDLE_RULE_0001–CANDLE_RULE_0034 and CANDLE_RULE_0039–CANDLE_RULE_0044, excluding 0035–0038 whose existing replay/evaluator artifacts are already audited separately.

## Execution lanes
### Lane A — deterministic candle geometry/sequence
0001–0011, 0013–0020, 0022, 0025–0032, 0034.

### Lane B — Market Reader dependent
0021, 0023, 0024, 0038 already has prior replay evidence; reuse rather than rebuild.

### Lane C — source blocked
0033, 0036, 0037 remain NOT_EVALUABLE where canonical operational definitions are absent. Do not infer numeric thresholds.

### Lane D — context gates
0039–0044 are evaluated as contextual confirmation gates, not standalone candle recognizers.

## Required output for each rule
- source reference
- operator contract
- evaluator status
- deterministic test status
- historical QA status
- no-lookahead status
- final state: PASS / FAIL / NOT_EVALUABLE
- freeze eligibility

## Governance
- Nison is confirmation-only and cannot create trade direction.
- 2025 remains OOS and is excluded from tuning.
- No invented thresholds, tolerances, or timeframes.
- Existing artifacts must be reused and reconciled before creating replacements.

## Immediate action
Build the shared deterministic contract matrix for Lane A first, then feed those contracts into the existing evaluator/test framework. This is an execution queue, not a declaration of completion.