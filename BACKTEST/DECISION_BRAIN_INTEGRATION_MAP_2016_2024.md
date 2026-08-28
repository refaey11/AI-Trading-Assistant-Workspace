# Decision Brain Integration Map — 2016–2024

## Purpose
Single fixed map for the development backtest. No rule semantics are changed and 2025 remains OOS-locked.

## Data/evidence path
H1 authoritative source
→ Market State contract
→ Dynamic MTF/context
→ Murphy 34 directional evidence
→ Nison 44 confirmation/contradiction
→ Historical Context Memory (evidence only)
→ Historical Outcome Memory (evidence only)
→ Similarity Memory V2 (evidence only; never direction)
→ Context-Aware Retrieval V2 (evidence/metadata only)
→ TIZ process gate (hard process gate)
→ Risk/Execution gate (hard execution gate)
→ Knowledge/Decision handoff
→ recovered Decision Brain V1
→ frozen execution/backtest contract

## Governance invariants
- Murphy can provide directional context.
- Nison cannot independently generate direction.
- Similarity and all memory layers cannot generate direction or tuning parameters.
- TIZ cannot generate direction; it can block execution.
- Risk is a hard execution gate.
- All evidence is timestamp/as-of bounded.
- 2025 is not used for calibration or tuning.
- The recovered Decision Brain source remains unchanged.

## Current implementation status
- H1 2016–2024: PRESENT
- Market State artifact + contract: PRESENT
- Murphy 34 evidence: PRESENT
- Nison 44 evidence: PRESENT
- MTF runtime/adapters: PRESENT in repository; backtest integration gate must verify consumption
- Historical Context Memory: PRESENT in Dropbox/repository boundary; integration consumption must be verified
- Historical Outcome Memory: PRESENT in Dropbox/repository boundary; integration consumption must be verified
- Similarity Memory V2: PRESENT in Dropbox/repository boundary; integration consumption must be verified
- Context-Aware Retrieval V2: PRESENT in Dropbox/repository boundary; integration consumption must be verified
- TIZ process gate: PRESENT in repository
- Risk/Execution: PRESENT in repository
- Knowledge/Decision handoff: PRESENT in repository
- Recovered Decision Brain V1: PRESENT in repository

## Gate before backtest
The backtest is not accepted until the integration gate proves the runtime evidence package reaches the handoff with timestamp/as-of provenance and preserves the governance invariants above.

## Result interpretation
A zero-trade result before the gate passes is an integration diagnostic, not a strategy performance result.
