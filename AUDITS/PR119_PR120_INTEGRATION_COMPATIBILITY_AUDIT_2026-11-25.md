# PR #119 / #120 Integration Compatibility Audit — 2026-11-25

## Scope and safety
- Read-only review of PR #119 and PR #120 metadata, patches, pinned runtime files, and the GitHub Actions run/job logs available for their recorded heads.
- No runtime/source edits, no merge/rebase/cherry-pick, no workflow dispatch, no tests initiated by this audit, no broker connection or order.
- GitHub only. No Dropbox access, no market-data payloads, and no 2025/2026 dataset reads.
- 2025 remains locked OOS; this audit does not authorize any 2025 use for tuning, calibration, selection, or development.
- Findings are branch-pinned to PR #119 head `289b99cbf3567fd65b4fa7d507be24f2c50f07a3` and PR #120 head `d1df29b0d3526378402e47959a55a73b13bd1889`.

## 1. PR topology: stacked claim is stale
- PR #119 is open/draft, base `current-stack-dev-backtest-2016-2024-v3` at `34f2f8ca89d0cb1b437d0bdf8bd9fbfd7e5a2f6e`, head `289b99cbf3567fd65b4fa7d507be24f2c50f07a3`.
- PR #120 is open/draft, base `compatibility-remediation-time-risk-tiz-2026-11-16` at `59a6521544934fd770999f48ae757c0e73961d86`, head `d1df29b0d3526378402e47959a55a73b13bd1889`.
- The PR #120 base SHA is the merge-base of PR #119 and #120, not the current PR #119 head.
- Compare `289b99c...d1df29b`: status `diverged`, 8 commits ahead on #120 and 10 commits behind the #119 head. PR #120 is therefore not currently stacked on the latest #119 head, despite its description saying it is.
- No automatic retarget/rebase is recommended. First resolve the policy and code blockers below, then create a deliberate integration branch from the approved #119 head and replay/reconcile #120 changes with a compatibility audit.

