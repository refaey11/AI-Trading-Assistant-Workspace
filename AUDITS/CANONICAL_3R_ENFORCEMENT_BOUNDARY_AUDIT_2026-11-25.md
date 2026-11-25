# Canonical 3R Enforcement Boundary Audit — 2026-11-25

## Scope
GitHub-only, branch-pinned static inspection. Working branch: `fix/similarity-direction-isolation-2026-11-25`.
Compared with `current-stack-dev-backtest-2016-2024-v3`: 16 commits ahead, 0 behind at inspection time; merge base `34f2f8ca89d0cb1b437d0bdf8bd9fbfd7e5a2f6e`.

This audit checks where canonical minimum RR=3R is actually enforced, how the frozen evaluation-only 2R path is separated, and whether authority metadata is sufficient at the Gate 3C boundary.

No runtime/source implementation changed. No tests or workflows were run. No market-data payloads were accessed. 2025 OOS and 2026 market data were not accessed. No PR, merge, rebase, cherry-pick, or main-branch change occurred.

## 1. Canonical 3R implementation exists on PR #119's separate head
Inspected PR #119 head commit `05667a1e0c8ad67eca926fba345a99bcc204b699` (draft/open; separate branch `compatibility-remediation-time-risk-tiz-2026-11-16`), including:
- `RUNTIME/RISK_ENGINE_INTEGRATION_V1/risk_engine_integration_v1.py`
- `tests/risk_engine/test_risk_contract_separation_v1.py`
- `AUDITS/PR119_COMPATIBILITY_AUDIT_2026-11-16.md`
- `BACKTEST/GOVERNED_CANONICAL_RUNNER_V3.py`
- `BACKTEST/GOVERNED_INTEGRATION_GATE_V3.py`

The PR #119 canonical integration explicitly sets `CURRENT_CANONICAL_MIN_RR = 3.0`. It calculates RR from the supplied stop/target bracket, rejects RR below 3R, rejects non-finite inputs/outputs, enforces 0.5–4 ATR stop distance and the drawdown breaker, and rejects invalid stop/target orientation.

Its separation tests explicitly require:
- canonical 3R: PASS;
- canonical 2R: FAIL;
- canonical 1.5R: FAIL;
- separate candidate Risk Engine's frozen 2R profile: PASS.

The PR #119 audit states that the development execution bridge was hardened to require generated execution levels to match canonical Risk output and RR >= canonical minimum. PR #119's own body reports 57 Risk Contract Separation tests passed on its latest head; that status was read from the PR description and was not rerun in this audit.

## 2. The inspected Gate 3C route on this working branch is a different, evaluation-only 2R path
On `fix/similarity-direction-isolation-2026-11-25`, the inspected chain is:
`gate3c_single_event_e2e_v1.py` -> `full_brain_runtime_bridge_v1.py` -> `full_decision_brain_assembler_v1.py` -> `three_book_decision_evaluator_v1.py` -> `execution_oos_compatibility_v1.py` -> `execution_oos_adapter_v1.py`.

The Gate 3C risk builder:
- uses `OOS_2025/frozen_candidate_risk_profile_v1.py`;
- creates a 0.75 ATR stop / 2R target;
- calls `risk_engine/risk_execution_runtime_v1.py`, whose contract checks positive TP distance and 0.5–4 ATR stop range but does not enforce 3R;
- emits `rr: 2.0`, `authority_scope: evaluation_single_event`, and `frozen_candidate_contract: 0.75_ATR_stop_2R_target`;
- also emits `authoritative: true`.

The frozen candidate profile itself explicitly says it must not redefine canonical Risk or canonical three-book mode. The execution adapter fixes SL=0.75 ATR and TP=2R and consumes an already-approved action plus `risk_pass=True`.

## 3. Gate 3C does not validate canonical RR or evaluation scope at its input boundary
The inspected Gate 3C runner requires the Risk mapping to contain `authoritative`, `risk_pass`, account fields, entry, SL, TP and ATR, and checks `authoritative is True`. It does not require or validate:
- `authority_scope == evaluation_single_event` for the candidate path;
- `rr == 2.0` for the frozen candidate path;
- `rr >= 3.0` for a canonical path;
- canonical Risk producer identity or canonical Risk result provenance;
- SL/TP equality with a canonical 3R Risk result.

