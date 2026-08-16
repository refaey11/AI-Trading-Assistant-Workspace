# Nison 0008–0015 Execution Gate V1

## Scope
This batch records a fail-closed source contract gate for rules 0008–0015 using only clauses present in the integrated Nison registry.

## Rule states
- 0008 Morning Star: PARTIAL_EXISTING_ENGINE; 3 candles + downtrend are source-declared, but exact pattern operator and confirmation mapping remain open.
- 0009 Evening Star: PARTIAL_EXISTING_ENGINE; 3 candles + uptrend are source-declared, but exact pattern operator and confirmation mapping remain open.
- 0010 Morning Doji Star: NO_APPROVED_CANONICAL_OPERATOR_FOUND; doji/pattern operator not source-locked in the current approved infrastructure.
- 0011 Evening Doji Star: NO_APPROVED_CANONICAL_OPERATOR_FOUND; doji/pattern operator not source-locked in the current approved infrastructure.
- 0012 Abandoned Baby: NO_APPROVED_CANONICAL_OPERATOR_FOUND; gap/doji/pattern operator not source-locked in the current approved infrastructure.
- 0013 Harami: PARTIAL_EXISTING_ENGINE; 2 candles + prior long body + second small body inside prior body are source-declared, but no approved source-bounded size/containment comparator is available in this gate.
- 0014 Harami Cross: NO_APPROVED_CANONICAL_OPERATOR_FOUND; doji comparator not source-locked in the current approved infrastructure.
- 0015 Tweezers Top: NO_APPROVED_CANONICAL_OPERATOR_FOUND; top/equality comparator not source-locked in the current approved infrastructure.

## Implementation rule
The new gate validates only source-declared candle count and trend context. If those clauses pass but the pattern operator is unresolved, the result is `NOT_EVALUABLE`. No numeric threshold, tolerance, lookback, scoring, proxy, or direction generation is introduced.

## Tests
9 deterministic tests added:
- 8 fail-closed checks for unresolved operators.
- 2 wrong-context rejection checks (combined in one test).

## Governance
- Nison remains confirmation-only.
- 2025 remains OOS and excluded from tuning/selection/calibration/optimization.
- Unit tests do not grant production freeze.
- Historical QA and availability/no-lookahead remain blocked until the complete evaluator contract is closed.
