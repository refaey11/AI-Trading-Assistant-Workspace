# Full Project Recovery & Backtest Roadmap — 2026-11-15

Status: READ-ONLY EXECUTION AUDIT / ROADMAP
Target development window: 2016-2024
Protected OOS window: 2025 (strictly excluded from tuning, calibration, threshold selection, feature selection, and implementation selection)
Repository: refaey11/AI-Trading-Assistant-Workspace
Audited development branch: current-stack-dev-backtest-2016-2024-v3
Audited branch HEAD: 34f2f8ca89d0cb1b437d0bdf8bd9fbfd7e5a2f6e

## Executive decision

Do not restart the project and do not rebuild existing knowledge or data products. The repository already contains substantial Decision Brain, Murphy/Nison, memory, runtime, risk, tests, and backtest assets. The immediate problem is not that the entire system is missing: the current advertised V5.4 GitHub Actions green check is a contract-test pass, not a historical replay/backtest. Several important upstream data producers and execution contracts still require proof before any profitability claim is valid.

Recommended route: establish a reproducible, read-only 2016-2024 input/preflight and integration path first; resolve MTF producer provenance and risk-contract identity; then run the real replay with complete event/trade/funnel/validation artifacts. Similarity V3 remains isolated and must not block unrelated recovery work.

## 1. Repository and branch state

- Repository exists and is writable by the connected GitHub account.
- Default branch: main.
- Development target branch: current-stack-dev-backtest-2016-2024-v3.
- Target branch HEAD at audit: 34f2f8ca89d0cb1b437d0bdf8bd9fbfd7e5a2f6e.
- PR #116 is OPEN, DRAFT, NOT MERGED. It targets current-stack-dev-backtest-2016-2024-v3. It is a read-only MTF / Market Structure / Similarity producer-lineage investigation. No merge is authorized by this audit.
- This report is documentation only. No runtime, risk, source archives, market data, or OOS files were changed.

## 2. Confirmed assets and what they prove

### 2.1 Candle data

PR #116 reports a GBPUSD M1-to-six-timeframe reconciliation against the existing MULTI_TF_MARKET_DATA_V1 output for 2016-2024:
- M5: 671,601 / 671,601
- M15: 223,978 / 223,978
- M30: 111,995 / 111,995
- H1: 55,998 / 55,998
- H4: 14,209 / 14,209
- D1: 2,544 / 2,544

All tested OHLC, M1 row counts, volume availability flags, and available-volume sums matched; no missing or extra output bars were reported. 2025+ was excluded. Do not rebuild this conversion. This proves the tested GBPUSD candle aggregation output reconciliation, not Market Structure/MTF feature formulas.

### 2.2 Existing data and engine assets

The audited branch contains:
- BACKTEST/DEV_BACKTEST_RUNNER_V1.py and a development runner plan.
- DEVELOPMENT_2016_2024 historical replay implementations V2, V3, V4, V5.3, and V5.4.
- Current-stack component-completeness and runtime-wiring gates.
- Recovered Decision Brain V1 source and handoff adapters.
- Murphy and Nison evaluator/runtime modules and tests.
- Historical memory provider and memory governance tests.
- TIZ process gate.
- RUNTIME/RISK_ENGINE_INTEGRATION_V1 and a separate risk_execution_runtime_v1 path.
- 2025 OOS lock/freeze manifests and evaluation policy.

Presence of a file or adapter does not prove that the historical replay consumes it correctly. Each input must pass schema, timestamp, point-in-time, lineage, and semantic compatibility checks.

### 2.3 MTF and Market Structure lineage

PR #116's source-lineage findings are binding until superseded by stronger evidence:
- Existing Market Structure and six-timeframe MTF output archives exist for EURUSD, GBPUSD, USDJPY, USDCAD, and XAUUSD.
- Existing adapters validate, normalize, or join precomputed outputs; they do not generate the underlying structure/regime/score fields.
- Exact producer formulas for trend_regime, pivots/structure features, six-timeframe alignment, and mtf_trend_score were not recovered.
- MTF Architecture V2 is a specification/planning folder, not proof of the original six-timeframe producer.
- Do not invent categorical encodings, averages, missing-value defaults, or a substitute score.
- Keep affected semantic Brain fields NOT_EVALUABLE / blocked until exact provenance is proven.

