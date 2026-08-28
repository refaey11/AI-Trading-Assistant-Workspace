# Real-Source E2E Boundary Plan V1 — 2026-08-28

## Immediate blockers
1. Similarity V2 and Context-Aware Retrieval V2 must be consumed as timestamp/as-of evidence, not merely reported as directory snapshots.
2. TIZ must be invoked through the existing process-only boundary; unavailable historical process evidence must remain NOT_EVALUABLE rather than PASS.

## Next implementation contract
For each H1 timestamp t in 2016-2024:
- Similarity: retrieve only records with source/effective time <= t and attach provenance.
- Retrieval: retrieve only records with source/effective time <= t and attach provenance.
- TIZ: invoke the existing process boundary if process evidence exists; otherwise emit NOT_EVALUABLE.
- Handoff: preserve evidence-only status and contradiction/abstain routing.
- Brain: consume the governed handoff without changing Decision Brain V1 semantics.
- Risk: only evaluate with real upstream execution inputs; otherwise NOT_EVALUABLE.

## Completion gate
The full Integration Gate must remain blocked until these two real-source boundaries are implemented and covered by a deterministic smoke test.
