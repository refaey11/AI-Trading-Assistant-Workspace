# Decision Brain Integration Compatibility Audit — 2026-08-22

## Result
Status: BLOCKED_PENDING_SOURCE_RECOVERY
Primary classification: MISSING_SOURCE
Secondary classifications: ADAPTER_REQUIRED

## Source-of-truth rule
Workspace / File Library / project backup artifacts remain the source of truth. GitHub is the development/provenance mirror. No original Decision Brain implementation was modified or rebuilt during this audit.

## Existing Decision Brain evidence found in GitHub
The live `decision_brain/` directory contains only `run_070` artifacts in the current repository view:
- `decision_brain/run_070/decision_brain_historical_evidence_integration.py`
- `decision_brain/run_070/DECISION_BRAIN_FULL_HISTORICAL_EVIDENCE_INTEGRATION_RUN_070.json`

The Run 070 wrapper explicitly acts as a historical-evidence integration wrapper and calls the legacy Decision Brain assessment boundary without allowing similarity to change direction. It records governance that similarity predicted return is not used as direction, historical evidence is not the final decision, and the legacy Decision Brain is not modified.

The actual authoritative `decision_brain.py` / V1/V1.1 implementation and its canonical input/output contracts were not found in the live GitHub `decision_brain/` directory. Therefore the Brain contract cannot be safely inferred from the wrapper.

## Completed layer compatibility
### Market / MTF
Status: COMPATIBLE at adapter level.
- Dynamic MTF runtime gate passed.
- Market State contract passed.
- Market Reader contract passed.
- Market Scenario contract passed.

### Historical Memory
Status: COMPATIBLE at evidence-package boundary.
- Historical Context = evidence only.
- Historical Outcome = descriptive evidence only.
- Similarity Memory V2 = retrieval/evidence only.
- Memory Evidence Package enforces `memory_role = EVIDENCE_ONLY`, no direction, no final trade decision, and separate development vs `oos_evaluation` mode.
- 2025 remains locked for development/tuning.

### Outcome -> Scenario
Status: COMPATIBLE at boundary level.
- Historical Outcome cannot alter scenario scores/confidence.
- Historical Outcome cannot create direction or final trade decision.

### Nison
Status: ADAPTER_REQUIRED for full integration.
- Canonical Nison contract: confirmation / contradiction only.
- Unified runtime artifact states missing/invalid candle inputs must return `NOT_EVALUABLE`.
- Nison cannot independently create final trade direction.
- Current runtime evidence is promotion-ready for unified integration, but full repository CI for all Nison runtime was not claimed in the canonical Nison runtime note.

### Trading in the Zone
Status: MISSING_SOURCE / ADAPTER_REQUIRED.
- Current repository artifact explicitly states `CANDIDATE_NOT_AUTHORITATIVE`.
- It defines psychology/process outputs and says TIZ cannot generate BUY/SELL and cannot override technical direction.
- Multiple TIZ rules remain evidence gaps / candidate operators.
- Authoritative producer, deterministic evaluator, adapter integration, historical QA, and cross-file consistency are still listed as freeze requirements.
- Therefore TIZ cannot honestly be promoted to a production/frozen runtime gate from this audit alone.

### Risk
Status: MISSING_PRODUCTION_SOURCE / ADAPTER_REQUIRED.
- Current project handoff classifies `RISK_ENGINE_SPEC_V1` as a research prototype, not execution-ready.
- Research-only parameters must not be promoted to production constants.
- Unresolved live requirements include costs, spread, slippage, leverage, contract size, and broker-specific pip value.
- Risk is architecturally a hard gate, but the production execution contract is not yet available from the current source set.

### Murphy
Status: ADAPTER_REQUIRED / PARTIAL SOURCE CLOSURE.
- Project handoff records 35/51 Murphy rules as currently authoritative/frozen and 16 deferred/open.
- The current `MURPHY_51_MASTER_AUDIT.csv` contains multiple rules still `REVIEW`, `UNBLOCKED`, `PARTIAL`, or `NOT_EVALUABLE`.
- This does not block using already-frozen Murphy evidence, but it prevents claiming that all 51 Murphy rules form a production-frozen Brain input universe.
- 2025 remains excluded from tuning/selection.

## Governing architecture confirmed
- Murphy = technical context / market structure evidence.
- Nison = confirmation / contradiction only.
- TIZ = psychology / process gate only.
- Historical / Similarity Memory = evidence only and never sole decision maker.
- Risk = hard gate.
- Decision Brain = synthesis layer for current market evidence + book knowledge + historical evidence + risk.
- `ABSTAIN` is valid.
- 2025 = OOS and cannot be used for tuning, calibration, optimization, or implementation selection.

## Required next action
1. Recover the authoritative/original Decision Brain artifact from Workspace / File Library / project backup assets.
2. Extract the actual input contract and output contract from source.
3. Reconcile that contract against the completed Market/Memory adapters, Knowledge Alignment boundary, Nison boundary, TIZ boundary, and Risk hard-gate boundary.
4. Create only the minimum adapter(s) required by actual contract mismatches.
5. Add representative integration tests.
6. Add a CircleCI Decision Brain integration job only after the real contract is recovered.
7. Record and sync the next verified checkpoint in GitHub and Dropbox.

## Explicit non-actions
- Do not rebuild `decision_brain.py` from the wrapper.
- Do not invent Brain scoring/thresholds.
- Do not convert Historical Outcome or Similarity into independent direction.
- Do not promote TIZ candidate semantics to authoritative production semantics.
- Do not promote Risk research parameters to live execution constants.
- Do not use 2025 for tuning or implementation selection.
