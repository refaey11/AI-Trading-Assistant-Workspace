# NISON Availability Policy V1

Status: PROPOSED_INTEGRATION_POLICY
Scope: Decision Brain / 2025 OOS evidence handling

## Policy

Nison `NOT_EVALUABLE` is an evidence-availability state, not a global Decision Brain blocker.

- Nison remains confirmation / contradiction evidence only.
- Nison never creates standalone direction.
- `PASS` contributes confirmation only when the runtime emits directional evidence.
- Directional `FAIL` contributes contradiction only when the runtime emits explicit direction.
- `NOT_EVALUABLE` contributes neither confirmation nor contradiction.
- Missing Nison evidence must remain visible in audit/coverage outputs.
- Fail-closed behavior remains inside each Nison evaluator; this policy does not convert missing evidence into PASS.
- Murphy remains the directional market-structure source; Trading in the Zone remains the process/psychology gate.

## Rationale

The existing Nison aggregate already treats confirmation as available only when a directional PASS exists and never creates direction from missing evidence. This policy keeps that evidence semantics intact while preventing missing Nison evidence from becoming a global blocker for the Decision Brain.

## 2025 OOS Governance

2025 remains evaluation-only. No threshold tuning, rule tuning, or evidence fabrication is permitted under this policy.

## Implementation boundary

This policy is an integration-layer contract. It does not modify canonical Nison source contracts or evaluator semantics.
