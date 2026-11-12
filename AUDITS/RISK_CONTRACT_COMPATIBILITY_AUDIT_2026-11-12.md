# Risk Contract Compatibility Audit — 2026-11-12

Status: AUDIT COMPLETE — NO RUNTIME CODE CHANGED
Base branch: current-stack-dev-backtest-2016-2024-v3
Audit branch: audit/risk-contract-compatibility-2026-11-12

## Executive decision

The repository contains two intentionally distinct risk scopes. They must not be merged:

1. Canonical Decision Brain / governed runtime contract: minimum 3R, implemented by `RUNTIME/RISK_ENGINE_INTEGRATION_V1/risk_engine_integration_v1.py`.
2. Frozen Candidate Evaluation contract: 0.75 ATR stop / 2R target, implemented by `OOS_2025/frozen_candidate_risk_profile_v1.py` and consumed by historical candidate replay and the Gate 3C single-event evaluation builder.

The 2R engine does not enforce a minimum RR. Its current role is execution geometry and frozen candidate evaluation, not the general 3R canonical gate. Gate 3C evidence must therefore be labelled and interpreted as evaluation_single_event / Candidate 2R proof, not as proof that the canonical 3R risk gate passed.

No evidence in this audit justifies changing the canonical 3R threshold to 2R.

## Compatibility matrix

| Path | Risk implementation | Contract | What it can prove |
|---|---|---|---|
| BACKTEST/GOVERNED_E2E_ORCHESTRATOR_V1.py | RUNTIME/RISK_ENGINE_INTEGRATION_V1 | 3R | Governed canonical risk evaluation when this orchestrator is executed and its gate passes |
| BACKTEST/GOVERNED_E2E_ORCHESTRATOR_V2.py | RUNTIME/RISK_ENGINE_INTEGRATION_V1 | 3R | Governed canonical risk evaluation; explicit target distance is 3x stop distance |
| BACKTEST/GOVERNED_E2E_RUNNER_V1.py | RUNTIME/RISK_ENGINE_INTEGRATION_V1 | 3R | Runner integration through canonical execution plan and risk evaluation |
| BACKTEST/GOVERNED_CANONICAL_RUNNER_V3.py | RUNTIME/RISK_ENGINE_INTEGRATION_V1 | 3R | Validation of supplied SL/TP against canonical risk contract |
| DEVELOPMENT_2016_2024/current_stack_historical_replay_v4.py | risk_engine/risk_execution_runtime_v1.py plus frozen candidate profile | 0.75 ATR / 2R | Candidate replay path only; it does not prove canonical 3R |
| DEVELOPMENT_2016_2024/current_stack_historical_replay_v5_4.py | V5.4 local frozen candidate implementation plus risk_execution_runtime_v1.py | 0.75 ATR / 2R | Candidate replay path only; see regression below |
| OOS_2025/build_single_event_risk_evidence_v1.py | frozen_candidate_risk_profile_v1.py plus risk_execution_runtime_v1.py | 0.75 ATR / 2R | One pre-2025 event, explicit evaluation account bootstrap; authority scope is evaluation_single_event |
| RUNTIME/DECISION_RUNTIME_V1/gate3c_single_event_e2e_v1.py | consumes authoritative risk evidence; no independent RR calculation | inherited input scope | Brain integration for supplied evidence; does not independently prove 3R |
| .github/workflows/gate3c-single-real-event-e2e-v2.yml | invokes single-event builder and bridge | 0.75 ATR / 2R evaluation evidence | Integration-contract check, not canonical 3R acceptance |

## Confirmed findings

### A. Canonical 3R implementation is present

`risk_engine_integration_v1.py` defines:
- `CURRENT_CANONICAL_MIN_RR = 3.0`
- 0.5–4.0 ATR stop-distance bounds
- 5% drawdown circuit breaker
- risk budget limits and loss-streak risk reduction
- a 1e-12 absolute tolerance only for floating-point representation at the exact 3R boundary

The reconciliation tests explicitly verify exact 3R passes and materially sub-3R fails. This supports the 3R unit-level contract. It does not, by itself, prove that every complete orchestrated event path has been executed successfully.

### B. Candidate 2R is explicitly scoped separately

`OOS_2025/frozen_candidate_risk_profile_v1.py` documents that its 0.75 ATR / 2R profile is evaluation-only and must not redefine the canonical Risk Engine or three-book mode.

`risk_engine/risk_execution_runtime_v1.py` validates finite inputs, supported risk profiles, stop mode, locked risk budget, positive stop/target and stop/ATR range. It does not calculate or enforce a minimum reward:risk ratio. Therefore a positive target alone is not proof of a 2R or 3R policy unless the calling layer validates the ratio.

### C. V5.4 has a confirmed risk-control regression

V4 loads and calls `OOS_2025/frozen_candidate_risk_profile_v1.py`, whose risk evaluation includes the 5% drawdown circuit breaker.

