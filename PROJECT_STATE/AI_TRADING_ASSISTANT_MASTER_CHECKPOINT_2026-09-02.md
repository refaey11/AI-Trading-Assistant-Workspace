# AI Trading Assistant — Master Checkpoint

**Date:** 2026-09-02
**Purpose:** Freeze and document the exact state before any new implementation work. This checkpoint is audit/handoff only; it does not change trading semantics.

## 1. Project identity
- Project: **AI Trading Assistant — Decision Brain**
- Goal: build a governed decision system, not a standalone indicator.
- Canonical stack:
  1. Current Market State
  2. Canonical six-TF MTF context: M5, M15, M30, H1, H4, D1
  3. John Murphy 34 rules
  4. Steve Nison 44 rules
  5. Historical Context Memory
  6. Historical Outcome Memory
  7. Similarity / Similarity V2
  8. Context-Aware Retrieval V2
  9. Trading in the Zone process/psychology gate
  10. Risk Engine
  11. Decision Brain / Decision Boundary

## 2. Non-negotiable governance
- Murphy = primary technical context/direction.
- Nison = confirmation/contradiction only; never primary direction.
- Trading in the Zone = process/psychology gate only.
- Similarity/memory = historical evidence only; never sole decision maker or direction generator.
- Risk = hard gate / canonical risk authority.
- MTF = context only; never generates BUY/SELL.
- Missing volume remains missing, not zero.
- No guessed numeric encodings, zero fill, imputation, scaling, or fabricated MTF values.
- Evidence must be causal and as-of bounded.
- 2025 is OOS and must never be used for tuning, calibration, implementation selection, threshold selection, or fitting.
- No canonical 2016–2024 profitability claim until the required governance/provenance gates pass.

## 3. Recovered Decision Brain V1
- Recovered Brain V1 lives at `RUNTIME/DECISION_RUNTIME_V1/decision_brain.py`.
- Do not edit recovered Brain V1 directly; use the governed compatibility adapter/wrapper.
- Direct Brain inputs are intentionally narrow: `mtf_trend_score`, six TF trend regimes, volume availability/regimes, and explicitly passed similarity where governance permits.
- Current governance does not use similarity as a direct directional authority.

## 4. Rule Adapter contract
- Current contract: `rule_adapter_contract_v1.json`.
- Status: DESIGN_ONLY.
- It normalizes existing rule outputs into evidence/gate/conflict/decision_hint/confidence_delta.
- It must not duplicate or rewrite the 102 registry rules.
- Precedence:
  - process failure blocks;
  - risk failure blocks;
  - Murphy invalidation blocks directional setup;
  - Nison confirms or contradicts;
  - similarity supports or weakens;
  - Decision Brain synthesizes.

## 5. Canonical governed rule boundary
- Frozen Decision Brain allowlist: **78 rules total = 34 Murphy + 44 Nison**.
- Murphy 0008 is blocked / not evaluable and is not part of the governed 34-rule runtime set.
- Governed Murphy IDs:
  `0003, 0004, 0006, 0007, 0018, 0019, 0021, 0022, 0023, 0025, 0026, 0028, 0029, 0030, 0031, 0032, 0033, 0034, 0035, 0036, 0037, 0038, 0039, 0040, 0041, 0042, 0043, 0044, 0045, 0047, 0048, 0049, 0050, 0051`.
- Nison IDs: `NISON_0001` through `NISON_0044`.

## 6. Murphy recovery status — important correction
The earlier interpretation that four Murphy rules were missing was corrected.

Authoritative repository history and the current runtime show:
- MURPHY_0018 / 0019: exact evaluators, runtime binding, tests, canonical runtime path; promoted to Runtime Implemented by commit `05da42997104bcc9970a501150895ade5b45a85e` after full-path integration PASS (6/6).
- MURPHY_0025 / 0026: runtime evaluators, tests, entry-point wiring; promoted to verified runtime by commit `a8cc1ae3f2bd0c51204f08904fe2938976916dbe`.
- Current canonical entry point `MURPHY_EVALUATORS_V1/murphy_runtime_entrypoint_v1.py` dispatches the governed Murphy rules and contains bindings for 0018/0019 and 0025/0026 plus the other governed groups.

Therefore:
- **Do NOT rebuild Murphy.**
- **Do NOT request another Murphy archive just because standalone evidence files are absent.**
- **Do NOT fabricate synthetic evidence.**
- The correct task is to make the historical producer/fan-in expose the already existing 34 governed runtime rules.

## 7. Current historical evidence problem
- The current 2016–2024 replay source used by the diagnostic backtest exposes only **7 distinct Murphy rule IDs in its historical source rows**.
- This does **not** mean only 7 Murphy evaluators exist.
- It means the historical evidence extraction/fan-in currently feeding the replay does not surface the full governed 34-rule envelope.
- Therefore `murphy_source_backed_rules_observed = 7` in the previous replay must not be interpreted as “only 7 Murphy rules exist”.

