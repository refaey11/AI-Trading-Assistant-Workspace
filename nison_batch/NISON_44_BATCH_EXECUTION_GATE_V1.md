# NISON 44-RULE BATCH — EXECUTION GATE V1

Date: 2026-08-17
Branch: nison-batch-v1

## Purpose
Run the 44 Nison rules as one governed batch without inventing source semantics or changing the Decision Brain contract.

## Current batch state
- 31 rules: BATCH_MAPPED
- 7 rules: CANDIDATE / require Market Reader primitives or source-locked comparator
- 2 rules: SOURCE_BLOCKED (0033, 0036)
- 1 rule: SOURCE_BLOCKED (0037) — qualitative comparator
- 6 rules: CONTEXT_GATE (0039–0044)
- 3 rules in the candidate set with existing evaluator work (0035–0038 subset; 0034 also has a deterministic evaluator contract)

## Execution policy
1. BATCH_MAPPED rules may enter deterministic contract-test generation when their required shared operators are implemented.
2. CANDIDATE rules enter execution only when their declared Market Reader primitives are available.
3. SOURCE_BLOCKED rules remain NOT_EVALUABLE; no arbitrary thresholds are allowed.
4. CONTEXT_GATE rules are evaluated as contextual evidence/gates, not candle pattern recognizers.
5. Nison output remains confirmation-only and cannot create direction.
6. 2025 remains OOS and cannot be used for tuning.
7. Historical QA is required before Freeze.

## Required final evidence per rule
rule_id, evaluator_version, source_reference, input_schema, output_state, reason, no_lookahead_check, historical_QA_status, freeze_status.

## Next execution action
Connect the mapped operator groups to the existing Market Reader primitives and run the deterministic contract suite across all 44 rule IDs. Do not mark PASS/FREEZE merely because a rule is BATCH_MAPPED.