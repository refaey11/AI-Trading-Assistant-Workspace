# Murphy State Verifier

Evidence-first verifier contract for the 51 Murphy rules.

## Authority

Git history and traceable repository artifacts are authoritative. Chat/handoff claims are not authoritative unless backed by repository evidence.

## State model

- FROZEN: freeze evidence, required QA, and no unresolved blocker are proven.
- QA_COMPLETE: required QA is proven but freeze gate is not fully proven.
- TECHNICALLY_COMPLETE: evaluator/technical contract is proven but QA or integration remains.
- INTEGRATION_PENDING: technical rule exists but integration evidence is incomplete.
- BLOCKED: an active authoritative blocker remains.
- UNVERIFIED: evidence is insufficient to establish a stronger state.
- CONFLICT: authoritative evidence contradicts itself and cannot be safely reconciled.

## Safety invariants

1. Never modify frozen Rule artifacts.
2. Never infer missing semantics, thresholds, operators, or contracts.
3. A stale blocker is not active when a later authoritative closure/freeze evidence explicitly supersedes it.
4. Contradictory authoritative evidence produces CONFLICT rather than a guess.
5. 2025 OOS is protected from tuning, threshold selection, calibration, feature selection, rule changes, and optimization.
6. No lookahead, future-data leakage, hindsight labeling, or future-reference contamination.

`evidence_state_schema.json` is the machine-readable contract for downstream collector/state-engine implementation.
