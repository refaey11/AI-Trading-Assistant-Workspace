# Nison Integration Audit — 2026-08-22

## Purpose
Start Nison integration without rebuilding the existing Nison knowledge base and without changing frozen Murphy semantics.

## Source package findings
The existing Nison Candlestick Confirmation V1 package explicitly describes itself as an engineering prototype, not an exact reproduction of the book. It states that the next step is to map each pattern's contextual requirements (trend, location, preceding candles, support/resistance) from the source knowledge base before robustness/OOS testing.

The Nison Context Engine V1 package likewise describes itself as an operational prototype and explicitly says its thresholds are not canonical Steve Nison thresholds.

## Integration role
Nison is a directional confirmation layer on top of an established technical setup. It must not replace Murphy's structural role and must not independently create a final trade decision.

## Current status
- Existing candle detector: PRESENT
- Existing contextual engine: PRESENT
- Canonical Nison source mapping: PENDING
- Authoritative producer contract: PENDING
- Deterministic integration evaluator: PENDING
- Unified Decision Brain adapter: NOT STARTED
- 2025 OOS protection: REQUIRED and must remain locked

## Rules for this phase
1. Audit and integrate existing artifacts first.
2. Do not invent Nison pattern definitions or thresholds.
3. Do not tune against 2025.
4. Do not promote candidate prototype semantics to canonical status.
5. Nison may confirm or reject a Murphy setup; it is not the sole decision maker.

## Immediate next action
Build a source-mapped Nison contract from the existing knowledge package: pattern identity, directional implication, required context, invalidation/conflict conditions, evidence availability/provenance, and output status. Only then create the runtime producer/evaluator.