## 2. Verification evidence: what actually passed
### PR #119 head `289b99c`
- Risk Contract Separation Tests: completed success; job log reports **57 passed**.
- TIZ Metadata-Only Compatibility: completed success; Actions run conclusion success (run #104).
- Current Stack Development Backtest V5.4: completed success; log says **V5.4 contract tests: PASS**. This ran `DEVELOPMENT_2016_2024/test_v5_4_contract.py`; it is not a full historical replay/backtest.
- MTF Source Gate Smoke: failed. The canonical acquisition contract test step reports **7 passed**, then the exact MTF archive download failed with HTTP **401**. Annual-file validation and the fail-closed MTF gate were skipped. No MTF source validation passed in this run.
### PR #120 head `d1df29b`
- Live Decision Runtime V1: completed success; job step `Test live runtime and canonical risk contract` succeeded.
- TIZ Metadata-Only Compatibility: completed success.
- These results establish only that the workflow's selected tests passed on the PR #120 head. They do not prove source authentication, correct authority boundaries, or live trading readiness.
- The #120 Actions runs checked here are tied to `d1df29b`; they do not test a merged/rebased combination with the latest #119 head.

## 3. Blocking policy contradiction: TIZ
- Checked-in `03_TIZ/TIZ_RUNTIME_BOUNDARY_RESOLUTION_V2.json` says it is superseded by the 2026-11-12 decision and explicitly defines TIZ as optional audit metadata only.
- It explicitly prohibits TIZ from blocking/allowing a trade, changing confidence/risk/size, or making missing/failed TIZ evidence block runtime.
- PR #120 nevertheless requires `tiz_evidence`, validates its source envelope, invokes `evaluate_tiz_gate`, and returns BLOCKED unless process state is READY.
- PR #120 test `test_live_runtime_blocks_tiz_process_failure` codifies the contradictory blocking behavior.
- This is a direct contract violation. Do not merge #120 as-is. Remediation must make TIZ optional metadata only: missing, failed, or NOT_EVALUABLE TIZ cannot block, allow, or alter direction/confidence/risk/eligibility. Do not synthesize READY.

## 4. Blocking directional-authority violation: Murphy is not the sole direction source
- PR #120 calls recovered Brain V1 with the MTF row: `brain.assess(normalized_row, similarity=None)`.
- Recovered Brain V1 derives bullish/bearish evidence and `directional_bias` from `mtf_trend_score` and six `*_trend_regime` values; volume may add bullish evidence.
- The Three-Book evaluator then chooses BUY/SELL from Brain bias and only checks Murphy for PASS and directional conflict.
- PR #120's final equality check against Murphy catches disagreement, but agreement does not establish that the direction was generated from Murphy.
- This violates the project invariant that Murphy owns market direction and MTF is contextual input, not an independent directional authority.
- Remediation must prevent raw MTF/volume fields from independently creating or changing final direction. Direction must be sourced from governed Murphy evidence/rule provenance; MTF can remain non-authoritative context/validation only. Nison remains confirmation/contradiction only.

## 5. Brain no-trade reasons are collected but not enforced
- PR #120 serializes `assessment.no_trade_reasons` into `brain_assessment`.
- The evaluator does not inspect `no_trade_reasons`; PR #120 does not apply a separate gate to them.
- The recovered Brain adds a no-trade reason whenever volume confirmation is unavailable, and also for neutral/conflicted evidence or low confidence.
- Consequently the runtime can potentially proceed to SIGNAL_READY while the Brain reports one or more no-trade reasons, depending on other evaluator checks.
- This requires an explicit governed contract: determine which Brain reasons are absolute no-trade blockers versus informational metadata. Until that decision and tests exist, do not treat the collected list as an enforced gate or claim the runtime honors it.

## 6. Source authenticity and freshness gaps
- PR #120's `_require_source_envelope` accepts caller-supplied `authoritative=True` plus non-empty source/producer strings and `available_at <= as_of`.
- It does not authenticate those strings against a producer registry, signed manifest, immutable artifact digest, producer configuration, or verified lineage.
- Exact equality between `mtf_evidence.fields` and `brain_row` proves only that the two caller-supplied copies match; it does not authenticate how the MTF values were produced or their encoding semantics.
- PR #120 rejects timestamps more than five minutes in the future but has no maximum age for the event or source evidence. Old 2026 events can remain eligible if the caller supplies a matching old `available_at`.
- Add governed source/producer authentication and explicit maximum event/source age before any live eligibility claim.

## 7. PR #119 violates the GitHub-only project constraint and has an OOS scope hazard
- PR #119's GitHub Actions MTF workflow reads `DROPBOX_ACCESS_TOKEN` and downloads `/MTF_ALIGNMENT_GBPUSD_V1.zip` from Dropbox. The observed run failed at this step with HTTP 401.
- PR #119's CircleCI source-acquisition helper still uses `DROPBOX_ACCESS_TOKEN` and downloads several source archives from Dropbox. This conflicts with the user's explicit GitHub-only instruction.
- The same CircleCI source map includes `GBPUSD_H1_2016_2025_MASTER.zip`; the frozen-scope check asserts H1 data reaches year 2025. This is a static pipeline hazard against the locked 2025 OOS boundary. This audit did not execute the pipeline or read that dataset.
- Do not run these CircleCI acquisition/backtest paths. Replace them only through a separately reviewed GitHub-hosted, immutable, range-isolated source-manifest design that proves 2016–2024 selection without opening or scanning 2025/2026 payloads. Do not move the data to GitHub without reviewing repository size, privacy, licensing, and artifact access controls.

## 8. Risk and execution boundaries
- PR #120 imports the canonical risk integration, which exposes a 3R minimum, 0.5–4 ATR stop range, and drawdown breaker. The #120 Actions test succeeded, including its canonical risk contract test.
- The output remains `SIGNAL_ONLY`, `orders_enabled=False`, and `broker_volume=None`; no MT5 order adapter is connected.
- This is a useful safety boundary, not a production readiness certificate. Broker-specific lot sizing, MT5 Demo execution, and end-to-end order lifecycle remain unimplemented.
- Preserve canonical 3R. Do not substitute the separate candidate/evaluation 2R protocol.

## 9. Required remediation sequence
1. Record the policy resolution: TIZ optional metadata only; Murphy exclusive direction authority; Similarity historical evidence only; Risk hard gate; Nison confirmation only; 2025 OOS locked.
2. Keep PR #119 and #120 open/draft. Do not merge either as-is.
3. Retire Dropbox-dependent CI acquisition paths from the approved workflow; do not dispatch or run CircleCI acquisition/backtest jobs.
4. Design and approve a GitHub-only, immutable source manifest and a 2016–2024-only source selection process that cannot read 2025/2026 payloads. Keep producer semantics/timezone lineage explicitly NOT EVALUABLE until authenticated.
5. Remediate #120 in an isolated integration branch based on the approved latest #119 head: remove TIZ from required/blocking flow; prevent MTF/volume from generating final direction; define/enforce Brain no-trade reasons; add producer authentication and max event age.
6. Add adversarial tests for missing/failed TIZ non-blocking behavior, MTF/volume directional inertness, Murphy direction provenance, no-trade reasons, forged source envelope, stale event/source, 3R enforcement, and SIGNAL_ONLY/no-orders.
7. Run only the targeted GitHub Actions tests after checking triggers and ensuring no Dropbox/data acquisition path can run. Verify exact head SHA and job logs before recording results.
8. Only after all compatibility gates pass should a new PR be considered. No merge or live execution is authorized by this audit.

## Final status
- PR #119: **DRAFT / NOT MERGE-READY** — Risk contracts pass; MTF acquisition fails; Dropbox dependency conflicts with GitHub-only governance.
- PR #120: **DRAFT / NOT MERGE-READY** — selected Actions pass, but TIZ blocking and non-Murphy directional authority are hard contract violations.
- Combined #119 + #120: **NOT INTEGRATION-READY** — stale stacked base, unresolved source lineage/authentication, freshness gap, and no-trade reason enforcement gap.