### 2.4 Similarity lineage

Keep the product generations separate:
- Similarity V2: 57D schema; raw/current-query producer and preprocessing lineage remain unproven.
- Similarity V3: 71D schema; Run 039 refers to v3_shared_builder.py, but its source was not recovered from the reviewed Dropbox archives/backups and selected GitHub trees.
- FEATURE_ENGINEERING_V2: separate completed 22-feature descriptive/memory schema; it is not proven to be part of the V3 71D builder or the V2 57D producer.
- Do not infer 71 = 49 + 22.
- Similarity and historical memory are evidence only and must never generate direction or tuning parameters.
- Keep Similarity V3 isolated. Existing daily recovery automation is already tracking the missing builder; do not create a duplicate automation.

## 3. Critical finding: V5.4 green check is not a backtest

Workflow:
.github/workflows/current-stack-development-backtest-2016-2024-v5-4.yml

The workflow's executed steps are:
1. Checkout.
2. Set up Python.
3. Install pandas.
4. Check that the V5.4 replay and contract-test files exist.
5. Run DEVELOPMENT_2016_2024/test_v5_4_contract.py.
6. Print "V5.4 contract PASS".

It does NOT:
- acquire H1, Market State, Murphy, Nison, MTF, or memory datasets;
- run the V5.4 replay CLI with input arguments;
- call the replay's run() function on historical data;
- emit event, executed-trade, funnel, metrics, or validation-manifest artifacts;
- apply or validate the frozen transaction-cost/slippage contract.

Latest reviewed run:
https://github.com/refaey11/AI-Trading-Assistant-Workspace/actions/runs/43665616843

Its logs explicitly show only the contract test and the PASS message. This is a test success, not a backtest success.

Earlier run:
https://github.com/refaey11/AI-Trading-Assistant-Workspace/actions/runs/43665185311

It failed because pandas was not installed before importing V4. The later run installed pandas and passed the contract test, but still did not run the replay.

Therefore: do not report V5.4 as a completed or profitable backtest.

## 4. V5.4 / V4 compatibility and risk boundary

V5.4 wraps/transforms V4 source and defines a frozen candidate profile:
- Stop = 0.75 ATR
- Target = 2.0R
- Nison absence is treated as optional confirmation evidence in this candidate mode.

The canonical project decision contract remains minimum 3R, with 1e-12 tolerance, as documented in AUDITS/RISK_EXECUTION_CONTRACT_RECONCILIATION_2026-08-29.md and implemented in RUNTIME/RISK_ENGINE_INTEGRATION_V1/risk_engine_integration_v1.py.

V4 and V5.4 also reference a separate risk implementation path under risk_engine/risk_execution_runtime_v1.py / frozen candidate risk profile. Do not assume this is interchangeable with RUNTIME/RISK_ENGINE_INTEGRATION_V1. Trace and reconcile the exact runtime call chain before promotion.

Consequences:
- V5.4 2R candidate replay cannot be labelled canonical 3R Decision Brain performance.
- Do not silently change 2R to 3R or 3R to 2R.
- Keep 2R legacy/candidate research evidence separate from the canonical 3R decision contract.
- Do not modify SL/TP generation, risk thresholds, drawdown breaker, position sizing, or risk authority during this documentation/audit phase.

## 5. Current evidence classification

