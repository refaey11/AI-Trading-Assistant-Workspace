# Murphy 0021–0023 — Mapping Execution Blocker V1

Date: 2026-08-15
Status: MAPPING NOT APPROVED / PRODUCTION FREEZE BLOCKED

## Verified source artifacts
The Workspace contains the 0021–0023 evaluator contract and implementation artifacts.
- Evaluator status: IMPLEMENTED_AND_UNIT_TESTED.
- Rules: MURPHY_0021, MURPHY_0022, MURPHY_0023.
- Dynamic MTF; no hard-coded execution timeframe.
- No added thresholds.
- No spot-FX OI proxy; CFTC futures OI is used.
- 2025_used = false.
- Unit tests recorded as PASS.
- Historical evaluation artifacts for 2020–2024 exist.

## Canonical adapter finding
The Workspace canonical `024/rule_adapter.py` returns only:
module, source_rule_id, statement, direction, strength, available, gate, conflict.

The adapter contract additionally requires:
decision_hint and bounded confidence_delta.
The adapter also accepts `current_state` but the implementation does not use it.

More importantly, the current adapter is registry-oriented: it constructs a normalized record from rule metadata and defaults `gate` to pass and `available` to true unless its own role logic changes those values. It does not accept the 0021–0023 evaluator result boundary as a first-class input.

Therefore the proposed direct mapping:
PASS -> gate=pass; FAIL -> gate=fail; NOT_EVALUABLE -> needs_review
cannot yet be treated as an approved production mapping merely by documentation.

## Required safe architecture
Evaluator result must first be preserved losslessly, then passed through an explicitly approved evaluator-result-to-NormalizedEvidence bridge. The bridge must define all status, availability, direction, conflict, decision_hint, and confidence semantics. No field may be inferred when the evaluator does not supply authoritative evidence.

## No semantic changes permitted
- Do not modify 0021–0023 evaluator logic.
- Do not add thresholds.
- Do not add a fixed timeframe.
- Do not substitute spot OI/tick volume for CFTC futures OI.
- Do not use 2025 for tuning or selection.
- Do not rebuild Decision Brain.
- Do not treat existing historical artifacts as proof of production freeze.

## Current gates
Evaluator: PASS/verified
Unit tests: PASS/verified
Historical artifact: PRESENT
Lossless boundary: PASS at recorded deterministic level
Canonical evaluator-result mapping: OPEN
Runtime integration: OPEN
Full reconciliation: OPEN
Availability/leakage audit: OPEN
Production Freeze: NOT GRANTED

## Decision
Do not merge or label 0021–0023 frozen from the current mapping proposal. The next implementation must be the smallest explicit bridge contract, followed by deterministic tests and full reconciliation.
