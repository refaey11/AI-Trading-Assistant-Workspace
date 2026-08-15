# Murphy 0021–0023 — Canonical Rule Adapter Compatibility Matrix V1
Date: 2026-08-15
Status: COMPATIBILITY AUDIT COMPLETE — INTEGRATION NOT YET FROZEN

## Source basis
- Workspace `024/rule_adapter.py` is the current adapter implementation.
- Workspace `025/rule_adapter_contract_v1.json` is the adapter contract.
- PR #4 on GitHub contains the 0021–0023 lossless evaluator-result boundary and its deterministic test evidence.
- Project compatibility audit V1 identifies adapter contract gaps that are broader than 0021–0023.

## Matrix
| Contract item | Existing adapter | 0021–0023 evaluator boundary | Result |
|---|---|---|---|
| source_rule_id | present | preserved | PASS |
| statement | present | reason/name available upstream | COMPATIBILITY INPUT, not direct mapping yet |
| direction | derived from registry text | evaluator may supply directional_confirmation | GAP — cannot silently equate these |
| strength | synthesized conservatively | not supplied by evaluator | GAP — must not infer from evaluator |
| available | present | availability semantics supplied when present | COMPATIBLE, needs explicit mapping |
| gate | pass/fail/needs_review | evaluator has PASS/FAIL/NOT_EVALUABLE | GAP — direct field mapping is explicitly prohibited |
| conflict | present | not supplied | GAP — do not infer |
| decision_hint | contract requires it | not in current implementation | GLOBAL CONTRACT GAP |
| confidence_delta | contract requires bounded adjustment | not in current implementation | GLOBAL CONTRACT GAP |
| current_market_state | accepted by function signature but unused | not evaluator-owned | GLOBAL CONTRACT GAP; do not claim state-aware normalization |

## Critical decision
Do NOT implement `gate = evaluator.status`.
Do NOT convert `NOT_EVALUABLE` to `needs_review`, `fail`, or `pass` without an approved canonical contract.
Do NOT infer strength, conflict, direction, decision_hint, or confidence_delta from missing evaluator fields.

## What is already proven
The lossless boundary preserves evaluator fields without semantic mapping and has independent deterministic evidence of 6/6 checks passing. This is boundary validation only, not canonical adapter integration.

## What remains
1. Approve an explicit canonical mapping for evaluator result -> Decision Brain evidence.
2. Implement only that approved mapping in the existing adapter layer.
3. Add repository-native deterministic tests.
4. Reconcile the mapped outputs against the existing 122,943-row independent evaluator result set with zero mismatches.
5. Run availability/no-lookahead reconciliation.
6. Issue a final freeze manifest only after all gates pass.

## Governance
- Do not rebuild the Rule Adapter.
- Do not change 0021/0022/0023 semantics.
- Do not add thresholds, lookbacks, OI proxies, or new timeframes.
- 2025 remains OOS and is excluded from tuning/selection.
- This matrix does not grant Production Freeze.
