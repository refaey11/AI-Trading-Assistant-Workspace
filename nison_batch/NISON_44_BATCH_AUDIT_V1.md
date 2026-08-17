# Nison 44-Rule Batch Audit V1

## Scope
All 44 Steve Nison confirmation rules. This batch layer does not rewrite the registry and does not give Nison directional authority.

## Governance
- Nison = confirmation only.
- No rule may create direction by itself.
- No invented numeric thresholds/operators.
- Qualitative source language remains NOT_EVALUABLE until an approved comparator exists.
- 2025 is OOS and excluded from tuning/selection.
- Existing evaluators/artifacts are reused; no rebuild from scratch.

## Batch states
Each rule must resolve through: SOURCE_LOCKED -> OPERATOR_READY -> EVALUATOR_READY -> UNIT_TESTED -> HISTORICAL_QA -> AVAILABILITY/NO_LOOKAHEAD -> FREEZE.
A blocker in one rule does not stop independent rules.

## Known existing Nison batch artifacts
0035 Tasuki Gap: evaluator + unit tests exist; canonical body-size comparator remains unresolved.
0036 Gapping Play: structural evaluator + unit tests exist; qualitative sharpness/small-body/congestion/near-high-low definitions remain unresolved.
0037 Side-by-Side White Lines: structural evaluator + unit tests exist; same-open/similar-body comparators remain unresolved.
0038 Windows: deterministic structural evaluator exists; 2016-2024 replay found 6 windows (2 bullish, 4 bearish) with zero availability violations; freeze still requires compatibility sign-off and manifest.

## Current batch verdict
NOT_READY_TO_FREEZE.

Reason: the repository/file-library evidence supports partial execution for 0035-0038, but the full 44-rule batch does not yet have source-locked operators/evaluators and executable historical data access for a complete run.

## Next batch execution
1. Build the 44-rule source/operator matrix from the canonical registry.
2. Reuse shared candle/window/context primitives.
3. Generate rule-specific evaluator contracts only where source semantics are deterministic.
4. Mark qualitative/undefined rules NOT_EVALUABLE rather than inventing thresholds.
5. Run unit tests in parallel.
6. Run 2016-2024 historical QA where runtime data is available.
7. Run availability/no-lookahead audits.
8. Produce one consolidated freeze manifest; do not merge/freeze unless all required gates pass.
