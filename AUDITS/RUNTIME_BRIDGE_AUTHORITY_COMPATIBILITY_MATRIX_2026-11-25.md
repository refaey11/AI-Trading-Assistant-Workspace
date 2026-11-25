# Runtime Bridge Authority Compatibility Matrix — 2026-11-25

## Scope and method
Static, read-only inspection of GitHub-tracked source on `fix/similarity-direction-isolation-2026-11-25`. This document records compatibility findings only. No runtime implementation or test code is changed. No tests or workflows are run. No market-data payloads are opened. No 2025/2026 data is accessed.

## Files inspected
- `RUNTIME/DECISION_RUNTIME_V1/full_brain_runtime_bridge_v1.py`
- `RUNTIME/DECISION_RUNTIME_V1/gate3c_single_event_e2e_v1.py`
- `OOS_2025/full_decision_brain_assembler_v1.py`
- `compatibility/decision_brain_v1_handoff_adapter.py`
- `evaluation/three_book_decision_evaluator_v1.py`
- `tests/compatibility/test_decision_brain_nison_absence_nonblocking_v1.py`
- `tests/compatibility/test_nison_absence_nonblocking_v1.py`
- `tests/evaluation/test_three_book_decision_evaluator_v1.py`
- `CHECKPOINTS/DECISION_BRAIN_CONTRACT_AUDIT_2026-08-21.md`
- `audits/evidence/KNOWLEDGE_ALIGNMENT_TO_DECISION_BRAIN_HANDOFF_CONTRACT_AUDIT_2026-08-21.md`
- `governance/KNOWLEDGE_ALIGNMENT_TO_RISK_ENGINE_COMPATIBILITY_CONTRACT_V1.md`

## Compatibility matrix

| Boundary / behavior | Existing evidence | Finding |
|---|---|---|
| Gate3C Murphy authority | Gate3C requires `authoritative is True`, `status == PASS`, known rule IDs and non-empty source-backed event rows | Enforced on this caller path |
| Gate3C Murphy/Risk linkage | Gate3C compares BUY/SELL direction, `pass_rule_id`, and `directional_source_rule_id` sets | Enforced on this caller path |
| Gate3C Nison envelope | Gate3C requires the complete 44-rule Nison ID envelope | Enforced on this caller path |
| Nison confirmation state | Three-book evaluator rejects contradiction; tests explicitly allow `ABSENT` and classify it as medium rather than strong | Missing confirmation is not globally a hard block under current tests |
| Nison authority in direct bridge | Bridge requires a non-empty mapping, but does not check `authoritative`, status, or confirmation | Direct-call authority gap |
| Murphy authority in direct bridge | Bridge requires a non-empty mapping, but does not check `authoritative`, status, rule provenance, or direction | Direct-call authority gap |
| Assembler / handoff adapter | Handoff adapter records Murphy/Nison evidence but does not authenticate it; its PASS is an assessment/handoff result | PASS must not be interpreted as authenticated source authority |
| Risk gate | Bridge requires `authoritative=True`; handoff/evaluator require Risk pass and stop-loss inputs | Risk protections exist but are not a replacement for full source lineage |
| Similarity | Aligned adapter calls Brain with `similarity=None`; Similarity remains evidence metadata | Directional isolation fix remains intact |
| TIZ | Assembler and evaluator treat TIZ as optional metadata only | No TIZ decision authority |
| Brain directional input policy | Brain receives current market row; existing checkpoint describes MTF/timeframe, volatility, volume and price action as current-market inputs, while the project's Master Map places Murphy in directional authority | Policy/lineage mismatch remains unresolved; do not invent a field mapping or modify the Brain |

## Important distinction: Nison envelope vs Nison confirmation
Two separate concepts must not be conflated:
1. Gate3C's source-envelope validation requires all 44 governed Nison rule IDs.
2. The downstream evaluator's confirmation state may be `ABSENT`; existing tests expect medium-strength logic, not an automatic rejection.

Therefore, the current evidence does **not** support changing missing Nison confirmation into a universal hard block. The required behavior is to preserve explicit absence/unknown state and never reinterpret it as confirmed. Whether a particular production route requires the full 44-rule envelope is caller-specific and already enforced in Gate3C.

## Architecture issue requiring a canonical decision
The recovered Brain assesses directional bias from its market row. The Three-Book evaluator checks that Brain bias does not oppose Murphy, but agreement alone does not prove that Murphy generated the direction. The August 21 checkpoint also documents current-market MTF/timeframe and volume context entering Brain. This is not yet reconciled with the project invariant that Murphy/market structure owns direction and MTF/volume are supporting context unless explicitly authorized otherwise.

No change is made here. A canonical decision must define:
- whether MTF and Volume may contribute to directional bias or are context-only;
- the exact existing Murphy evidence fields and provenance that authorize direction;
- whether a direct bridge call must require the same Murphy/Risk linkage currently checked by Gate3C;
- how the current non-blocking Nison ABSENT behavior is preserved while distinguishing missing source envelope from missing confirmation.

## Safe next implementation sequence
1. Approve the direction-authority policy against the existing Master Map and source contracts.
2. Define one shared validation contract using existing field names/enums; do not create speculative schema fields.
3. Add tests first for direct bridge bypass, missing Murphy authority, missing Nison envelope, Nison ABSENT confirmation, direction mismatch, pass-rule mismatch, provenance mismatch, and valid Gate3C path.
4. Only after compatibility review, make the smallest fail-closed bridge change.
5. Run only explicitly scoped GitHub Actions tests whose workflow triggers and data scope have been inspected. Keep 2025 locked and do not launch broad backtests.

## Status
- Static source review: complete for the listed files.
- Existing Nison absence policy: documented by tests as non-blocking / medium-strength when no contradiction exists.
- Direct bridge Murphy/Nison authority validation: gap confirmed.
- Canonical MTF/Volume directional-authority policy: unresolved.
- Runtime code changed: no.
- Tests/workflows executed: no.
- PR created or merged: no.
- Main changed: no.
- 2025 OOS or 2026 market data accessed: no.
