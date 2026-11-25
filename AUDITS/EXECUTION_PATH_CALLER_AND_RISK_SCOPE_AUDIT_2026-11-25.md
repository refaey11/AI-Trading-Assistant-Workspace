# Execution Path, TIZ Boundary, and Risk Scope Audit — 2026-11-25

## Scope and branch
GitHub-only static review on `fix/similarity-direction-isolation-2026-11-25`.

Compared with `current-stack-dev-backtest-2016-2024-v3`:
- base / merge-base: `34f2f8ca89d0cb1b437d0bdf8bd9fbfd7e5a2f6e`
- branch: 14 commits ahead, 0 behind at review time.
- no PR opened, no merge/rebase/cherry-pick, no main changes.

This is a focused static source review, not a complete proof of every direct, dynamic, generated, or future caller. The GitHub code-search connector indexes the default branch, so its results cannot establish a complete branch-specific call graph.

## 1. Assembler path and BUY/SELL conversion
Inspected:
- `OOS_2025/full_decision_brain_assembler_v1.py`
- `compatibility/decision_brain_v1_handoff_adapter.py`
- `evaluation/three_book_decision_evaluator_v1.py`
- `RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py`

Observed:
1. The assembler calls `assess_with_governance`, then `evaluate_three_book_decision`.
2. The evaluator maps Brain `directional_bias == bullish` to BUY and `bearish` to SELL after allowlist, Murphy PASS, no Murphy/Brain conflict, Risk pass + stop loss, and no Nison contradiction.
3. The recovered Brain's directional bias is calculated from signed `mtf_trend_score` and the mean of six signed trend-regime fields. Positive volume can add bullish evidence; zero/negative volume is neutral in the inspected implementation.
4. The evaluator's Murphy check is a consistency check. It does not prove that Brain direction originated from Murphy.
5. The handoff passes Similarity as `None` into Brain; historical memory remains audit evidence.

Finding: the inspected assembler/evaluator path remains Brain/market-row-direction-led with Murphy agreement validation, not a proven Murphy-exclusive direction-authority path. This conflicts with the Master Map's Murphy directional authority unless an explicit governance amendment authorizes MTF-derived direction.

## 2. TIZ: assembler/evaluator vs legacy event builder
Observed:
- Assembler and evaluator explicitly describe TIZ as optional metadata only.
- The evaluator tests include absent TIZ and `NOT_READY` TIZ while still allowing BUY when the other inputs pass.
- `OOS_2025/execution_oos_compatibility_v1.py` delegates to `execution_oos_adapter_v1.py`; the latter does not consume TIZ for execution eligibility.
- Separately, `ADAPTERS/rule_adapter_execution_bridge_v1.py::build_execution_event` requires `trading_zone.process_state == READY` as part of its `executable` predicate.

Finding: TIZ metadata-only semantics are consistent within the assembler/evaluator/execution-plan path inspected, but conflict with the separate legacy `build_execution_event` helper. This audit does not establish that the helper is called by the active Gate 3C path. Do not silently change it until its callers and canonical policy are confirmed.

## 3. Risk scope and 2R vs canonical 3R
Inspected:
- `OOS_2025/build_single_event_risk_evidence_v1.py`
- `OOS_2025/frozen_candidate_risk_profile_v1.py`
- `OOS_2025/execution_oos_adapter_v1.py`
- `risk_engine/risk_execution_runtime_v1.py`

Observed:
1. The single-event builder labels its result `authority_scope: evaluation_single_event` and `frozen_candidate_contract: 0.75_ATR_stop_2R_target`.
2. The frozen candidate profile explicitly says it must not redefine canonical Risk Engine or canonical three-book mode.
3. The execution-plan adapter is evaluation mechanics only; it sets SL to 0.75 ATR and TP to 2.0R, and consumes an already-approved direction plus Risk pass.
4. The inspected canonical Risk Engine validates frozen risk profiles, stop distance 0.5–4 ATR, and positive TP distance, but this function does not itself enforce a minimum RR of 3.0.

Finding: the 2R path is an evaluation candidate protocol, not proof that the canonical production minimum RR changed. Keep it separate from the project's canonical 3R requirement. Do not infer production eligibility from Gate 3C's evaluation-scoped result.

## 4. Caller-path coverage
Confirmed source paths inspected:
- Gate 3C E2E calls `full_brain_runtime_bridge_v1.run_full_brain_cycle`.
- The bridge calls the assembler.
- The assembler calls the governed handoff, three-book evaluator, and evaluation execution-plan adapter.
- A separate adapter exposes `build_execution_event`; no claim is made here that this is part of the active Gate 3C path.
- Existing knowledge handoff / historical producer paths have separate call structures documented in prior branch audits.

Coverage limitation: this is not an exhaustive whole-branch call graph. No recursive branch-tree export was available through the connected GitHub operations in this review, and default-branch code search cannot prove absence of additional callers. Before changing any public helper, enumerate every caller from a branch-pinned repository tree or local checkout and inspect dynamic imports/entrypoints.

## 5. Decisions and blockers before code changes
1. Confirm whether Murphy is the sole directional authority, or formally amend the Master Map to authorize MTF/Brain-derived direction.
2. Confirm one canonical TIZ policy across assembler, execution plan, and legacy event builder.
3. Preserve canonical 3R separately from the frozen evaluation-only 2R candidate.
4. Establish the branch-pinned complete caller list for `build_execution_event`, `run_full_brain_cycle`, and `assemble_decision_event`.
5. Then add direct-call fail-closed tests at the public bridge and event-builder boundaries, without changing recovered Brain V1 or frozen rule semantics.

## 6. Safety / execution status
- Static source inspection only.
- No runtime/source implementation changed.
- No tests or workflows run.
- No market-data payloads accessed.
- 2025 OOS and 2026 market data untouched.
- No live trading, broker connection, or automatic order execution enabled.
- No PR created or merged.
