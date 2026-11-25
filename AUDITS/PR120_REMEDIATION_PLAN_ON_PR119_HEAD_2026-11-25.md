# PR #120 Remediation Plan on Latest PR #119 Base
Date: 2026-11-25
Status: PLAN ONLY — no runtime implementation or merge authorization

## 1. Verified branch topology

- PR #119 is open/draft. Its live GitHub head is `289b99cbf3567fd65b4fa7d507be24f2c50f07a3` on `compatibility-remediation-time-risk-tiz-2026-11-16`, based on `current-stack-dev-backtest-2016-2024-v3`.
- PR #120 is open/draft. Its head is `d1df29b0d3526378402e47959a55a73b13bd1889` on `feature/live-decision-runtime-v1`, based on the older `compatibility-remediation-time-risk-tiz-2026-11-16` base at `59a6521544934fd770999f48ae757c0e73961d86`.
- Comparing PR #119 head to PR #120 head reports `diverged`: PR #120 is 8 commits ahead and 10 commits behind, with merge base `59a6521544934fd770999f48ae757c0e73961d86`.
- The compared PR #120-only file set is:
  - `.github/workflows/live-decision-runtime-v1.yml`
  - `RUNTIME/DECISION_RUNTIME_V1/live_decision_runtime_v1.py`
  - `RUNTIME/DECISION_RUNTIME_V1/test_live_decision_runtime_v1.py`
- This plan branch starts exactly from PR #119's current head. It does not merge, rebase, cherry-pick, or copy PR #120 code.

## 2. Non-negotiable governance contract

1. Murphy is the sole authority for directional bias. A BUY/SELL direction must be traceable to an eligible Murphy directional rule and its source provenance.
2. Nison is confirmation/contradiction only. It cannot originate or reverse direction.
3. Similarity / historical memory is evidence and audit metadata only. It must never affect direction, confidence, or eligibility.
4. MTF trend fields and volume fields are context/evidence only. They must not create, reverse, or strengthen directional bias or confidence independently of Murphy.
5. Risk is a hard gate. Canonical minimum reward:risk remains 3R; stop distance remains within the approved 0.5–4 ATR contract and drawdown controls remain active. Evaluation-only 2R candidate mechanics must remain separate and cannot authorize canonical decisions.
6. TIZ follows the checked-in 2026-11-12 resolution: optional metadata only; missing, failed, or non-READY TIZ must not block or authorize a decision. Do not manufacture a READY state.
7. 2025 remains locked OOS. No training, tuning, calibration, threshold selection, feature selection, or data access involving 2025/2026 historical payloads.
8. V1 remains SIGNAL_ONLY. No broker order, MT5 execution, or live-trading readiness is authorized by this plan.

## 3. Required remediation work

### R1 — Reconcile the PR base before code changes
- Treat PR #119 head `289b99cbf3567fd65b4fa7d507be24f2c50f07a3` as the proposed integration base only after its own blockers are resolved.
- Re-audit imports, contracts, and tests for the three PR #120 files against that exact base.
- Do not retarget PR #120 or merge/rebase either PR as a shortcut.
- Any implementation must live on a separate remediation branch created from the approved base and be submitted as a new draft PR.

### R2 — Make Murphy the only directional authority
- Stop using recovered Brain V1's MTF/volume-derived `directional_bias` as the BUY/SELL authority.
- Do not modify frozen book sources or invent a Murphy direction.
- Introduce an explicit, typed directional-authority handoff sourced from eligible Murphy evidence: direction, status, rule ID, source rule provenance, and authority proof must travel together.
- The decision/evaluator boundary must consume that Murphy-authorized direction. Brain market state, contradictions, and non-directional context may be retained as diagnostics only.
- Reject missing, ambiguous, conflicting, non-allowlisted, or provenance-incomplete Murphy direction.
- Verify that changing MTF trend values or volume values while holding Murphy evidence constant cannot change final direction, confidence, or eligibility.

### R3 — Remove TIZ from authorization
- Remove TIZ from required evidence-envelope loops and all blocking predicates.
- TIZ may be absent, malformed, failed, or non-READY without changing the decision result; record only safe optional metadata when valid.
- Keep explicit tests proving TIZ cannot authorize, block, change direction, change confidence, or change risk.
- Do not call the TIZ process gate to create a synthetic READY value.

