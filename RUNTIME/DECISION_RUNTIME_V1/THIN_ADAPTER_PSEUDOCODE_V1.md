# Thin Adapter Implementation Contract V1
Date: 2026-08-29
Status: IMPLEMENTATION SPEC — NO STRATEGY LOGIC

## Goal
Populate the existing DECISION_SCHEMA_V1 from existing producer outputs. The adapter may normalize field names and validate provenance/as_of, but may not invent trading semantics, scores, directions, thresholds, or missing evidence.

## Input producers
market_state, mtf_reader, murphy, nison, similarity_memory, historical_outcome_memory, tiz_optional, risk_engine.

## Assembly order
1. Read authoritative market snapshot and `as_of`.
2. Read Market State + available MTF outputs at or before `as_of`.
3. Read Murphy evidence and classify through MURPHY_34_ROLE_MAP_V1.
4. Read Nison confirmation/contradiction evidence for the same snapshot.
5. Read Similarity/Historical Outcome memory only through existing source-backed builders/queries and retain provenance.
6. Read TIZ authoritative process state; if unavailable emit `NOT_EVALUABLE`.
7. Assemble the existing `DECISION_SCHEMA_V1` fields without creating a second schema.
8. Invoke the existing Decision Brain.
9. Pass its result to the existing Risk boundary.
10. Produce a Trade Plan only when Risk permits; otherwise preserve the block reason.

## Hard validation
- Reject future-dated evidence relative to `as_of`.
- Reject silently synthesized values.
- Do not convert qualitative direction labels to arbitrary numbers.
- Nison cannot originate direction.
- Memory cannot be sole decision maker.
- TIZ cannot originate direction.
- Cross-market evidence requires an explicit approved contract.
- 2025 cannot be used for tuning.

## Single-event acceptance fixture
Use one pre-2025 GBPUSD event with all available source-backed evidence. Expected result is a fully traceable Decision Schema payload. Direction must be attributable to allowed directional evidence; confirmation, context, memory, TIZ, and risk retain their boundaries.

## Explicit non-goal
This contract does not implement a new strategy, alter existing Murphy/Nison rules, or claim profitability. It exists solely to connect existing components into one executable decision path.