Target pipeline:
`Murphy 34 Registry → 34 Runtime Evaluators → Historical Event Evaluation 2016–2024 → lossless source_rule_id fan-in → PASS/FAIL/NOT_EVALUABLE → Decision Brain`

## 8. Canonical MTF source
- Canonical six-TF source: Dropbox `/MTF_ALIGNMENT_GBPUSD_V1.zip`.
- Annual files: `GBPUSD_M5_MTF_ALIGNMENT_2016.csv` … `2024.csv`.
- Required fields: `mtf_trend_score`, `M5/M15/M30/H1/H4/D1_trend_regime`.
- Source gate previously passed with producer values used verbatim, no categorical translation, imputation, or scaling, and direction generation false.
- MTF is context only.

## 9. Strict as-of correction
A critical look-ahead issue was found and corrected in the diagnostic V5.4 wrapper.

Previous behavior used:
`searchsorted(ts, side="right") - 1`
which could consume a current H1 row at the bar-start timestamp before that H1 bar had closed.

Current correction on diagnostic branch commit:
`64d17c3236a1311968a4d248b01fe36a17ec862d`
message: `fix: enforce strict asof execution inputs in V5.4 replay`

Changes:
- `asof_row` uses `searchsorted(ts, side="left") - 1` so producer inputs are strictly prior to the decision timestamp.
- Exit simulation starts at `entry_idx`, because the first H1 candle beginning at the decision timestamp is the first post-decision execution candle.
- V5.4 wrapper still freezes 0.75 ATR stop distance and 2R target and preserves current Nison semantics.

## 10. Risk contract
Canonical Risk Engine:
`RUNTIME/RISK_ENGINE_INTEGRATION_V1/risk_engine_integration_v1.py`

Frozen V5.4 constants:
- BASE risk: 0.005
- AFTER_TWO_LOSSES: 0.0025
- MAX: 0.015
- SL: 0.75 ATR
- TP: 2.0R
- canonical minimum RR: 2.0

No risk tuning is authorized at this stage.

## 11. Last completed diagnostic full replay BEFORE strict-asof correction
Workflow: `Diagnostic Full Backtest V5.4 2016-2024 V2`
- Run: `33584080603`
- Job: `100104420076`
- Branch: `diagnostic/mtf-gate-observable-2026-09-02`
- Artifact: `9829526630` (`diagnostic-full-backtest-v5-4-2016-2024-v2`)
- Artifact digest: `sha256:0b664...`
- Full Replay: PASS
- Provenance Audit: PASS
- Upload: PASS

Metrics from that run (diagnostic only; not an official profitability result):
- candidate_events: 30678
- evaluated_events: 29163
- realized executed trades: 19644
- open positions at window end: 3
- max concurrent positions: 24
- costs applied: false
- tuning applied: false
- official profitability claim: false
- Murphy registry rules: 34
- Murphy source-backed rule IDs observed: 7
- wins: 6601
- losses: 13043
- win rate: 0.3360313581755243
- profit factor: 1.012190446983056
- expectancy_R: 0.008094074526573
- total_R: 159.0
- max drawdown_R: -400.0

Yearly realized R:
- 2016: +143
- 2017: +34
- 2018: +147
- 2019: -5
- 2020: -7
- 2021: -171
- 2022: +163
- 2023: +97
- 2024: -242

Additional provenance facts:
- trade rows: 27064
- ambiguous trade rows: 7420
- realized trades: 19644
- realized PnL recorded only on exit
- risk state updates only on realized PnL
- unclosed positions excluded from realized profitability
- future data used: false
- event-driven lifecycle: true
- Nison fail is not a contradiction
- Nison contradiction requires opposite-directional pass

## 12. Earlier baseline audit / version-freeze context
The pre-existing Version Freeze Plan and Official Baseline Audit are retained as historical context.
- Prior candidate: Similarity Engine V2 + 4H.
- That candidate was explicitly not official until a uniform walk-forward/leakage audit.
- Stored earlier baseline results use different protocols and therefore are not the current official baseline.
- Current project work has moved into the governed Decision Brain integration path; no old profitability result overrides the current governance state.

## 13. GitHub state before this checkpoint
Repository: `refaey11/AI-Trading-Assistant-Workspace`

Relevant branches:
- `main`: `eae7d7f590bff410b280d21d7ad4dad379d34b12`
- `current-stack-dev-backtest-2016-2024-v3`: development backtest branch
- `diagnostic/mtf-gate-observable-2026-09-02`: diagnostic development branch

