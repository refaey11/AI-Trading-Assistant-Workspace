# AI Trading Assistant — Decision Brain
## Current State Checkpoint — 2026-08-31

Purpose: preserve the exact working state reached during Gate 3C validation so the project is not restarted, rebuilt, or confused with older states.

## 1. Project rules / non-negotiables
- This is the AI Trading Assistant / Decision Brain project, not an indicator.
- Existing project knowledge/components are not to be rebuilt from scratch.
- 2025 remains OOS and must not be used for tuning.
- Murphy provides technical context / market structure.
- Nison provides confirmation; it does not independently create the final direction.
- Trading in the Zone (TIZ) is direction-neutral/process-gate material and must not generate direction.
- Similarity / historical memory is evidence only and is never the sole decision maker.
- Decision Brain must remain fail-closed: if evidence does not produce an executable direction, it may reject the trade rather than invent BUY/SELL.

## 2. Gate 3C pipeline reached
The current Gate 3C workflow on `main` explicitly:
1. Restricts the event timestamp to 2016-2024.
2. Authenticates to Dropbox.
3. Acquires one-event source slices for H1, Murphy, MTF, market state, Nison, historical context/outcome, similarity, and retrieval.
4. Requires exactly 44 Nison rules (`NISON_0001` through `NISON_0044`) for the event.
5. Builds authoritative risk evidence.
6. Builds the canonical event bundle.
7. Runs the real single-event Decision Runtime E2E.
8. Uploads the resulting `gate3c_result.json` artifact.

Current workflow file: `.github/workflows/gate3c-launcher.yml`.

## 3. Evidence from the latest validation sequence
User-provided GitHub screenshots show the following progression:

- Gate 3C automated validation run #32: **Failure**, duration 46s, branch `ci/gate3c-auto-auth-test`, with `single_event` failing after ~42s.
- Subsequent Gate 3C commits included:
  - `Gate 3C: preserve evidence on NO_TRADE` (commit on branch `gate3c-contract-fix-2026-08-31`).
  - `CI: single-shot Gate 3C auth probe` (commit on `main`).
- Gate 3C launcher run #39: **Success**, duration 50s; `single_event` **Successful in 46s**; one artifact was produced.
- This successful run demonstrates that the current auth/acquisition/E2E launcher path can execute end-to-end for the single event.

## 4. Decision result already observed in the E2E evidence
For the tested event, the important semantic result was:
- Risk: `risk_pass=true`.
- Risk budget: passed/closed.
- RR: `2.0`.
- Decision Brain: `NO_TRADE` -> `REJECTED`.
- Brain rejection reason: `BRAIN_DIRECTION_NOT_EXECUTABLE`.
- TIZ: `NOT_EVALUABLE`, `authoritative=false`; it did not block the event and did not generate direction.
- Nison: engine/rule evaluation path is active. The evidence container can show PASS at the evidence-container level, but the present rule/event evidence did not provide an executable confirmation direction.

Therefore the current blocker is NOT the old MTF acquisition problem and NOT Risk. The pipeline has reached the Decision Brain semantic layer.

## 5. Code-level observation captured during the investigation
A GitHub screenshot of `compatibility/decision_brain_v1_handoff_adapter.py` showed the adapter normalization path, including:
- `_normalize_gate(textual)` returning normalized gate values.
- Risk normalization now uses `_normalize_risk_gate(risk)` instead of directly normalizing the raw risk field.
- The visible diff included a `risk_pass` handling path and a `NOT_EVALUABLE` fallback.

This was part of the reconciliation work around the Decision Brain handoff adapter. No claim is made here that this adapter is the root cause; that must be verified before changing code.

## 6. Current technical question — DO NOT skip this
The next investigation must answer exactly why the current event has no executable direction:

A. Does Murphy produce a directional/market-structure signal that reaches the canonical evidence container?
B. Does Nison produce a directional confirmation label (`BULLISH` / `BEARISH`) or only a non-directional/pass evidence state for this event?
C. Does the evidence bridge correctly map governed Nison outputs without inventing direction?
D. Does the Decision Brain V1 contract intentionally require an explicit executable direction from the upstream evidence, causing `BRAIN_DIRECTION_NOT_EXECUTABLE` by design?
E. Is there an adapter/evidence-mapping defect that drops a valid Murphy/Nison direction before the Decision Brain sees it?

Do NOT tune thresholds, change trading logic, loosen fail-closed behavior, or modify 2025 data until A-E are established from source evidence.

## 7. Relevant existing architecture evidence
GitHub PR #39 (`OOS: connect governed Nison runtimes to 2025 producer boundary`) states that the evidence bridge normalizes `BUY_CANDIDATE` / `SELL_CANDIDATE` into `BULLISH` / `BEARISH` confirmation labels **without creating direction**, and that missing source-backed inputs remain `NOT_EVALUABLE`.

GitHub PR #32 (`OOS: isolated TIZ optional evaluation mode`) states that TIZ remains direction-neutral and unchanged in canonical three-book mode, and that the optional evaluation mode does not add direction logic or change SL/TP.

## 8. Safe next sequence
1. Freeze the current successful Gate 3C launcher state.
2. Inspect the exact canonical event JSON and E2E result artifact from the successful run.
3. Trace Murphy evidence -> canonical bundle -> Decision Brain input.
4. Trace Nison 44/44 evidence -> confirmation mapping -> Decision Brain input.
5. Compare the adapter contract with the actual event payload fields.
6. Determine whether `BRAIN_DIRECTION_NOT_EXECUTABLE` is an intended V1 rejection or a mapping defect.
7. Only after that, make the smallest compatibility fix if a defect is proven.
8. Re-run the same single event and require evidence preservation.
9. Do not use 2025 for tuning.

## 9. Change policy for this checkpoint
This checkpoint is documentation only. It does not change trading logic, risk rules, TIZ semantics, Nison contracts, Murphy rules, MTF logic, historical memory, similarity memory, or 2025 OOS data.

## 10. Recovery statement
If a later chat becomes confused, resume from this checkpoint. The project is NOT to be restarted. The immediate task is semantic tracing of the current Gate 3C event from Murphy/Nison evidence into the Decision Brain and determination of whether `BRAIN_DIRECTION_NOT_EXECUTABLE` is intentional or caused by adapter/evidence mapping.