The assembler/evaluator checks Risk pass and presence of SL, but does not enforce an RR threshold. The evaluator's unit fixture even supplies `rr: "2.0"` with `risk_pass: true` and expects BUY; this demonstrates that RR enforcement is not the evaluator's responsibility. The execution adapter then constructs its own 2R bracket.

Interpretation: this Gate 3C chain is an evaluation/development candidate path, not a canonical 3R production path. The `authoritative: true` flag on an evaluation-scoped 2R record is potentially ambiguous if any downstream consumer treats that boolean as general production authorization without also checking scope and producer contract.

## 4. Canonical 3R is not proven to be wired into this Gate 3C chain
The PR #119 canonical 3R integration is a separate module and separate branch. The inspected Gate 3C builder on the working branch imports `risk_engine/risk_execution_runtime_v1.py`, not `RUNTIME/RISK_ENGINE_INTEGRATION_V1/risk_engine_integration_v1.py`.

The inspected PR #119 `BACKTEST/GOVERNED_CANONICAL_RUNNER_V3.py` does call the canonical 3R integration, but it is a different historical runner. Its existence does not prove the Gate 3C event path or any live runtime path calls it.

PR #120's draft description claims a separate Live Decision Runtime V1 uses canonical Risk (minimum 3R) and is SIGNAL_ONLY with orders disabled. That is a PR-description claim, not an independent code-path verification in this audit. PR #120 is stacked on PR #119 and remains subject to the stated merge order and unresolved MTF producer gate.

## 5. Additional boundary observations
- `RUNTIME/DECISION_RUNTIME_V1/full_brain_runtime_bridge_v1.py` only checks Risk `authoritative=True`; it does not validate RR, scope, or canonical Risk producer identity.
- `evaluation/three_book_decision_evaluator_v1.py` checks Risk pass and stop loss, not RR or authority scope.
- `ADAPTERS/rule_adapter_execution_bridge_v1.py::build_execution_event` checks a Risk pass and TIZ READY, but does not itself calculate or enforce RR. Its active caller path remains unproven.
- This review is not an exhaustive branch-wide caller inventory. Default-branch code search cannot prove absence of additional branch-specific/dynamic callers.

## 6. Required closure before calling the boundary safe
1. Keep Gate 3C's 2R result explicitly evaluation-only and never treat its `authoritative: true` boolean as production authorization.
2. At every production-eligible entry point, require a canonical Risk result from the 3R integration, verify its scope/producer identity, and verify SL/TP match that result.
3. Add fail-closed tests for a 2R evaluation-scoped record presented to a production boundary, including the case where `authoritative=True`.
4. Add tests proving canonical 3R passes and 2R/1.5R fail at each production-eligible boundary, not only inside the isolated canonical Risk function.
5. Enumerate all callers of `build_single_event_risk_evidence_v1`, `build_execution_plan`, `build_execution_event`, and `run_full_brain_cycle` from a branch-pinned complete tree before changing public boundaries.
6. Preserve PR #119's 3R vs candidate 2R separation. Do not copy or merge PR #119/PR #120 changes without the established review and merge order.

## Status
- Canonical 3R Risk implementation and isolated contract tests: PRESENT on PR #119 head.
- 3R enforcement in the inspected PR #119 canonical Risk function: PRESENT.
- 3R enforcement in the working branch's Gate 3C evaluation path: NOT PRESENT / NOT REQUIRED FOR ITS DECLARED 2R EVALUATION CONTRACT.
- Production boundary rejecting evaluation-scoped 2R even when `authoritative=True`: NOT PROVEN.
- Canonical 3R integration wired into Gate 3C: NOT PROVEN; inspected Gate 3C path uses the separate candidate engine.
- Complete caller inventory: OPEN.
- Implementation edits/tests/workflows: none.
