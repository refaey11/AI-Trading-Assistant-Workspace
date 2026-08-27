# Current Decision Brain Component Wiring Audit — 2026-08-26

## Scope
Read-only compatibility audit of the current recovery branch. No rule semantics, thresholds, or 2025 OOS parameters changed.

## Status matrix

| Component | Source/runtime evidence | Current Decision Brain/OOS path | Status |
|---|---|---|---|
| 34 Murphy rules | Full Murphy evidence is preserved per event | Passed to `assemble_decision_event()` as full evidence and converted to a governed 34-rule compatibility view | WORKING |
| 44 Nison rules | Full Nison evidence is preserved per event | Passed to the same decision boundary as full evidence; used for confirmation/contradiction | WORKING |
| 78-rule governed package | `build_governed_78_package()` + assertion on full-evidence path | Explicit ingress artifact before Decision Brain governance | WORKING |
| Market State | 2025 producer reads the market-state context and passes the latest context row into the recovered Brain | `row=_pick_context(market_context, ts)` | WORKING |
| MTF | Historical MTF datasets exist and are part of the project, but the current 2025 event producer does not pass a separate MTF evidence object into the Decision Brain boundary | Current producer feeds market-state context; no explicit MTF evidence field at the boundary | PRESENT / NOT EXPLICITLY WIRED |
| Historical Context Memory | Source package and current reads exist; prior CI boundary work exists | Current 2025 producer calls `assemble_decision_event(... historical_evidence=None)` | NOT WIRED |
| Historical Outcome Memory | Source package/read artifacts and prior boundary verification exist | Current 2025 producer does not pass outcome-memory evidence into `historical_evidence` | NOT WIRED |
| Similarity Memory | Source package/read artifacts and prior boundary verification exist | Current handoff adapter calls recovered Brain with `similarity=None` | NOT WIRED |
| Context-Aware Retrieval | Current retrieval artifacts exist and provide project-derived evidence | No retrieval payload is connected to the current 2025 decision event's `historical_evidence` | NOT WIRED |
| TIZ | Optional 2025 evaluation path; no authoritative verified events in current OOS | Optional bypass is explicit; TIZ does not generate direction | OPTIONAL / NOT VERIFIED |
| Risk | Risk evidence is passed to governance and the Three-Book evaluator; execution risk profile is active | Hard execution gate | WORKING |
| Execution | Frozen execution adapter produces executable plans and P&L trades | 31 trades were produced in the latest artifact; subsequent censoring audit is being added | WORKING / AUDIT IN PROGRESS |

## Critical finding
The current branch does **not** constitute a fully memory-aware Decision Brain.

The 78 rules are actually wired into the current OOS decision boundary. The memory assets are present in the project and have historical compatibility-boundary work, but the current 2025 producer passes `historical_evidence=None`, and the handoff adapter invokes the recovered Brain with `similarity=None`.

This is a wiring gap, not evidence that the memory systems are missing or should be rebuilt.

## Architecture constraint
Memory must remain historical evidence only. It must never generate direction or become the sole decision maker. The existing handoff adapter already sanitizes historical evidence to prevent predicted returns from becoming direction.

## Required next step
Build a **shadow-only historical evidence bridge** for development years (2016–2024 first), feeding:
- Historical Context Memory
- Historical Outcome Memory
- Similarity Memory
- Context-Aware Retrieval

into the single `historical_evidence` envelope without changing final direction semantics.

Measure:
- retrieval availability,
- candidate counts,
- lookahead violations,
- memory availability by timestamp,
- agreement/conflict with Murphy direction,
- whether memory is actually consumed downstream,
- and whether any memory field can affect direction (must remain false).

Only after this shadow audit passes should the memory evidence be made part of the governed decision boundary.

## OOS governance
2025 remains locked and must not be used to tune memory retrieval, thresholds, weights, or decision semantics. The first implementation/validation target for memory wiring is pre-2025 chronological development data.