Latest diagnostic branch commit before this checkpoint:
`64d17c3236a1311968a4d248b01fe36a17ec862d`

Open/draft PRs relevant to this state include diagnostic/integration work such as PR #86, #82, #83, and #74. Diagnostic work must not be merged to main merely because it passes CI.

## 14. Dropbox state relevant to this checkpoint
Authoritative/relevant records currently located in Dropbox include:
- `/AI_TRADING_ASSISTANT_MURPHY_34_SOURCE_COVERAGE_LEDGER_2026-08-29.md`
- `/MURPHY_RUNTIME_COVERAGE_CORRECTION_2026-08-29.md`
- `/MURPHY_REFRESH_V1.zip`
- `/GBPUSD_RULE_EVALUATOR_V2_WORKSPACE_PART_01_OF_03.zip.part`
- `/GBPUSD_RULE_EVALUATOR_V2_WORKSPACE_PART_02_OF_03.zip.part`
- `/GBPUSD_RULE_EVALUATOR_V2_WORKSPACE_PART_03_OF_03.zip.part`

The coverage correction is authoritative for the interpretation of 0018/0019/0025/0026: they exist as runtime implementations.

## 15. Workspace files present at checkpoint
Key uploaded work packages currently available locally include:
- `VERSION_FREEZE_PLAN_V1.json`
- `OFFICIAL_BASELINE_AUDIT_V1.txt`
- `TRUE_BACKTEST_V2.zip`
- `AI_Trading_Assistant_SIMILARITY_MEMORY_V2.zip`
- `AI_Trading_Assistant_HISTORICAL_OUTCOME_MEMORY_V1.zip`
- `AI_Trading_Assistant_HISTORICAL_CONTEXT_MEMORY_V1.zip`
- `AI_Trading_Assistant_MULTI_TIMEFRAME_READER_V1.zip`
- `AI_Trading_Assistant_MARKET_SCENARIO_ENGINE_V1.zip`
- `AI_Trading_Assistant_MARKET_STATE_READER_V1.zip`
- `AI_Trading_Assistant_MARKET_READER_V1.zip`
- `AI_Trading_Assistant_CONTEXT_AWARE_RETRIEVAL_V2.zip`
- `AI_Trading_Assistant_NISON_CONTEXT_ENGINE_V1.zip`
- `AI_Trading_Assistant_NISON_CANDLE_CONFIRMATION_V1.zip`
- `AI_Trading_Assistant_TRADING_RULES_V2.zip`
- `AI_Trading_Assistant_3_BOOK_INTEGRATION_V1.zip`
- `AI_Trading_Assistant_MASTER_KB_V1.zip`
- `rule_adapter_contract_v1.json`
- current diagnostic provenance/result artifacts
- the split GBPUSD Rule Evaluator V2 workspace parts

## 16. What is DONE
1. Core architecture and governance boundary defined.
2. Decision Brain V1 recovered and protected from direct modification.
3. 78-rule governed boundary frozen.
4. Murphy 34 runtime implementations recovered/verified, including 0018/0019 and 0025/0026.
5. Nison 44 governance boundary in place.
6. Canonical six-TF MTF source validated.
7. Risk contract and V5.4 frozen risk behavior established.
8. Full diagnostic backtest and provenance audit completed successfully under the previous as-of behavior.
9. Strict-as-of/look-ahead correction implemented in diagnostic V5.4 wrapper.
10. Dropbox/GitHub cross-check confirmed the Murphy problem is historical evidence/fan-in coverage, not missing Murphy runtime evaluators.

## 17. NOT DONE / current blockers
1. Re-run the full governed replay after the strict-as-of correction.
2. Replace the current 7-ID historical Murphy feed with a full governed 34-rule producer/fan-in path.
3. Validate that all 34 rules can produce authoritative PASS/FAIL/NOT_EVALUABLE envelopes on real 2016–2024 events without fabricated values.
4. Re-run provenance and backtest gates after full-34 fan-in.
5. Only later, after governance passes, evaluate profitability. No official profitability claim now.
6. Intrabar ambiguity resolution is not yet considered solved merely because M1 source exists; it must be implemented and validated before claiming perfect lifecycle resolution.

## 18. Immediate next work — after this checkpoint only
**First:** inspect and wire the existing 34 Murphy runtime producers into the historical evaluation/fan-in path.
**Second:** validate the resulting evidence envelope on a bounded pre-2025 sample.
**Third:** re-run the strict-as-of V5.4 full 2016–2024 diagnostic replay and provenance audit.

No new strategy tuning, risk tuning, threshold tuning, rule rewriting, or OOS use is authorized during this step.

## 19. Checkpoint rule
This file is the authoritative handoff snapshot for the current project state. Before any later task changes implementation semantics, update the checkpoint/history first so the sequence and evidence trail remain reconstructible.
