# Murphy 0034-0045 Semantic Compatibility Gate — 2026-08-25

## Decision
Do not mount Murphy 0034-0045 into the production Decision Brain runtime yet.

## Evidence
The preserved `MASTER_TRADING_RULES_V2.json` classifies all twelve rules 0034-0045 as `INCOMPLETE_NEEDS_RULE_DEFINITION` and `UNTESTED`.

The recovered `EXACT_MAPPING_V1.csv` tables provide intended feature/operator mappings, but several entries remain PARTIAL / NOT_EVALUABLE / NOT_YET_EVALUABLE and explicitly state that exact routing or indicator behavior must be inherited from approved modules rather than invented.

Examples of incompatibility or incompleteness:
- 0034 and 0035 have mapping-table conditions that differ from the canonical Master Trading Rules definitions. This is a semantic-version conflict, not a missing-code-only problem.
- 0036 requires verified Elliott Wave structure/territory evidence and is explicitly scoped in the source mapping to a stated stock cash-market framework; it must not be generalized to FX without an approved scope rule.
- 0037 has explicit 38.2%, 50%, and 61.8% source references, but the mapping says the existing Fibonacci module must first be verified.
- 0038 has no verified cycle-trough feature in the inspected project schemas.
- 0039 is primarily a process/evaluation principle and cannot generate market direction.
- 0040 requires a verified Parabolic SAR feature plus an approved regime gate; no invented threshold is permitted.
- 0041 requires an actual DMI/ADX feature; generic `trend_regime` is not an acceptable substitute.
- 0042-0045 are portfolio/risk constraints with explicit source values/ranges, but their instrument/account scope and compatibility with the existing Risk Engine must be reconciled before adoption.

## Historical implementation evidence
Historical Git checkpoints show that a dedicated 0034-0045 evaluator package once executed with 13 evaluator tests and 5 adapter tests. However, the implementation package itself is not present in the current main repository or the reconstructed 241-file workspace, and the historical checkpoint explicitly characterized it as a shared evaluator candidate rather than production-frozen.

## Governance outcome
- Runtime status remains `RECOVERED_NOT_MOUNTED` for 0034-0045.
- Missing/unverified evidence remains `NOT_EVALUABLE` / fail-closed.
- No new rule semantics, thresholds, confidence weights, or aggregation logic are introduced.
- 2025 remains OOS and must not be used for tuning.
- Official 2025 P&L remains blocked until 34/34 Murphy rules are source-backed, semantically reconciled, and runtime-tested.
