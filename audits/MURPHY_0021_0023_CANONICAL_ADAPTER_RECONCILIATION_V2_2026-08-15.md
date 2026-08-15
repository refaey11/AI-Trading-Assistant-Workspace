# Murphy 0021–0023 — Canonical Rule Adapter Reconciliation V2

Date: 2026-08-15
Status: INTEGRATION BLOCKED — NOT PRODUCTION FROZEN

## Source-verified facts
The existing Workspace contains `024/rule_adapter.py` and `025/rule_adapter_contract_v1.json`.
The adapter is an initial/design implementation. The contract requires evidence + gate + conflict + decision_hint + bounded confidence_delta; the current implementation returns only module, source_rule_id, statement, direction, strength, available, gate, conflict.

## 0021–0023 evaluator status
The existing evaluator contract is IMPLEMENTED_AND_UNIT_TESTED for MURPHY_0021, MURPHY_0022, MURPHY_0023.
- 0021: price direction + existing volume_direction UP; no extra threshold.
- 0022: price UP + volume UP + available CME British Pound futures OI UP.
- 0023: price DOWN + volume UP + available CME British Pound futures OI UP.
- No spot-FX OI proxy.
- No added thresholds.
- Dynamic timeframe policy.
- 2025_used = false.

Existing unit tests recorded PASS for bullish/bearish/no-confirmation and missing/wrong-OI/wrong-price cases.

## Historical gate
Canonical clean historical artifact is the 2020–2024 clean result set: 122,934 rows and zero 2025 rows. The previously observed 122,943-row raw artifact is not the canonical freeze target.

## Adapter compatibility finding
The current canonical adapter is registry-oriented and does not accept evaluator results as a first-class input. Therefore it is unsafe to map evaluator `status` directly to canonical `gate` without an approved bridge contract.

Required bridge behavior:
- preserve evaluator result losslessly before normalization;
- do not invent direction when evaluator says NONE/UNKNOWN;
- do not infer strength or confidence;
- do not allow Similarity to override a hard gate;
- Risk Engine remains the authoritative hard gate;
- NOT_EVALUABLE must remain unavailable/needs-review semantics unless explicitly approved by the canonical contract.

## Required minimal repair
1. Add/approve evaluator-result bridge input contract separately from registry normalization.
2. Extend canonical evidence output with `decision_hint` and bounded `confidence_delta` exactly as required by the existing contract.
3. Keep registry adapter behavior unchanged unless compatibility tests prove a necessary correction.
4. Add deterministic bridge tests for 0021–0023 PASS/FAIL/NOT_EVALUABLE and direction preservation.
5. Reconcile all 122,934 clean evaluator results through the bridge.
6. Run availability/no-lookahead and provenance checks.
7. Only then issue the freeze manifest.

## Explicit non-actions
- Do not rebuild the adapter.
- Do not alter 0021–0023 evaluator semantics.
- Do not add thresholds.
- Do not use spot OI as a proxy.
- Do not tune on 2025.
- Do not call the freeze candidate production frozen.

## Current verdict
Historical/evaluator QA: PASS / freeze candidate.
Canonical adapter integration: OPEN.
Production Freeze: NOT GRANTED.