V5.4 defines its own `evaluate_frozen_candidate_risk` and patches the imported frozen profile to use that local implementation. The V5.4 local function does not calculate drawdown or enforce `DRAWDOWN_BREAKER_PCT`. Consequently, an account state at or beyond the frozen 5% drawdown threshold can pass this local candidate risk function if its other inputs pass.

The existing `DEVELOPMENT_2016_2024/test_v5_4_contract.py` verifies 0.75 ATR / 2R geometry and Nison optionality, but does not test drawdown-block behavior. This is a test-coverage gap around a real behavioral regression.

The V5.4 wrapper's exact-match replacement for `take_profit_distance=rr_target` replaces that line with itself. It is a no-op guard, not an execution change. The resulting target calculation `TP_R * (SL_ATR * ATR)` is mathematically 2R with a 0.75 ATR stop, consistent with the frozen candidate contract. The prior note's characterization of 1.5*ATR as a distinct target defect is therefore not supported by this exact source comparison alone.

### D. Gate 3C does not prove the canonical 3R gate

`build_single_event_risk_evidence_v1.py`:
- restricts the event timestamp to 2016–2024;
- invokes the frozen candidate profile;
- uses stop = 0.75 ATR and reward = 2 x stop;
- cross-checks SL, TP and position size against the separate Risk Execution Runtime;
- labels the evidence `authority_scope = evaluation_single_event`.

The Gate 3C bridge checks that risk evidence is present and authoritative, but it does not independently compute RR >= 3. The workflow's integration validation checks that risk evidence is authoritative, but does not require `risk_pass is True` or `rr >= 3`. A valid NO_TRADE result is intentionally allowed to count as integration-contract PASS, as documented in the preflight note. Therefore that PASS is not proof of a successful risk approval or of the 3R canonical contract.

This is consistent with the historical Gate 3C log, which explicitly scopes its proof to one pre-2025 event and the frozen 0.75 ATR / 2R candidate profile. The label "canonical event input" refers to the event envelope/build contract, not to the 3R risk policy.

## Required repair and verification sequence

1. Preserve both policy scopes: canonical 3R remains unchanged; candidate evaluation remains 2R and separately labelled.
2. Repair V5.4 so the local candidate evaluator preserves all frozen candidate controls, especially the 5% drawdown circuit breaker. Prefer a single source of truth or an exact parity test against the frozen profile; do not silently maintain divergent implementations.
3. Add V5.4 tests proving drawdown below threshold can proceed and drawdown at/above 5% blocks, alongside existing 0.75 ATR / 2R geometry checks.
4. Tighten Gate 3C reporting and validation so the workflow explicitly reports the evidence scope and distinguishes:
   - integration-contract PASS,
   - risk approval PASS/BLOCK,
   - Brain decision EXECUTABLE/NO_TRADE/NOT_EXECUTABLE.
   Do not force a BUY/SELL outcome merely to satisfy a gate.
5. Add an independent single-event test of the canonical 3R path: exact 3R passes, materially below 3R fails, and the event is actually routed through the canonical 3R integration path.
6. Only after these focused repairs and tests pass, run one governed development event, then a small deterministic sample, then the governed 2016–2024 replay.
7. Keep all 2025 OOS data, scripts, thresholds and results untouched. Do not use 2025 for tuning or calibration.

## Explicit non-actions

- No changes to Murphy, Nison, Similarity, Memory, TIZ or Decision Brain direction semantics.
- No change from 3R to 2R in the canonical risk contract.
- No promotion of Candidate 2R evidence into canonical 3R proof.
- No 2016–2024 full backtest or profitability claim during this audit.
- No edits to 2025 OOS data or calibration.
- No runtime code was changed in this audit commit.

## Evidence files inspected

- `RUNTIME/RISK_ENGINE_INTEGRATION_V1/risk_engine_integration_v1.py`
- `RUNTIME/RISK_ENGINE_INTEGRATION_V1/test_risk_engine_contract_reconciliation_v1.py`
- `AUDITS/RISK_EXECUTION_CONTRACT_RECONCILIATION_2026-08-29.md`
- `risk_engine/risk_execution_runtime_v1.py`
- `risk_engine/test_risk_execution_runtime_v1.py`
- `OOS_2025/frozen_candidate_risk_profile_v1.py`
- `OOS_2025/build_single_event_risk_evidence_v1.py`
- `DEVELOPMENT_2016_2024/current_stack_historical_replay_v4.py`
- `DEVELOPMENT_2016_2024/current_stack_historical_replay_v5_4.py`
- `DEVELOPMENT_2016_2024/test_v5_4_contract.py`
- `OOS_2025/full_decision_brain_assembler_v1.py`
- `RUNTIME/DECISION_RUNTIME_V1/full_brain_runtime_bridge_v1.py`
- `RUNTIME/DECISION_RUNTIME_V1/gate3c_single_event_e2e_v1.py`
- `.github/workflows/gate3c-single-real-event-e2e-v2.yml`
- `PROJECT_LOGS/GATE3C_RISK_BRIDGE_PASS_2026-08-30.md`
- `audits/GATE3C_PREFLIGHT_CONTRACT_NOTE_2026-08-30.md`
