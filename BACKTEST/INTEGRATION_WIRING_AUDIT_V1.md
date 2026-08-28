# Governed Integration Wiring Audit V1 — 2026-08-28

Branch: `backtest-only-2026-08-28`

## Purpose
Freeze one canonical wiring map before any full Backtest. This is an audit/contract artifact only; it does not alter Decision Brain V1 or book semantics.

## Canonical path
H1 -> Market State -> Dynamic MTF/Time Context -> Murphy 34 -> Nison 44 -> Historical Context Memory -> Historical Outcome Memory -> Similarity V2 -> Context-Aware Retrieval V2 -> Rule Adapter/Knowledge Alignment/Agreement -> Knowledge/Decision Handoff -> Decision Brain V1 -> TIZ process gate -> Risk -> Execution.

## Current verified boundaries
- Decision Brain V1 remains existing/recovered and untouched.
- Handoff preserves contradiction/abstain routing and explicitly prevents Memory/Retrieval from generating direction.
- TIZ boundary is process-only; absent process evidence is NOT_EVALUABLE, not PASS.
- Risk boundary requires upstream SL/TP/ATR and computes the hard risk gate; it does not invent SL/TP.
- CircleCI governed backtest workflow remains parameter-gated with default `false`.
- 2025 remains locked/OOS and is excluded from the development window.

## Current runner finding
`CANONICAL_E2E_ORCHESTRATOR_V2.py` still contains two integration shortcuts that prevent it from being the final governed runner:
1. Similarity/Retrieval are currently represented as filesystem snapshots rather than per-timestamp evidence consumption.
2. TIZ is represented as `UNRESOLVED_OPTIONAL` rather than an explicit invocation of the existing TIZ runtime/process boundary.

These are blockers for a real-source Integration Gate. They must be resolved before the 2016-2024 full Backtest is enabled.

## Guardrails
- No synthetic TIZ PASS.
- No synthetic Risk PASS.
- No synthetic SL/TP.
- No direction from Nison alone.
- No direction from Memory/Similarity/Retrieval.
- No tuning or calibration using 2025.
- No change to Decision Brain V1 semantics.
