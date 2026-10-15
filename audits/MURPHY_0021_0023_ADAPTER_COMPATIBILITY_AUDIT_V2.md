# Murphy 0021–0023 — Rule Adapter Compatibility Audit V2

Date: 2026-08-13
Scope: 0021–0023 only
Status: COMPATIBILITY GAP IDENTIFIED — NO PRODUCTION CHANGE

## Sources inspected
- Existing Rule Adapter contract: `025/rule_adapter_contract_v1.json`
- Existing Rule Adapter implementation: `024/rule_adapter.py`
- Existing project handoffs and 0021–0023 evaluator status artifacts
- PR #4 evaluator-to-adapter contract proposal

## Finding
The canonical Rule Adapter currently consumes registry-rule inputs, current market state, and optional historical-memory inputs. Its declared inputs do not include an evaluator result.

The implementation normalizes registry-rule metadata (`rule_id`, source, original rule, setup/conditions, decision, trade plan, risk) into `NormalizedEvidence`. It derives direction from the registry rule and computes a conservative strength. It does not consume an evaluator result containing PASS/FAIL/NOT_EVALUABLE.

Therefore the existing Adapter cannot yet be claimed to provide an `EvaluatorResult -> NormalizedEvidence` integration for Murphy 0021–0023.

## Existing contract constraints
The adapter contract is `DESIGN_ONLY` and explicitly says the adapter normalizes book-rule outputs, does not duplicate source rules, and does not decide trades. Murphy remains technical context; Nison confirmation; Trading in the Zone process gate; Similarity historical evidence; Risk hard gate.

## Required boundary
The missing boundary is an interface, not a new adapter:

`Existing 0021–0023 Evaluator Result -> Adapter normalization boundary -> Decision Brain evidence`

The boundary must preserve, without recomputation:
- rule_id
- PASS / FAIL / NOT_EVALUABLE status
- directional_confirmation when supplied
- availability semantics
- source attribution

`NOT_EVALUABLE` must remain unavailable/needs-review and must never be converted to PASS or FAIL.

## Prohibited changes
Do not:
- rebuild the Rule Adapter
- modify 0021–0023 evaluator semantics
- add thresholds, lookbacks, proxies, or new direction logic
- use 2025 for tuning or selection
- infer strength/conflict unless an approved upstream source already supplies it
- treat the historical artifact alone as proof of adapter integration

## Validation gate
Before Production Freeze, the interface must be exercised on the existing independent 0021–0023 evaluator result set and reconciled with zero mismatches. Any mismatch blocks Freeze.

## Current decision
PR #4 remains a proposal/validation change only. No merge and no Production Freeze are authorized by this audit.