# AI Trading Assistant — Master Continuation State
Date: 2026-08-29
Status: ACTIVE / EXECUTION PATH LOCKED

## Objective
One unified AI Trading Assistant / Decision Brain that reads the market, combines governed evidence, produces BUY/SELL/NO_TRADE with traceable reasons, applies Risk, creates a Trade Plan, and ultimately connects to MT5/n8n.

## Do not rebuild
Reuse the existing Market/Market State/MTF, Murphy, Nison, Similarity/Historical Memory, TIZ, Decision Brain, Risk, and execution artifacts. Do not create a second Decision Schema.

## Locked boundaries
- Murphy: primary technical/directional context under the governed rule boundary.
- Nison: confirmation/contradiction only; cannot originate direction.
- Similarity/Historical Memory: evidence only; cannot decide alone.
- TIZ: process/psychology only; cannot generate direction. If unavailable, explicit NOT_EVALUABLE.
- Risk: hard execution gate.
- Point-in-time: no future evidence; preserve provenance/as_of.
- 2025: OOS only; never tune/calibrate/optimize on it.

## Current truth
GitHub history already contains a Full Decision Brain event orchestration path, historical event producer, OOS assembler, point-in-time evidence layer, execution adapter, and a decision-boundary fix requiring the full 34 Murphy + 44 Nison evidence to be consumed rather than reduced to one selected row.

## Completed in this continuation
- Added `RUNTIME/DECISION_RUNTIME_V1/historical_context_memory_pit_adapter_v1.py` on branch `build/decision-runtime-v1`.
- The adapter is transport/validation only; it cannot generate direction, thresholds, tuning, or trade commands.
- It filters Historical Context Memory by the same pair/context signature and only accepts candidates strictly earlier than `query_as_of`.
- It explicitly counts future candidates excluded and self-match rows excluded.
- The adapter was recorded against the supplied Historical Context Memory artifact for `GBPUSD` at `2016-01-08T06:00:00Z`; the recorded result is PASS with 10 eligible candidates, latest eligible candidate `2016-01-08T04:00:00Z`, 7,456 future rows excluded, and 1 self row excluded.
- Added `RUNTIME/DECISION_RUNTIME_V1/full_brain_memory_pit_integration_v1.py` as the minimal wrapper that resolves PIT memory and passes it as `historical_evidence` into the existing Full Brain assembler without changing Decision Brain scoring or creating new trading semantics.

## Immediate next gate
Do NOT start a new architecture. Use the existing Full Brain path and prove ONE real pre-2025 GBPUSD event end-to-end:
Market/MTF -> full governed Murphy evidence -> full governed Nison evidence -> PIT memory evidence -> TIZ state -> Decision Brain -> Risk -> Trade Plan.

## Acceptance
- one authoritative as_of
- no future evidence
- 34 Murphy + 44 Nison consumed when governed full envelopes are present
- Nison cannot create direction
- Memory cannot decide alone
- TIZ cannot create direction
- Risk hard gate respected
- Decision and Trade Plan traceable to inputs

## After PASS
Gate 3C PASS -> unified 2016-2024 replay -> leakage/provenance/QA -> freeze -> 2025 OOS -> paper -> MT5 Demo -> n8n -> controlled live.

## Cost control
No exploratory CircleCI runs. Local/deterministic checks first; CI only for a candidate that is ready for a governed run.

## Current project conclusion
The project is not broken. The main remaining task is to prove and harden the existing Full Brain decision boundary, not to rebuild the system. Any new code must be the smallest compatibility/wiring change justified by a concrete failing gate.