# Canonical Decision Event V1
Date: 2026-08-29
Status: WIRING CONTRACT — NO NEW STRATEGY LOGIC

## Purpose
Provide one event envelope for the existing market, Murphy, Nison, memory, TIZ and risk outputs so the Decision Brain evaluates one coherent snapshot.

## Event envelope
- event_id: deterministic event identity
- symbol: instrument
- as_of: source/evaluation timestamp
- market: market snapshot + Market State/MTF outputs
- murphy: source-backed rule evidence grouped by role
- nison: confirmation/contradiction evidence only
- memory: Similarity + Historical Outcome evidence only
- tiz: authoritative process state when available; otherwise NOT_EVALUABLE; never synthetic
- decision: Decision Brain output
- risk: hard-gate result
- trade_plan: mechanical plan only when risk permits
- provenance: producer/source/as-of metadata for every evidence group

## Role boundaries
Murphy direction/technical context may inform the Brain. Murphy context/regime evidence informs the Brain without becoming an independent order. Candidate-validation rules remain upstream gates. Murphy risk/portfolio constraints remain in Risk. Process/governance rules do not generate direction. Cross-market evidence cannot silently become GBPUSD evidence.

Nison may confirm or contradict an existing technical hypothesis; it cannot originate direction by itself.

Memory is historical evidence only and cannot be the sole decision maker.

TIZ is process/psychology only and cannot generate direction. When unavailable, record NOT_EVALUABLE and continue; do not infer psychology from price data.

Risk is mandatory and authoritative for execution permission.

## Wiring requirement
All evidence in one event must share the same evaluation snapshot/as-of boundary. Missing evidence is explicit; no default bullish/bearish value may be invented.

## Decision lifecycle
MARKET SNAPSHOT -> EVIDENCE ADAPTERS -> CANONICAL EVENT -> DECISION BRAIN -> RISK -> TRADE PLAN -> EXECUTION EVENT.

## Gate
Before any 2016–2024 unified run, prove one pre-2025 event can be assembled from the existing producers and consumed by the existing Full Brain without bypass or semantic transformation.