| Area | Status | Evidence / interpretation |
|---|---|---|
| GBPUSD M1 to six-TF candle conversion | VERIFIED for 2016-2024 | 100% reconciliation reported by PR #116; do not rebuild |
| H1 historical source | PRESENT | Must verify actual downloaded file, coverage, duplicates, gaps, timezone |
| Market State | PRESENT as artifact/contract | Need runtime consumption and point-in-time proof |
| Murphy 34 evidence | PRESENT | Need source coverage, timestamp join, rule allowlist and decision handoff verification |
| Nison 44 evidence | PRESENT | Confirmation/contradiction only; absence handling must follow selected mode |
| Six-TF MTF output archive | PRESENT | Producer lineage/formula remains unproven; block semantic use where provenance is required |
| Market Structure producer | NOT RECOVERED | Do not invent feature formulas |
| Similarity V2 producer | NOT PROVEN | Evidence-only; not sole decision maker |
| Similarity V3 shared builder | NOT RECOVERED | Isolate; daily recovery automation active |
| Decision Brain V1 source | PRESENT | Preserve unchanged; inspect exact invocation and outputs |
| Memory provider/adapters | PRESENT | Prove as-of query and future-data isolation in replay |
| TIZ process gate | PRESENT | Process/psychology only; unresolved must not be converted to PASS |
| Risk runtimes | PRESENT, CONTRACT RECONCILIATION REQUIRED | Separate candidate/canonical paths and 2R/3R conflict |
| V5.4 workflow | GREEN CONTRACT TEST ONLY | Does not execute replay |
| Actual V5.4 full-window backtest | NOT PROVEN / NOT EXECUTED by reviewed workflow | No valid run artifacts from the green check |
| Costs/slippage | NOT APPLIED in inspected V4 diagnostic metrics | Must be frozen and applied before profitability claims |
| 2025 OOS | LOCKED | Never tune, calibrate, select, or debug implementation against 2025 |

## 6. Recommended execution map to a valid development backtest

### Gate A — Reproducible input preflight (first implementation target)

Create a read-only 2016-2024 preflight using existing files and source bundles. It must:
- pin exact source paths, hashes, revisions, and download manifests;
- validate H1/M1/Market State/Murphy/Nison/MTF/memory schemas;
- report coverage by year, duplicates, gaps, timezone assumptions, nulls, and timestamp ordering;
- verify each event consumes only information available at its timestamp;
- enforce the 2016-01-01 through 2024-12-31 inclusive development window;
- fail closed on missing or unproven semantic fields;
- explicitly assert that no 2025+ row enters the development dataset;
- not calculate strategy profitability.

Acceptance: deterministic preflight manifest with PASS/FAIL per source and reproducible hashes.

### Gate B — Runtime and decision integration audit

Trace one actual historical event through:
H1/Market State + MTF -> Murphy directional evidence -> Nison confirmation/contradiction -> evidence-only memory -> TIZ process gate -> Decision Brain V1 -> canonical risk gate -> execution event.

For each stage, record exact input/output, source timestamp, as-of timestamp, rule IDs, status, rejection reason, and provenance. Use existing single-event E2E and integration tests; do not substitute a smoke test for a full historical replay.

Acceptance: single-event end-to-end record is reproducible and matches the existing source contracts; no direction from Nison, Similarity, memory, or TIZ.

### Gate C — Resolve MTF semantic lineage

Recover the original Market Structure / MTF producer source or an exact serialized feature matrix with manifest, parameters, feature order, and preprocessing metadata. Reconcile output rows to the released archive. If source cannot be recovered, do not approximate. Mark fields NOT_EVALUABLE and formally decide whether the current Decision Brain can operate without them under its existing contract.

Acceptance: exact source-to-output reproducibility and point-in-time close alignment. No inferred formulas.

### Gate D — Risk/execution contract reconciliation

Compare the exact replay call chain with:
- AUDITS/RISK_EXECUTION_CONTRACT_RECONCILIATION_2026-08-29.md
- RUNTIME/RISK_ENGINE_INTEGRATION_V1/risk_engine_integration_v1.py
- risk_engine/risk_execution_runtime_v1.py
- frozen candidate risk profile and V5.4 wrapper.

Document which mode is being tested: canonical >=3R or a separately labelled frozen 2R candidate. Verify SL/TP, RR, sizing, loss streak, drawdown, open-position lifecycle, ambiguous bars, spread/commission/slippage, and exit accounting. No risk code changes until the reconciliation is approved.

Acceptance: one unambiguous execution contract selected for the run; tests prove boundary conditions and trade lifecycle.

### Gate E — Full 2016-2024 replay

Only after Gates A-D pass:
- implement/fix a real workflow that downloads the pinned existing source bundles;
- runs the selected replay command (not just a contract test);
- produces the planned event, decision, trade, funnel, metrics, and validation outputs;
- uploads immutable artifacts with run ID, commit SHA, source hashes, and config manifest;
- records costs/slippage and execution assumptions;
- fails if any validation gate fails.

