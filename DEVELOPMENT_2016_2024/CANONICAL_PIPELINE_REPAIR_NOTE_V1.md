# Canonical Decision Pipeline Repair V1 — Contract Reconciliation

Status: RECONCILIATION REQUIRED — prior V5.4 defect claim corrected

## Scope
This note covers the 2016–2024 development replay and its execution-contract boundaries only. Murphy, Nison, Similarity, Memory, TIZ, and Decision Brain direction semantics remain unchanged.

## Two separate risk contracts

### A. Frozen historical candidate-evaluation contract
- Stop distance: 0.75 ATR
- Target distance: 2.0 × stop distance = 1.5 ATR
- Resulting reward/risk: 2.0R
- Used by the V5.4 historical candidate replay and the Gate 3C single-event evaluation evidence builder.
- This is a candidate-evaluation protocol, not the canonical 3R risk policy and not production authorization.

### B. Canonical risk-integration contract
- Minimum reward/risk: 3.0R
- Enforced by `RUNTIME/RISK_ENGINE_INTEGRATION_V1/risk_engine_integration_v1.py`.
- The governed E2E orchestrator calculates its target as 3.0 × stop distance before calling this engine.
- This contract must not be silently replaced by the candidate 2R protocol.

The separate `risk_engine/risk_execution_runtime_v1.py` validates positive TP distance, stop geometry, frozen risk profile, and locked risk budget, but does not itself enforce a minimum RR. In the historical candidate path, the 2R ratio is supplied by the frozen candidate profile. Do not treat a PASS from that runtime as proof of the canonical 3R contract.

## V5.4 source audit — correction
The earlier statement that V5.4 passed a 1.5 × ATR target while recording 2.0R as a defect was incorrect.

V5.4 sets:
- `stop_distance = 0.75 * ATR`
- `rr_target = 2.0 * stop_distance`
- `take_profit_distance = rr_target`

Therefore `rr_target = 1.5 * ATR`, which is exactly 2.0R relative to the 0.75 ATR stop. The V5.4 target calculation is internally consistent with its frozen 2R candidate-evaluation contract. No V5.4 execution-code change is authorized on the basis of the previous defect claim.

## Gate 3C interpretation
Gate 3C's single-event risk evidence builder labels its authority scope as `evaluation_single_event` and uses the frozen 0.75 ATR / 2R candidate profile. A Gate 3C PASS therefore demonstrates that candidate-evaluation path for one source-backed pre-2025 event; it does not demonstrate the canonical 3R integration contract or production readiness.

## Required acceptance sequence
1. Keep separate regression tests for candidate 2R and canonical 3R behavior.
2. Verify canonical 3R passes and canonical 2R / 1.5R fail.
3. Verify candidate 2R remains accepted by its explicitly scoped evaluation runtime.
4. Run one real source-backed pre-2025 event through the appropriate governed path.
5. Run a small deterministic 2016–2024 sample.
6. Only then consider the full 2016–2024 replay.
7. Costs, slippage, and profitability analysis remain subsequent stages.

2025 remains OOS-locked and must not be used for tuning, calibration, or optimization. No profitability or production-readiness claim is authorized by this note.
