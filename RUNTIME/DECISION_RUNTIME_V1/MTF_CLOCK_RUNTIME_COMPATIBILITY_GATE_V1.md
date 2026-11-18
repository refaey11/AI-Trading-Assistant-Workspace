# Live Decision Runtime V1 — MTF Clock Compatibility Gate

**Status:** FAIL-CLOSED — no production timezone policy is approved yet  
**Scope:** Compatibility between MT5 Raw Capture V1.3, the MT5 clock provenance validator, and Live Decision Runtime V1.

## Finding

The previous Live Decision Runtime required timezone-aware evidence-envelope timestamps, but it did not require per-timeframe bar-clock lineage or an approved timezone policy. A caller could therefore provide plausible MTF fields and a claimed source envelope without proving that the bar timestamps used to create those fields had passed the MT5 clock gate.

## Runtime control added

Before reading brain_row, trusting MTF fields, or binding dynamic MTF roles, the runtime now requires:

1. A clock_provenance object with status VERIFIED.
2. Exactly six timeframe records: M5, M15, M30, H1, H4, and D1.
3. Each record identifies its timeframe and matches the MTF envelope's source and producer.
4. Each record carries a 64-character SHA-256-shaped payload hash.
5. Each record passes verify_bar_clock_lineage for source clock, server wall time, explicit UTC, observation time, policy ID, evidence reference, offset type/range, and offset arithmetic.
6. Bar and observation timestamps are causal and do not exceed the decision query_as_of.
7. No bar from 2025 or earlier can enter this live runtime path.
8. The timezone_policy_id must be present in APPROVED_TIMEZONE_POLICY_IDS.

## Critical policy state

APPROVED_TIMEZONE_POLICY_IDS is intentionally empty in production code.

The repository's current MT5_CLOCK_SOURCE_EVIDENCE_REGISTER_2026-11-18.md says authoritative MT5 platform documentation, clock-domain approval, and trusted observation-clock evidence are still pending. Therefore no production policy ID may be allowlisted yet.

Consequences:
- V1.3 rows marked UNVERIFIED are rejected.
- Missing clock provenance is rejected.
- A caller-provided VERIFIED status does not bypass arithmetic or policy checks.
- Even a structurally valid record is rejected unless its policy ID is explicitly approved in repository code after evidence review.
- The current production runtime will block all MTF-backed live decisions until that approval is completed.

Tests use TEST_POLICY_ONLY by overriding the allowlist inside the test process only. This synthetic fixture policy is not present in production code and is not an approved real broker/MT5 policy.

## Important limitations

- The gate checks declared lineage and timestamp arithmetic. It does not independently authenticate the content of timezone_evidence_ref.
- A payload hash shape is checked here; this runtime does not recompute the raw-capture payload hash or prove that every derived MTF field was calculated from the referenced bar payload. That requires a separately specified producer-to-feature lineage contract.
- The runtime's available_at envelope timestamp and per-bar observation timestamps are both checked against query_as_of; no unsupported maximum-staleness threshold is invented.
- The current V1.3 raw-clock producer cannot pass this gate because it intentionally emits UNVERIFIED and does not produce approved UTC lineage.

## Preserved boundaries

- No MTF formulas, feature values, role-selection heuristics, direction rules, or scoring semantics changed.
- Murphy remains the directional context; Nison remains confirmation/contradiction only.
- TIZ remains a process gate and cannot generate direction.
- Similarity remains audit-only and is not passed into Decision Brain direction.
- Risk gate semantics are unchanged.
- 2025 OOS remains locked and unused.
- Execution remains SIGNAL_ONLY; orders remain disabled.
- No main changes and no PR merge.

## Acceptance needed to unblock

1. Attach and review authoritative MT5 API documentation/source for the relevant clock semantics.
2. Establish a reviewed broker/platform timezone policy and its immutable policy ID.
3. Provide evidence for the observation clock's synchronization/uncertainty.
4. Approve the policy ID explicitly in APPROVED_TIMEZONE_POLICY_IDS.
5. Define and test cryptographic lineage from captured bar payloads to the derived MTF fields before allowing Stage C feature production.

Until these are completed, the runtime is intentionally fail-closed.
