# Decision Brain V1 ↔ Risk Engine V1 Compatibility Audit — Part 01

Date: 2026-08-21
Status: EVIDENCE AUDITED / FULL RUNTIME CHAIN NOT YET PROVEN

## Evidence examined
- Dropbox `/decision_brain.py`, server-modified 2026-08-19.
- Dropbox `/DECISION_BRAIN_V1_SPEC.json`, server-modified 2026-08-19.
- Dropbox active `RISK_ENGINE_SPEC_V1.json`, server-modified 2026-08-19.

## Decision Brain V1 contract findings
1. V1 is explicitly an evidence aggregator, not a trading signal generator.
2. It produces market-state assessment only.
3. It consumes six trend-regime inputs: M5, M15, M30, H1, H4, D1.
4. Volume is used only when `volume_available=true`; unavailable volume is represented as unavailable/neutral, not as zero market volume.
5. Similarity is HistoricalMemory evidence only.
6. Output includes market state, directional bias, confidence, evidence, contradictions, and explicit no-trade reasons.
7. The spec states risk is evaluated after market understanding and V1 has no automatic BUY/SELL execution.
8. Hard rules include: no future data, 2025 OOS/no calibration, similarity not standalone, evidence-module traceability.

## Risk Engine V1 contract findings
Hard gates are explicitly defined:
- positive stop distance
- stop distance between 0.5 ATR and 4 ATR
- defined take profit
- risk budget fixed before entry

Declared risk behavior:
- risk profiles: 0.25%, 0.5%, 1%, 1.5%
- position size = risk_money / stop_distance
- stop modes: structure, 2x ATR, hybrid
- research target: 1.5R
- drawdown is tracked but not yet a trading halt
- live execution remains incomplete until costs, spread, slippage, leverage, contract size and broker-specific pip value are added

## Compatibility matrix — Part 01

| Boundary | Verdict | Evidence |
|---|---|---|
| Decision Brain is market-understanding before risk | PASS | Brain spec explicitly places risk after market understanding |
| Brain automatic execution -> Risk | PASS boundary | V1 explicitly has no automatic BUY/SELL execution |
| Six-timeframe architecture -> Brain | PASS | Code/spec explicitly consume M5, M15, M30, H1, H4, D1 |
| Volume semantics -> Brain | PASS | `volume_available` gate; unavailable != zero |
| Similarity -> Brain | PASS | Evidence/memory only; not standalone |
| 2025 governance -> Brain | PASS | Spec explicitly reserves 2025 as OOS/no calibration |
| Brain output -> Risk Engine entry inputs | PARTIAL | Brain provides market context, but the inspected evidence does not yet show a complete runtime adapter mapping to stop distance, ATR, TP and risk budget |
| Knowledge Alignment 79-rule contract -> Brain runtime | UNPROVEN | Inspected V1 code/spec mentions curated knowledge but does not yet expose the full 79-rule runtime interface |
| Process gate / Trading in the Zone -> Brain runtime | UNPROVEN | Requires explicit runtime contract evidence in the next audit part |
| Risk Engine live readiness | NOT READY BY SPEC | Risk spec explicitly marks research-only missing live market mechanics/cost inputs |

## Key interpretation
The high-level ordering is compatible:

`Market evidence -> Decision Brain market understanding -> risk context / Risk Engine gates -> no automatic execution in V1`

However, the actual runtime handoff from Decision Brain outputs to the Risk Engine inputs is not yet proven by the inspected artifacts. This is a compatibility evidence gap, not a reason to rebuild either module.

## Governance
- Do not rebuild Decision Brain V1 or Risk Engine V1.
- Preserve the six-timeframe architecture as already proven.
- Preserve `volume unavailable != zero`.
- Preserve Similarity as historical evidence only.
- Preserve 2025 as final OOS and never use it for tuning/calibration.

## Next audit part
Continue with actual Risk Engine runtime artifacts (events/results/trades/archive) and locate/inspect the runtime contracts for:
1. Brain -> Risk input adapter.
2. 79 authoritative rules -> Brain knowledge interface.
3. Trading in the Zone process gate -> Brain/Risk ordering.
4. Risk output/event lineage and AS-OF/no-lookahead evidence.

Only after this evidence is checked may the end-to-end compatibility verdict be finalized.
