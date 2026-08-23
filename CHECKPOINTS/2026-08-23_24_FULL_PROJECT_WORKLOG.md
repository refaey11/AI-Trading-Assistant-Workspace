# AI Trading Assistant — Full Worklog / Checkpoint

Date window: 2026-08-23 through 2026-08-24 (project timezone +03:00)
Purpose: Preserve a single chronological record of the work performed, failures found, resolutions, current verified state, and the remaining Final OOS performance path.

## 1. Starting governance / source-of-truth boundaries
- 2025 remains OOS and must not be used for tuning, calibration, threshold selection, or operator selection.
- Murphy = technical context / market structure; Nison = confirmation/context and cannot generate direction; TIZ = process/psychology evidence boundary and direction-neutral; Similarity Memory = historical evidence only and not the sole decision maker; Risk = hard execution gate.
- Existing project knowledge was audited and integrated; no blanket rebuild of Murphy/Nison semantics was introduced.
- The corrected current Murphy baseline is 34/35 runtime-verified; the current PF-B1/0008 reconciliation keeps 0008 separately governed/blocked rather than reopening the verified rule set for performance tuning.
- Nison baseline is 44/44 source-frozen and runtime-verified.

## 2. Nison 2025 producer / CI recovery
- PR #39 merged: governed Nison 2025 producer boundary connected to the existing 44-rule runtime path.
- PR #44 merged: current 78-rule 2025 coverage report executed; missing evidence stays NOT_EVALUABLE / NO_2025_OUTPUT.
- PR #43 merged: governed 78-rule Decision-Event Stream boundary (34 Murphy + 44 Nison), preserving existing outputs and NOT_EVALUABLE semantics. Main merge commit: b2668e23863fb47bc31c70b7593434fd5686201d.

## 3. TIZ ambiguity was resolved without changing canonical semantics
- PR #42 merged the TIZ boundary resolution.
- Canonical three-book mode remains fail-closed when authoritative TIZ process evidence is unavailable.
- An isolated OOS evaluation mode may continue with an explicit unverified-TIZ state, but TIZ remains direction-neutral and cannot generate/override BUY/SELL.

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
- The producer was adjusted so missing volume context is represented explicitly and counted in the manifest.
- No new thresholds, futures OI proxy, direction logic, or 2025 tuning was added.

### Failure D — 2024->2025 boundary previous-close issue
- The regression test failed because the first 2025 H1 row did not have previous_close after pre-2025 rows were discarded.
- Fix: preserve the last completed pre-2025 state needed for the first 2025 evaluation while keeping 2025 OOS and avoiding future data.
- Murphy 0021 producer tests subsequently passed in CI.

### Result
- Murphy 0021 fresh 2025 producer path passed dedicated CI verification.
- PR #45 remains evidence/producer integration; it is not a profitability result.

## 6. Main Decision Brain integration verification
After the governed 78-rule Decision-Event Stream was merged, the main technical suite was green.
- decision_brain_v1_integration: SUCCESS
- decision_brain_final_e2e_readiness_v1: SUCCESS
- risk_execution_runtime_v1: SUCCESS
- tiz_optional_execution_adapter_v2: SUCCESS
- frozen_decision_2025_oos_evaluator_contract_v1: SUCCESS
- oos_2025_78_rule_coverage_v1: SUCCESS
- nison_2025_full_production_v1: SUCCESS
- remaining listed runtime/contract/memory/market checks: SUCCESS

This technical green gate does NOT mean a profitability result exists.

## 7. Technical E2E vs profitability distinction
The Decision Brain E2E/integration gate proves technical connectivity and contract integrity. It does not produce Win Rate, Profit Factor, Expectancy, P&L, or Drawdown. A separate Final OOS Performance Gate is required.

## 8. Legacy backtest blocked from final attribution
TRUE_BACKTEST_V2 was audited and explicitly gated from frozen OOS attribution. Its stored configuration uses a different candidate protocol and explicitly says costs were not yet applied. Therefore its PF/expectancy/total-R figures are diagnostic/history only and are not the Final Decision Brain result.

## 9. Isolated 2025 core profitability diagnostic (NOT final)
Existing diagnostic 2025 run:
- fresh 2025 M1 source: 372,632 rows
- Murphy smoke evaluations: 55,944
- assembled timestamps: 6,225
- eligible timestamps with a single unambiguous Murphy directional confirmation: 2,688
- BUY 1,411 / SELL 1,277
- Nison: NOT_EVALUABLE in this isolated path
- TIZ optional/unverified
- entry at event close; 0.75 ATR20 stop; 2R target; 4h M1 outcome horizon; no same-bar ambiguity observed; costs/slippage not applied; concurrent portfolio rules not modeled
- result: 858 TP, 1,550 SL, 280 timeout, +166R, PF 1.1071, TP rate 31.92%, max sequential drawdown -40R

This remains a diagnostic only, not a final three-book Decision Brain performance result.

