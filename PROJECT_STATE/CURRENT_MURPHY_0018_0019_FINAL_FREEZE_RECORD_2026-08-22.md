# CURRENT — Murphy 0018/0019 Final Freeze Record — 2026-08-22

## Scope
- Rule 0018 — Falling Wedge
- Rule 0019 — Rising Wedge

## Evidence chain used
1. `MURPHY_0018_0019_FINAL_BACKUP_AND_CHANGELOG_V1(5)` — 2026-08-19 21:35
2. `GOVERNANCE_APPROVAL_RECORD_V1.json` inside that backup — decision `APPROVED`
3. The preserved implementation package records 7/7 integration QA PASS.
4. The same backup preserves fail-closed handling: missing evidence = `NOT_EVALUABLE`.
5. 2025 remains OOS and excluded from tuning/calibration.

## Finalization decision
By explicit project-owner instruction on 2026-08-22, the approved freeze-candidate state is promoted to:

**FROZEN — GOVERNANCE/SOURCE SEMANTICS**

This promotion does not invent any threshold, confirmation rule, or trading logic. The following boundaries remain frozen:
- Murphy supplies wedge direction and raw-breakout context.
- Raw breakout is not an auto-trade.
- Volume remains evidence-only; no unsupported numeric Murphy threshold.
- Nison remains confirmation-only and cannot create or reverse wedge direction.
- Decision Brain synthesizes evidence.
- Risk/process remain hard gates.
- Missing evidence = `NOT_EVALUABLE`.
- 2025 remains OOS.

## Runtime boundary
This record does **not** claim executable runtime binding has already been committed. Runtime count therefore remains unchanged until the actual binding/dispatcher integration is present and tested.

## Current status
- 0018: FROZEN governance/source semantics; runtime binding pending
- 0019: FROZEN governance/source semantics; runtime binding pending
- Official Runtime Implemented count: 20/35 until executable integration is verified

## Next action
Use the frozen semantics above to bind 0018 and 0019 into the existing unified runtime, run integration tests, then promote the runtime count only if those tests pass.