### R4 — Enforce Brain no-trade reasons
- Define the contract for `assessment.no_trade_reasons` before changing behavior.
- A non-empty hard-block reason set must result in NO_TRADE unless a reviewed governance mapping explicitly classifies an item as informational.
- Preserve the original reasons in the output and expose the exact blocking reason.
- Add adversarial tests so SIGNAL_READY cannot coexist with an unresolved hard no-trade reason.

### R5 — Authenticate source provenance and freshness
- The current envelope's asserted `authoritative=True`, non-empty source/producer strings, and `available_at <= as_of` are not authentication.
- Define a trusted source/producer registry or verifiable manifest contract, including immutable artifact/version identity, producer version/config fingerprint, field schema, timezone/clock provenance, and source-to-event linkage.
- Reject forged or unregistered source claims. Do not treat a caller-supplied boolean as proof.
- Define an approved maximum event age and per-source freshness policy before implementation. Do not invent a numeric age threshold in code.
- Check event age, evidence age, and cross-source temporal alignment; fail closed when any required bound is absent or exceeded.

### R6 — Preserve risk and execution separation
- Keep canonical 3R enforcement on every SIGNAL_READY path.
- Explicitly test 2R and 1.5R rejection for canonical decisions, and preserve any evaluation-only 2R contract as a separate non-production scope.
- Keep output `SIGNAL_ONLY`, `orders_enabled=False`, and `broker_volume=None`.
- Do not connect MT5 or enable order submission in this remediation.

## 4. Required regression / adversarial test matrix

| Test | Required outcome |
|---|---|
| TIZ absent / invalid / failed / non-READY | No change to decision, direction, confidence, or eligibility |
| Murphy missing / non-PASS / unallowlisted / forged provenance | BLOCKED / NO_TRADE |
| Murphy BUY vs Murphy SELL with otherwise identical event | Direction follows the valid Murphy evidence only |
| MTF values changed while Murphy fixed | Direction, confidence, and eligibility unchanged |
| Volume values changed / unavailable while Murphy fixed | Direction, confidence, and eligibility unchanged |
| Similarity bullish / bearish / absent | Direction, confidence, and eligibility unchanged |
| Nison confirmed / absent | Confirmation strength may differ only under approved Nison contract; direction never changes |
| Nison contradicted | NO_TRADE |
| Non-empty hard Brain no-trade reasons | NO_TRADE |
| Forged source envelope / unregistered producer | BLOCKED |
| Stale event or stale source evidence | BLOCKED according to approved freshness policy |
| Canonical 3R | May pass only if every other gate passes |
| Canonical 2R / 1.5R | Rejected |
| Any accepted signal | SIGNAL_ONLY; orders disabled; no broker volume |

All tests must use synthetic fixtures or approved 2016–2024 development fixtures only. Never read or use 2025/2026 market-data payloads.

## 5. Safe implementation sequence

1. Resolve the governance contract and approve the unresolved policy items: hard vs informational Brain no-trade reasons, source registry/authentication design, and maximum event/source age.
2. Audit the three PR #120 files and every imported dependency against PR #119's exact head.
3. Add failing adversarial tests first, without altering frozen book sources.
4. Implement the smallest adapter/evaluator changes that satisfy Murphy-only direction, TIZ metadata-only, no-trade enforcement, and source/freshness gates.
5. Run only targeted GitHub Actions that do not download market-data archives or call Dropbox. Inspect workflow triggers before every push.
6. Verify results against the exact tested commit SHA and inspect job logs. A passing unit/contract workflow is not a historical replay, Demo execution test, or production-readiness proof.
7. Open a new draft PR for review. Do not merge without explicit approval and all governance gates passing.

## 6. Explicitly prohibited during this plan

- No edits to `main`, PR #119, or PR #120 branches.
- No merge, rebase, cherry-pick, or retarget of PR #120.
- No Dropbox access and no Dropbox-dependent acquisition workflow.
- No CircleCI source acquisition/backtest.
- No 2025/2026 historical market-data access.
- No full backtest launch, broker connection, Demo order, or live order.
- No profitability, readiness, or completion percentage claims.

## 7. Current result

This commit records a remediation plan only. It does not change runtime behavior, prove any tests pass, authenticate market-data sources, or authorize trading.