## 10. Final OOS performance gate
Issue #47 and Draft PR #48 define the governed Final OOS performance gate.
- Fold A: calibration 2016–2023 -> OOS 2024.
- Fold B: calibration 2016–2024 -> OOS 2025.
- Same signal definition, retrieval/index construction, feature availability, selection policy, SL/TP, ambiguity policy, execution timing, cost model, and missing-evidence handling across folds.
- Leakage checks must block future feature/memory/index state and prevent outcome leakage.
- Final report must publish 2024, 2025, and combined: decisions/trades, PASS/FAIL/NOT_EVALUABLE, Win Rate, Profit Factor, Expectancy R, Net P&L/R, Max Drawdown, Costs, ambiguity, availability, skipped/missing evidence, and leakage result.
- Missing required inputs must block the run; no guessed values.

## 11. Final OOS runner implementation
PR #48 added:
- OOS_2025/FINAL_OOS_INPUT_CONTRACT_V1.json
- OOS_2025/final_oos_walk_forward_leakage_gate_v1.py
- PROJECT_STATE/FINAL_OOS_PERFORMANCE_GATE_V1.md
- tests/evaluation/test_final_oos_input_contract_v1.py
- tests/evaluation/test_final_oos_walk_forward_leakage_gate_v1.py

The runner hard-fails on missing required columns, year contamination, duplicates, non-numeric R values, ambiguity mismatch, future feature availability, memory/index leakage, decision availability violations, and protocol mismatch across folds.

## 12. GBPUSD M1 Master source — verified in both current runtime and Dropbox
File: GBPUSD_M1_MASTER_2016_2026_V1.zip
Dropbox path: /GBPUSD_M1_MASTER_2016_2026_V1.zip
The same source is present in Dropbox and was also supplied as the current conversation upload.

Verified archive contents:
- README.md
- VALIDATION_SUMMARY.json
- GBPUSD_M1_MASTER_2016_2026.csv

Verified archive validation:
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

Year partitions verified locally from the master CSV:
- 2024: 373,339 rows; 2024-01-02 00:00:00 through 2024-12-31 23:59:00; volume_available rows: 373,339.
- 2025: 372,632 rows; 2025-01-02 00:00:00 through 2025-12-31 23:59:00; volume_available rows: 372,632.

Provenance in README:
- 2016–2019 historical M1, volume unavailable.
- 2020–2026 Titan FX M1, non-zero volume.
- overlapping timestamps deduplicated preferring TitanFX.
- no synthetic candles and no gap filling.
- timezone is not assumed/converted without source metadata.

This corrects the earlier mistaken statement that the M1 master was absent from Dropbox. It is present and verified.

## 13. Current GitHub state
- PR #43 merged.
- PR #44 merged.
- PR #42 merged.
- PR #45 open: fresh Murphy 0021 producer/evidence integration.
- PR #46 open draft: Murphy PF-B1/0008 governance reconciliation; no semantics/tuning changes.
- PR #48 open draft: Final OOS performance gate; it defines and tests the gate but is not itself a profitability result.

## 14. Problems encountered and how they were resolved
1. CI wrong M1 filename -> corrected source filename/path.
2. CircleCI Dropbox 401 -> project credential path refreshed.
3. Missing canonical M1-derived H1 volume context -> explicit NOT_EVALUABLE/fail-closed handling; no proxy invention.
4. First-2025 previous_close regression -> preserve last completed pre-2025 boundary state.
5. Confusion between technical E2E success and performance -> separate Final OOS performance gate.
6. Legacy backtest protocol mismatch/no costs -> blocked from final attribution.
7. Missing formal two-fold event contract -> final input contract + leakage gate runner + tests added.
8. Mistaken belief that the master M1 source was absent -> disproved by Dropbox search and local validation; master is available.

## 15. Actually finished
- Three-book Decision Brain technical integration boundary: DONE/CI-verified.
- Governed 78-rule Decision-Event Stream boundary: DONE/merged.
- Nison 44/44 runtime: verified.
- Murphy baseline: 34/35 runtime verified; 0008 governed separately by current reconciliation.
- TIZ canonical boundary resolution: DONE.
- Risk execution runtime: DONE/CI-verified.
- Fresh Murphy 0021 2025 producer: DONE/CI-verified after failures/fixes.
- Final OOS gate specification/runner/tests: DONE.
- GBPUSD M1 Master source: AVAILABLE and validated.

## 16. Not finished
- Official Final Decision Brain profitability result is NOT YET VALID.
- The 2024 and 2025 event-level OOS streams still need to be generated from the verified master source through the governed existing rule outputs and joined to the Final OOS contract.
- Only after those fold inputs exist can the final runner emit official 2024, 2025, and combined Win Rate / PF / Expectancy / Net R / Max DD / Costs.

## 17. Next controlled action
Use the verified Dropbox/working-copy M1 master to generate the two governed OOS fold event streams using existing evaluator/runtime outputs. Do NOT create new rule semantics, thresholds, TIZ psychology, Similarity direction, or Risk policy. Then run the Final OOS walk-forward + leakage gate and publish the resulting report only if the hard gates pass.

## 18. Audit note
This worklog deliberately records completed work, resolved failures, diagnostics, and current blockers. Diagnostic numbers are not converted into official performance claims.