Required artifacts should include:
- unified_78_events_2016_2024.csv
- decision_events_2016_2024.csv
- executed_trades_2016_2024.csv
- execution_funnel_2016_2024.json
- backtest_metrics_2016_2024.json
- validation_manifest_2016_2024.json
- source_manifest_2016_2024.json

Acceptance: reproducible rerun on the same commit/source hashes; all timestamp/lookahead/MTF/memory/risk/execution/cost gates PASS. A zero-trade result before these gates pass is diagnostic, not profitability evidence.

### Gate F — Post-backtest review

Evaluate 2016-2024 development results without changing parameters based on 2025. Report per-year and aggregate trades, win rate, expectancy, profit factor, drawdown, exposure, rejected-event reasons, costs, and robustness. Any later 2025 evaluation must follow the frozen OOS protocol and remain evaluation-only.

## 7. Non-negotiable project role boundaries

- John Murphy: technical context / market structure / directional evidence only through verified runtime rules.
- Steve Nison: confirmation or contradiction; never independent direction.
- Trading in the Zone: psychology/process gate; never direction.
- Similarity and historical memory: historical evidence only; never sole decision maker or direction generator.
- Decision Brain: combines current market evidence, book knowledge, historical memory, and risk.
- Risk: hard gate, non-overridable.
- No Auto BUY/SELL in V1.
- 2025 remains OOS protected.

## 8. Explicit prohibitions during recovery

- No rebuild of existing book knowledge or candle conversion.
- No guessed Market Structure/MTF/Similarity producer.
- No 2025 tuning, calibration, threshold selection, feature selection, or implementation selection.
- No silent 2R/3R substitution.
- No merge of PR #116 without review and explicit approval.
- No claim that a green smoke/contract test is a backtest.
- No real-money execution or live automation based on diagnostic outputs.

## 9. Immediate next engineering action

Implement Gate A only: a deterministic, read-only 2016-2024 source/input preflight workflow on a separate branch. Do not start a full replay until the input manifest, MTF semantic availability, and selected risk contract are proven. Keep this roadmap as the checkpoint to resume from in later sessions.

## References

- PR #116 — MTF archive producer lineage audit (OPEN DRAFT, NOT MERGED): https://github.com/refaey11/AI-Trading-Assistant-Workspace/pull/116
- MTF lineage report: https://github.com/refaey11/AI-Trading-Assistant-Workspace/blob/audit/mtf-archive-producer-lineage/AUDITS/MTF_MARKET_STRUCTURE_SIMILARITY_PRODUCER_LINEAGE_RECOVERY_2026-11-15.md
- V5.4 workflow: https://github.com/refaey11/AI-Trading-Assistant-Workspace/blob/current-stack-dev-backtest-2016-2024-v3/.github/workflows/current-stack-development-backtest-2016-2024-v5-4.yml
- V5.4 replay: https://github.com/refaey11/AI-Trading-Assistant-Workspace/blob/current-stack-dev-backtest-2016-2024-v3/DEVELOPMENT_2016_2024/current_stack_historical_replay_v5_4.py
- V5.4 contract test: https://github.com/refaey11/AI-Trading-Assistant-Workspace/blob/current-stack-dev-backtest-2016-2024-v3/DEVELOPMENT_2016_2024/test_v5_4_contract.py
- Successful V5.4 contract-only run: https://github.com/refaey11/AI-Trading-Assistant-Workspace/actions/runs/43665616843
- Earlier V5.4 failure (missing pandas): https://github.com/refaey11/AI-Trading-Assistant-Workspace/actions/runs/43665185311
- Risk contract reconciliation: https://github.com/refaey11/AI-Trading-Assistant-Workspace/blob/current-stack-dev-backtest-2016-2024-v3/AUDITS/RISK_EXECUTION_CONTRACT_RECONCILIATION_2026-08-29.md
- Pre-OOS freeze manifest: https://github.com/refaey11/AI-Trading-Assistant-Workspace/blob/current-stack-dev-backtest-2016-2024-v3/FREEZE/DECISION_BRAIN_PRE_OOS_FREEZE_MANIFEST_V1.json
