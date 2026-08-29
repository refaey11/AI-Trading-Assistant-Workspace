# Gate 3C — Integration Status V1
Date: 2026-08-29

## Current truth
The project has source-backed contracts and producers for Market/MTF, Murphy, Nison, Similarity/Historical Memory, TIZ process handling, Decision, and Risk/Execution. The current work is integration, not replacement of those subsystems.

## What is proven
1. Murphy 34 role map exists and separates direction/context, candidate validation, risk/portfolio, process/governance, and cross-market evidence.
2. Canonical Decision Event wiring contract exists.
3. TIZ remains optional: unavailable state is NOT_EVALUABLE and TIZ cannot generate direction.
4. Similarity/Historical Memory remains evidence-only and cannot be the sole decision maker.
5. Risk remains an execution hard gate.
6. 2025 remains excluded from tuning.

## What is NOT yet proven
A single real pre-2025 event has not yet been demonstrated, from existing producers, as one consumed Decision Schema payload containing Market/MTF + Murphy + Nison + Memory (+ TIZ state) and then producing Brain decision + Risk + Trade Plan.

## Next implementation gate
Build only the thin adapter needed to populate the existing DECISION_SCHEMA_V1 from existing producer outputs. Do not create a second decision schema and do not add strategy logic.

## Acceptance test
One pre-2025 GBPUSD event must satisfy:
- one authoritative as_of;
- all available evidence attached with provenance;
- missing evidence explicit, never synthesized;
- Nison cannot originate direction;
- Memory cannot be sole decision maker;
- TIZ cannot originate direction;
- Risk hard gate is respected;
- resulting decision and trade plan are traceable to inputs.

Only after this event passes should the same path be expanded to the 2016–2024 unified replay.
