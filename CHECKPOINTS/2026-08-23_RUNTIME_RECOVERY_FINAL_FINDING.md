# Existing Runtime Recovery — Final Finding — 2026-08-23

## Scope inspected
- Reconstructed GBPUSD Rule Evaluator V2 workspace: 241 readable archive entries.
- Dropbox `AI_Trading_Assistant_FULL_PROJECT_V1` recursive listing.
- Dropbox `AI_Trading_Assistant_CORE_V1` contents.
- Existing GitHub Decision Brain / OOS / bridge contracts.

## Finding
No authoritative central runner was recovered that generates a fresh 2025 Decision-Event Stream from the existing 78-rule runtime through Decision Brain -> process/Risk -> execution/evaluation.

The CORE contains `decision_engine/DECISION_CONTRACT_V1.json`, smoke-test artifacts, and `risk_engine/RISK_ENGINE_SPEC_V1.json`, but no standalone `risk_engine.py` or executable risk runtime was found. The archived Risk Engine contains research artifacts only. The full project contains `market_pipeline_evidence_adapter.py`, but this is a downstream evidence adapter, not a complete rule/decision runner.

The reconstructed GBPUSD Rule Evaluator workspace contains rule evaluators and contracts but no central runner/exporter for the frozen 2025 event stream.

## Governance decision
- Do not invent TIZ semantics.
- Do not invent Risk semantics or a fake risk runtime.
- Do not modify frozen Murphy/Nison rules.
- Do not use 2025 for tuning, calibration, threshold selection, or implementation selection.
- Preserve the current 78-rule allowlist (34 Murphy + 44 Nison); MURPHY_0008 remains blocked.

## Current exact gate
The missing artifact is now classified as an **existing-runtime recovery gap**, not a Market State/MTF gap.

Next work must be limited to building/validating an orchestration layer that consumes only already-produced, authoritative inputs and fails closed when TIZ/Risk evidence is unavailable. A real executable 2025 performance run remains unauthorized until executable TIZ/Risk evidence can satisfy the frozen OOS stream contract.
