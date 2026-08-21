# Existing Brain + Rule Adapter Runtime and Gap Reconciliation

Date: 2026-08-21
Status: EXISTING RUNTIME/TEST ARTIFACTS CONFIRMED / AUTHORITY GUARD NOT YET PROVEN IN CURRENT CODE

## Evidence boundary
File-library project inventory confirms the archived workspace contains:
- `GBPUSD_AI_TRADING_BRAIN_V1/decision_brain.py`
- `GBPUSD_AI_TRADING_BRAIN_V1/decision_brain_v1_1.py`
- `DECISION_BRAIN_V1_SPEC.json`
- `DECISION_BRAIN_V1_1_SPEC.json`
- `DECISION_BRAIN_RULE_ADAPTER_STRUCTURAL_TEST.csv`
- `DECISION_BRAIN_PRECEDENCE_CONFLICT_TEST.csv`
- `COMPATIBILITY_AUDIT_PART3_MODULE_MAP.csv`
- `COMPATIBILITY_AUDIT_PART3_CONFLICT_PRECEDENCE.csv`
- `GBPUSD_RULE_ADAPTER_V1/rule_adapter.py`
- Rule Adapter attribution/test artifacts.

Therefore a Brain-to-Adapter runtime/test layer already existed in the archived workspace. The project should not be described as having no bridge at all.

## Important historical gap evidence
The project compatibility audit records several limitations in the then-current adapter implementation:
1. `current_state` was accepted but not consumed, despite the contract listing market structure, MTF context, volatility, volume availability and current price action.
2. Direction semantics from the legacy 102-rule registry were unsafe for direct normalization; market-context direction, pattern polarity and trade direction needed separation.
3. Adapter risk logic was not a real Risk Engine gate; Risk Engine had to remain authoritative.
4. Similarity was prevented from overriding hard gates, but the final decision-hint/bounded-confidence layer was incomplete.
5. The old 102-rule registry was not equivalent to 102 executable strategies.

## Reconciliation with the newer 79-rule state
The newer project evidence establishes a separate authoritative 79-rule provenance boundary. Therefore the existing runtime/test artifacts may be reused only after an explicit source-authority guard is proven or added.

Safe rule:
`Existing Brain/Adapter runtime != automatic authority over rule identity.`

The runtime layer can be retained; the rule resolver must consume only provenance-approved current rules and preserve `source_rule_id`/source attribution.

## What is now proven
- Existing Brain runtime: YES.
- Existing Rule Adapter runtime: YES.
- Existing structural and precedence test artifacts: YES.
- Existing attribution/retest artifacts: YES.
- Existing bridge concept/runtime between Rule Adapter and Brain: YES at archived-workspace level.

## What is still not proven
- Current code enforces the authoritative 79-rule allow-list.
- Current runtime source resolver rejects legacy-only rule entries.
- Current runtime uses all contract-required market-state fields during normalization.
- Current Brain/Adapter runtime is the exact final version aligned with the newer 79-rule authority state.

## Final verdict
The previous conclusion is refined as follows:

`A Brain <-> Rule Adapter runtime/test bridge already exists.`

The real remaining task is not to build a bridge from zero. It is to reconcile and minimally patch/guard the existing bridge so that it is authoritative-79-rule compatible, preserves the current role boundaries, and does not reintroduce legacy 102-rule semantics.

## Next safe action
Inspect the actual current `rule_adapter.py` and attribution/mapping artifacts, then:
1. verify source-rule acceptance behavior;
2. verify authoritative-set guard;
3. verify unknown/unattributed rule behavior;
4. verify 79-rule mapping preservation;
5. run focused regression tests on pre-2025 data only;
6. record PASS/FAIL before any end-to-end integration.
