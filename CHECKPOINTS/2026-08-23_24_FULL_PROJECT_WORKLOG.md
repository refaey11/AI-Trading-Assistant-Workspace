# AI Trading Assistant — Full Worklog / Checkpoint

Date window: 2026-08-23 through 2026-08-24 (project timezone +03:00)
Purpose: Preserve a single chronological record of the work performed, failures found, resolutions, current verified state, and the remaining Final OOS performance path.

## 1. Starting governance / source-of-truth boundaries
- 2025 remains OOS and must not be used for tuning, calibration, threshold selection, or operator selection.
- Murphy = technical context / market structure; Nison = confirmation/context and cannot generate direction; TIZ = process/psychology evidence boundary and direction-neutral; Similarity Memory = historical evidence only and not the sole decision maker; Risk = hard execution gate.
- Existing project knowledge was audited and integrated; no blanket rebuild of Murphy/Nison semantics was introduced.
- The project had a corrected Murphy baseline of 34/35 runtime-verified rules, with Murphy 0008 governed separately as blocked in the later corrected baseline documentation. This state was explicitly recorded in GitHub.
- Nison baseline was recorded as 44/44 source-frozen and runtime-verified.

## 2. Nison 2025 producer / CI recovery
- The governed Nison 2025 producer boundary was connected to the existing 44-rule runtime path (PR #39, merged).
- A full 78-rule 2025 coverage boundary was executed (PR #44, merged): 34 Murphy + 44 Nison rule slots; missing evidence stays NOT_EVALUABLE / NO_2025_OUTPUT.
- The governed 78-rule Decision-Event Stream was then merged (PR #43, merged), preserving existing outputs and NOT_EVALUABLE semantics. Main merge commit: b2668e23863fb47bc31c70b7593434fd5686201d.

## 3. TIZ ambiguity was resolved without changing canonical semantics
- PR #42 merged the TIZ boundary resolution.
- Canonical three-book mode remains fail-closed when authoritative TIZ process evidence is unavailable.
- An isolated OOS evaluation mode may continue with an explicit unverified-TIZ state, but TIZ remains direction-neutral and cannot generate/override BUY/SELL.
- This resolved the earlier project problem where TIZ could not be treated as a market-derived signal.

## 4. Risk / execution integration
- Risk Execution Runtime V1 was merged as a fail-closed runtime using only already-specified Risk Engine gates/formulas.
- The isolated OOS V2+4H candidate protocol was frozen for evaluation only: 0.75 ATR stop and 2R target. This is not the canonical official baseline.

## 5. Murphy 0021 — 2025 fresh producer run and failures
Branch: oos-2025-murphy-0021-fresh-v1 (PR #45)

### Failure A — wrong source filename / path
- CircleCI first failed because the CI path referenced GBPUSD_M1_MASTER_2016_2026_V1(1).zip while the canonical file name was GBPUSD_M1_MASTER_2016_2026_V1.zip.
- The source/filename mismatch was corrected; no Murphy semantics or thresholds were changed.

### Failure B — Dropbox 401 Unauthorized
- After the source-name fix, Murphy and Nison CI jobs failed with 401 Unauthorized during authoritative 2025 source acquisition.
- Root cause: the CircleCI Dropbox credential path was not authorized. The Dropbox access credential was refreshed in the project environment.
- This was a CI credential problem, not a Murphy/Nison semantic problem.

### Failure C — 384 missing H1 volume-context rows
- Once acquisition worked, Murphy producer verification failed because 384 2025 H1 rows lacked canonical M1-derived volume context.
- Correct behavior was to fail-closed / treat missing evidence as NOT_EVALUABLE rather than invent a volume proxy or fallback.
- The producer was adjusted so missing volume context is represented explicitly and counted in the manifest instead of causing unsafe fabricated evidence.
- No new thresholds, futures OI proxy, direction logic, or 2025 tuning was added.

### Failure D — 2024->2025 boundary previous-close issue
- The regression test then failed because the first 2025 H1 row did not have previous_close after pre-2025 rows were discarded.
- Root cause: the boundary needs the last completed H1 observation before 2025 to support the first 2025 evaluation.
- Fix: preserve the required cross-year completed-observation state while keeping 2025 evaluation OOS and ensuring no future data is used.
- Murphy 0021 producer tests subsequently passed in CI.

### Result
- Murphy 0021 fresh 2025 producer path passed its dedicated CI verification after the above fixes.
- PR #45 remains an evidence/producer integration branch; it is not a profitability result.

## 6. Main Decision Brain integration verification
After the governed 78-rule Decision-Event Stream was merged, the main branch CI suite ran successfully.
- decision_brain_v1_integration: SUCCESS
- decision_brain_final_e2e_readiness_v1: SUCCESS
- risk_execution_runtime_v1: SUCCESS
- tiz_optional_execution_adapter_v2: SUCCESS
- frozen_decision_2025_oos_evaluator_contract_v1: SUCCESS
- oos_2025_78_rule_coverage_v1: SUCCESS
- nison_2025_full_production_v1: SUCCESS
- all remaining listed runtime/contract/memory/market checks: SUCCESS
- At that point the technical integration gate was green; this did NOT mean a profitability result had been produced.

## 7. The important distinction established
The green Decision Brain E2E/integration gate proves technical connectivity and contract integrity. It does NOT provide Win Rate, Profit Factor, Expectancy, P&L, or Drawdown.
A separate Final OOS Performance Gate is required before any profitability claim.

## 8. Legacy backtest was correctly blocked from being called the Final result
- TRUE_BACKTEST_V2 was audited and explicitly gated from frozen OOS attribution.
- Its stored configuration uses a different candidate protocol and explicitly states costs were not yet applied.
- Therefore its stored PF / expectancy / total-R figures are historical diagnostic evidence only, not the official Decision Brain final performance result.
- Example stored values visible in the archive include V2/XAUUSD 4h PF 1.2814 and other mixed asset/horizon results; these must NOT be presented as the Final Decision Brain result.

## 9. Isolated 2025 core profitability diagnostic (NOT final)
The existing core profitability evaluation produced a diagnostic 2025 run:
- 2025 GBPUSD fresh M1 source: 372,632 rows.
- Existing 2025 Murphy rule smoke stream: 55,944 rule evaluations.
- Assembled event timestamps: 6,225.
- Core eligible timestamps after market-state join and a single unambiguous Murphy directional confirmation: 2,688.
- BUY: 1,411; SELL: 1,277.
- Nison in that isolated stream: NOT_EVALUABLE (no authoritative Nison evidence attached).
- TIZ optional/unverified in that isolated path.
- Entry at event close; stop 0.75 ATR20; target 2R; 4h subsequent M1 horizon; same-bar ambiguity none observed; costs/slippage not applied; concurrent portfolio rules not modeled.
- Result: 858 TP, 1,550 SL, 280 timeout, total +166R, PF 1.1071, TP hit rate 31.92%, max sequential outcome drawdown -40R.
- This run is explicitly diagnostic only and must not be represented as the final three-book Decision Brain result.

## 10. Final OOS performance gate was created
GitHub Issue #47 and Draft PR #48 were created to define the governed Final OOS performance gate.
Required protocol:
- Fold A: calibration 2016–2023 -> OOS 2024.
- Fold B: calibration 2016–2024 -> OOS 2025.
- Same signal definition, retrieval/index construction, feature definitions/availability, selection policy, SL/TP, ambiguity policy, execution timing, cost model, and missing-evidence handling across folds.
- Leakage checks must block future feature/memory/index state and prevent outcome leakage.
- Final report must publish 2024, 2025, and combined metrics: decisions/trades, PASS/FAIL/NOT_EVALUABLE, Win Rate, Profit Factor, Expectancy R, Net P&L/R, Max Drawdown, Costs, ambiguity counts, availability, skipped/missing evidence, and leakage result.
- Missing required inputs must block the run; no guessed values.

## 11. Final OOS runner implementation
PR #48 added:
- OOS_2025/FINAL_OOS_INPUT_CONTRACT_V1.json
- OOS_2025/final_oos_walk_forward_leakage_gate_v1.py
- PROJECT_STATE/FINAL_OOS_PERFORMANCE_GATE_V1.md
- tests/evaluation/test_final_oos_input_contract_v1.py
- tests/evaluation/test_final_oos_walk_forward_leakage_gate_v1.py
The runner is designed to accept two event-level fold CSVs and hard-fail on missing required columns, year contamination, duplicates, non-numeric R values, ambiguity mismatch, future feature availability, memory/index leakage, decision availability violations, and protocol mismatch across folds.

## 12. Critical data correction — Master GBPUSD M1 source is available
A fresh upload was made and independently verified in the current runtime:
File: GBPUSD_M1_MASTER_2016_2026_V1.zip
Contents:
- README.md
- VALIDATION_SUMMARY.json
- GBPUSD_M1_MASTER_2016_2026.csv
Verified validation summary:
- raw_rows_combined: 5,022,012
- master_rows: 3,908,322
- unique_timestamps: 3,908,322
- duplicate_rows_before_dedup: 742,460
- invalid_ohlc_rows_before_dedup: 0
- missing_ohlc_master: 0
- missing_volume_master: 0
- volume_available_rows: 2,420,041
- volume_unavailable_rows: 1,488,281
- first_timestamp: 2016-01-03 17:00:00
- last_timestamp: 2026-06-30 23:59:00
- gaps_gt_1min: 5,621
- largest_gap_minutes: 4,326
README provenance states: 2016–2019 historical M1 with volume unavailable; 2020–2026 Titan FX M1 with non-zero volume; overlapping timestamps are deduplicated preferring TitanFX; no synthetic candles and no gap filling; timezone is not assumed/converted without source metadata.
This source is sufficient to proceed with controlled extraction of 2024 and 2025 data, subject to the remaining governed event-stream construction requirements.

## 13. Current GitHub state
- Main technical Decision Brain integration merge: b2668e23863fb47bc31c70b7593434fd5686201d.
- PR #43 (78-rule Decision-Event Stream): merged.
- PR #44 (78-rule coverage execution): merged.
- PR #42 (TIZ boundary resolution): merged.
- PR #45 (fresh Murphy 0021 producer): open; producer/evidence work only.
- PR #46 (Murphy PF-B1/0008 governance reconciliation): open draft; 0008 is governed separately and is not being reopened for performance tuning.
- PR #48 (Final OOS performance gate): open draft; it defines and implements the final gate and is not itself a profitability result.

## 14. Problems encountered and how they were resolved
1. Wrong M1 filename in CI -> corrected source filename/path.
2. CircleCI Dropbox 401 -> project credential path refreshed; source acquisition resumed.
3. Missing canonical M1-derived H1 volume context -> fail-closed NOT_EVALUABLE handling; no fabricated proxy.
4. First-2025 previous_close regression -> preserve last completed pre-2025 boundary state.
5. Confusion between technical E2E success and profitability -> explicitly separated integration readiness from Final OOS performance.
6. Legacy backtest protocol mismatch / no costs -> blocked it from final attribution.
7. Missing formal two-fold event input contract -> added Final OOS input contract + leakage gate runner + tests.
8. Earlier uncertainty about the availability of the master M1 source -> resolved by the new verified master upload listed above.

## 15. What is actually finished now
- Three-book Decision Brain technical integration boundary: DONE/CI-verified.
- Governed 78-rule event-stream boundary: DONE/merged.
- Nison 44/44 runtime: recorded as verified.
- Murphy baseline: corrected to 34/35 runtime verified; 0008 remains governed separately per current reconciliation.
- TIZ canonical boundary resolution: DONE; optional OOS execution adapter exists without generating direction.
- Risk execution runtime: DONE/CI-verified.
- Fresh Murphy 0021 2025 producer: DONE/CI-verified after the documented failures/fixes.
- Final OOS gate specification/runner/tests: DONE.

## 16. What is NOT finished
- The official Final Decision Brain profitability result is NOT YET VALID.
- The two required fold-level event streams (2024 OOS and 2025 OOS) still need to be generated from the verified master data under one frozen protocol and joined to the governed Decision-Event Stream.
- Only after those inputs exist can the final runner emit the official 2024, 2025, and combined Win Rate / PF / Expectancy / Net R / Max DD / Costs report.

## 17. Next controlled action
Do not change Murphy, Nison, TIZ, Similarity, or Risk semantics for performance.
Use the verified GBPUSD M1 Master source to construct the required governed fold event streams, run the Final OOS walk-forward + leakage gate, inspect the report, and only then report the performance numbers.

## 18. Audit note
This worklog intentionally records both completed work and blockers. It does not convert diagnostic numbers into official performance claims and does not override the project's OOS governance.
