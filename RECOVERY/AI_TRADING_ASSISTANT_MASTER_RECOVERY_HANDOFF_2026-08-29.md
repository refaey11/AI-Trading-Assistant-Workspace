# AI TRADING ASSISTANT — MASTER RECOVERY / HANDOFF
Date: 2026-08-29
Status: ACTIVE — CONTINUATION SAFE POINT
Repository: refaey11/AI-Trading-Assistant-Workspace
Branch at last verified read: backtest-only-2026-08-28
Last verified branch commit at handoff preparation: 4abc208106dd975c965ea0ffda91bae5dcca3166

## 0. PURPOSE
This document is the single continuity handoff for a new ChatGPT chat. It records the project identity, architecture, evidence, completed work, unresolved items, exact next steps, guardrails, and the state that must not be forgotten or rebuilt.

## 1. PROJECT IDENTITY — NON-NEGOTIABLE
This is a long-term AI Trading Assistant / Decision Brain, NOT a simple trading indicator.

Core roles:
- John Murphy = technical context / market structure / primary directional evidence.
- Steve Nison = confirmation / contradiction only; must not independently generate final direction.
- Trading in the Zone = process / psychology evidence only; never generates direction; missing/unresolved TIZ must not become PASS.
- Similarity Engine = historical memory / evidence only; never sole decision maker and never a direction generator.
- Historical Context Memory + Historical Outcome Memory = historical evidence only.
- Dynamic MTF = upstream multi-timeframe context; not the final decision maker.
- Risk = hard gate.
- n8n = orchestration / monitoring / automation, not the brain.
- MT5 = execution / broker boundary.
- 2025 = OOS / locked; NEVER use for tuning or development selection.
- Official development backtest scope = 2016–2024.
- Reuse existing project knowledge; do NOT rebuild existing modules from scratch.
- Before any new integration, perform compatibility/integration audit.

## 2. MASTER ARCHITECTURE
MARKET DATA
 -> MARKET SNAPSHOT
 -> MARKET STATE + MTF
 -> EVIDENCE ADAPTERS
    -> Murphy
    -> Nison
    -> TIZ
    -> Similarity
    -> Historical Context
    -> Historical Outcome
 -> RULE/EVIDENCE NORMALIZATION
 -> CANONICAL EVIDENCE HANDOFF
 -> DECISION BRAIN V1
 -> TIZ STATUS
 -> RISK GATE
 -> TRADE PLAN
 -> EXECUTION CONTRACT
 -> MT5 DEMO
 -> FILL/POSITION
 -> RESULT / P&L
 -> MEMORY + n8n

## 3. MTF — IMPORTANT CORRECTION
Do NOT confuse the full MTF Reader with the six-TF Brain feature/alignment layer.

Full MTF Reader V2 timeframes:
- M5 — execution confirmation
- M15 — short-term structure and confirmation
- M30 — local structure and pullback
- H1 — primary intraday structure
- H4 — higher-timeframe context
- D1 — major context
- W1 — macro context

Official reading order:
Weekly/Daily context -> 4H trend and major structure -> 1H current structure -> 30M pullback/continuation -> 15M setup development -> 5M confirmation.

The Decision Brain's six-TF feature/alignment layer is:
M5, M15, M30, H1, H4, D1
plus:
- mtf_trend_score
- M5_trend_regime
- M15_trend_regime
- M30_trend_regime
- H1_trend_regime
- H4_trend_regime
- D1_trend_regime
and the Brain spec also expects mtf_bullish_count, mtf_bearish_count, mtf_neutral_count, mtf_context_code, plus six-TF volatility inputs.

Critical policy:
- genuine OHLCV only
- UTC / as-of causality
- NEVER fabricate M5/M15/M30 from H1
- MTF never generates BUY/SELL itself
- missing MTF inputs fail closed; they do NOT become 0.0

Primary MTF evidence artifact:
- Dropbox: /MTF_ALIGNMENT_GBPUSD_V1.zip
- Dropbox full reader spec: /AI_Trading_Assistant_FULL_PROJECT_V1/AI_Trading_Assistant_MTF_ARCHITECTURE_V2/MTF_READER_SPEC_V2.json

## 4. DECISION BRAIN
Canonical Brain source:
- Dropbox: /DECISION_BRAIN_V1_SPEC.json
- Recovered runtime: RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py

Brain hard rules from source:
- no future data
- 2025 locked/OOS
- volume unavailable != zero
- Similarity = evidence only
- no automatic BUY/SELL execution in V1
- conclusions must cite evidence modules

Do NOT rewrite Decision Brain V1 during integration.

## 5. MURPHY / NISON / TIZ / MEMORY
Murphy:
- 34 runtime-verified rules are the governed runtime set.
- Murphy 0008 is blocked / not evaluable and is not part of the 34.
- Current Murphy source-coverage ledger shows archive evidence/freeze coverage for 30/34.
- Four runtime-verified Murphy rules whose dedicated evidence packs were not located in the supplied Murphy archive:
  MURPHY_0018 Falling wedge
  MURPHY_0019 Rising wedge
  MURPHY_0025 Four-week breakout
  MURPHY_0026 Four-week breakdown
- These four exist in broader candidate registry but are marked candidate/UNTESTED there.
- Do not invent evidence; if authoritative producers cannot be located, they remain NOT_EVALUABLE and a claimed full-34 E2E gate must stay fail-closed.

Nison:
- 44 governed rules.
- Earlier governed checks showed canonical PASS for 2016–2024 and prior integration reported 2,428,448 evidence rows and 44 rules.
- Nison remains confirmation/contradiction only.

TIZ:
- process/psychology only
- optional/unresolved outside production when runtime proof is unavailable
- never manufacture PASS

Historical / Similarity:
- PIT/as-of required
- evidence only
- cannot generate direction or tuning parameters

## 6. VERSION/FREEZE PROTECTION
Version Freeze Plan evidence:
- status: inventory_completed
- core_keep includes HISTORICAL_MEMORY_V1, HISTORICAL_OUTCOMES_V1, SIMILARITY_ENGINE_V2/INDEXES_V2, MARKET_STRUCTURE, MTF_ALIGNMENT, FEATURE_ENGINEERING_V2, FEATURE_WEIGHTING_V1, MASTER_EVIDENCE, EVIDENCE_LAYER
- do_not_delete = true
- next gate was uniform official walk-forward + leakage audit
- after gate = Decision Brain V1

This means existing intelligence must be protected. No rebuild-from-scratch.

## 7. CANONICAL E2E INTEGRATION PLAN
Dropbox artifact:
/AI_Trading_Assistant_FULL_PROJECT_V1/CANONICAL_E2E_INTEGRATION_PLAN_2026-08-28.md

Canonical runtime specified there:
H1 -> Market State -> MTF -> Murphy 34 -> Nison 44 -> Historical Context Memory -> Historical Outcome Memory -> Similarity V2 -> Context-Aware Retrieval V2 -> Knowledge/Decision Handoff -> Decision Brain V1 -> TIZ status -> Risk/Execution -> execution/backtest contract.

Architecture decision:
1) Evidence Compilation: canonical timestamp-keyed evidence table using sorted point-in-time joins such as merge_asof, with provenance.
2) Decision/Execution: one event envelope at a time through Handoff -> Decision Brain V1 -> TIZ status -> Risk/Execution.

Pre-flight tests required before any expensive governed run:
- every layer reaches Handoff
- historical/similarity/retrieval never generate direction
- TIZ is not hardcoded PASS
- Risk can genuinely PASS and FAIL according to contract
- 2025 blocked from development path
- Decision Brain V1 executes unchanged
- timestamps are as-of bounded / no future leakage

Known canonical E2E defects listed in the plan:
- shadow/partial consumption for Similarity and Context-Aware Retrieval
- old runner passed similarity=None into Brain V1, so historical memory was not really delivered as evidence
- old runner fabricated SL/TP with 0.75 ATR stop and 3R target; this must be replaced by existing upstream risk/execution contract
- Historical Outcome requires real as-of outcome evidence
- Handoff must be the actual boundary carrying complete evidence envelope into Brain

## 8. CURRENT RUNTIME / WIRING WORK DONE IN THIS CHAT
A strict MTF -> Brain join adapter was added conceptually as a source-backed wiring layer, with the design requirements:
- source-backed 7 Brain MTF fields
- backward/as-of merge
- reject missing values
- reject future values
- reject duplicates
- never silently default missing values to 0.0

Do not treat this adapter as a replacement for the canonical MTF source or the Decision Brain.

Important: earlier exploration initially treated the six-TF layer as the full MTF architecture. That was corrected here. W1 remains part of the full Reader architecture.

## 9. RISK / EXECUTION CONTRACT STATUS
There was a compatibility conflict discovered between an older/newer wrapper assumption of 3R minimum and the existing 2R execution contract.

Do NOT change 2R or 3R by guesswork.
The official next action is to resolve the exact frozen Risk/Execution contract from governance artifacts before declaring a full E2E PASS.

The old RISK_ENGINE_SPEC_V1 was a research prototype and is not the canonical final execution contract.

The canonical E2E plan explicitly says the runner must not fabricate its own SL/TP construction; it must use the project's existing upstream execution/risk contract.

## 10. CI / BRANCH / EXECUTION HYGIENE
Repository:
refaey11/AI-Trading-Assistant-Workspace

Verified branch:
backtest-only-2026-08-28

Last verified branch commit while preparing this handoff:
4abc208106dd975c965ea0ffda91bae5dcca3166
Message: Restore safe governed trigger defaults

CI facts recorded in the project handoff:
- cheap CircleCI build_and_test was previously verified SUCCESS after fixing a Python syntax error in BACKTEST/GOVERNED_RUNNER_STATIC_LINT_V1.py
- governed execution remains separate and parameter-gated
- multiple old GitHub workflows were intentionally moved to manual-only to avoid duplicate runs
- manual Governed Integration Gate is the intended official heavy execution path
- a prior CircleCI API trigger reached project resolution but did not create the governed workflow; do not claim trigger path proven until a real governed workflow is observed

Important distinction:
- pipeline creation != workflow execution
- cheap build_and_test PASS != governed integration PASS
- integration PASS != profitable trading system
- code readiness != validated trading performance

## 11. CURRENT PROJECT VERDICT
PROJECT IS NOT BROKEN.

Core architecture and most components are present.
Current remaining work is execution plumbing / governed integration proof and then actual validated performance.

## 12. HISTORICAL PERFORMANCE EVIDENCE — DO NOT MISUSE
An older CURRENT_PROJECT_STATUS_REPORT.json recorded exploratory True Backtest metrics. Examples from that artifact:
- V2, 4h: 1,892 trades, PF 1.2813, expectancy 0.0889R, total 169.67R, max DD -12.61R
- V3, 4h: 1,821 trades, PF 1.2819, expectancy 0.0895R, total 164.38R, max DD -13.05R

The same artifact also contains parameter configurations, including 0.75 ATR and 2R combinations.

These are HISTORICAL/EXPLORATORY metrics from an older project state. They are NOT a fresh governed Decision Brain result and MUST NOT be presented as proof of current profitability.

## 13. WHAT IS DEFINITIVELY DONE / PROVEN OR STRONGLY ESTABLISHED
1. Existing architecture is preserved.
2. 2025 is locked/OOS.
3. Murphy governed runtime set = 34, with 0008 blocked/not evaluable.
4. Nison governed runtime set = 44.
5. Full MTF Reader contract = 7 real-data TFs including W1.
6. Six-TF Brain alignment layer = M5/M15/M30/H1/H4/D1 plus MTF fields.
7. MTF source archive exists: MTF_ALIGNMENT_GBPUSD_V1.zip.
8. Decision Brain V1 specification exists and is recovered.
9. Historical/Similarity layers are evidence-only and PIT constrained.
10. TIZ process-only boundary exists.
11. Canonical E2E integration plan exists.
12. Cheap CI path was previously verified healthy.
13. Risk is an explicit hard gate.
14. The project is not broken; it is in integration / governed-proof stage.

## 14. WHAT IS NOT DONE / MUST NOT BE CLAIMED DONE
1. No fresh governed Gate 3C / Governed Integration Gate PASS has been established by this checkpoint.
2. No fresh complete canonical event has been proven through all required evidence -> Handoff -> Brain -> TIZ status -> Risk/Execution.
3. The actual MTF alignment archive has not been unpacked here through the connector, so do not claim raw file-level contents beyond what the source/provenance artifacts already establish.
4. Full 34-rule Murphy source-backed E2E is not proven until 0018/0019/0025/0026 are either located in authoritative producers or remain explicitly NOT_EVALUABLE.
5. Risk/Execution frozen contract resolution still needs to be confirmed from the governing artifact; do not invent 2R/3R semantics.
6. Unified governed 2016–2024 backtest has NOT earned a new official PASS yet.
7. 2025 must remain untouched for tuning/calibration.
8. Demo/Live deployment is NOT ready merely because modules exist.

## 15. EXACT NEXT STEPS — DO NOT DEVIATE
STEP 1 — Freeze this handoff/checkpoint.
STEP 2 — Verify the current branch and the latest corrected code state.
STEP 3 — Run the official Governed Integration Gate exactly once on the corrected current commit.
STEP 4 — If the gate fails, inspect ONLY the first genuine failing contract/step and fix only that blocker. Do NOT start the full backtest.
STEP 5 — If the gate passes, run the governed 2016–2024 backtest once.
STEP 6 — Analyze real signal quality:
- trade count
- BUY/SELL/NO_TRADE funnel
- expectancy
- PF
- total R
- max DD
- losing streak
- slippage/cost sensitivity
- ambiguity sensitivity
- provenance / leakage checks
STEP 7 — Keep 2025 locked and use it only as final OOS evaluation after development decisions are frozen.
STEP 8 — Freeze Decision/Risk/Execution contracts only after validated development results.
STEP 9 — Paper runtime using SAME decision semantics.
STEP 10 — MT5 Demo execution.
STEP 11 — Broker reconciliation.
STEP 12 — n8n operations/alerts/journal.
STEP 13 — Controlled live only after all gates pass.

## 16. MASTER ROADMAP PHASES
Phase 0 — FREEZE / PROTECT: DONE / baseline protected.
Phase 1 — CANONICAL CONNECT: IN PROGRESS.
Phase 2 — REAL DECISION REPLAY: NEXT after integration proof.
Phase 3 — TRADE PLAN + RISK: integration/validation dependency.
Phase 4 — UNIFIED BACKTEST: 2016–2024 development; 2025 OOS.
Phase 5 — PAPER RUNTIME.
Phase 6 — MT5 DEMO.
Phase 7 — RECONCILIATION.
Phase 8 — n8n operations.
Phase 9 — CONTROLLED LIVE.

Definition of DONE:
1) current snapshot enters runtime
2) all required evidence modules run on same snapshot/as-of
3) Brain makes final decision
4) Risk approves/rejects
5) trade plan exists for approved trade
6) execution can hand to MT5
7) MT5 outcome is captured/reconciled
8) event is journaled
9) n8n monitors lifecycle

## 17. RECOVERY INSTRUCTIONS FOR NEW CHAT
Start by reading this file FIRST.
Then read, in this order:
1. /AI_Trading_Assistant_PROJECT_HANDOFF_2026-08-29.md
2. /AI_TRADING_ASSISTANT_MASTER_EXECUTION_ROADMAP_V1_2026-08-29.md
3. /AI_Trading_Assistant_FULL_PROJECT_V1/CANONICAL_E2E_INTEGRATION_PLAN_2026-08-28.md
4. /AI_Trading_Assistant_FULL_PROJECT_V1/AI_Trading_Assistant_MTF_ARCHITECTURE_V2/MTF_READER_SPEC_V2.json
5. /DECISION_BRAIN_V1_SPEC.json
6. /AI_Trading_Assistant_MURPHY_34_SOURCE_COVERAGE_LEDGER_2026-08-29.md
7. /VERSION_FREEZE_PLAN_V1.json
8. latest continuation / wiring checkpoint

Then inspect the current GitHub branch and latest CI result.
Do NOT:
- rebuild Murphy
- rebuild Nison
- create a new Decision Brain
- fabricate MTF numeric encodings
- turn missing inputs into zero
- tune 2025
- start a broad backtest before governed integration PASS
- claim PASS from schema alone

## 18. ONE-LINE CURRENT STATE
The project is intact; the full MTF architecture is seven TFs, the Brain feature layer is six TFs, the core evidence modules are preserved, and the immediate job is one governed end-to-end integration proof on the corrected runtime; only after that should the governed 2016–2024 backtest run.

## 19. SOURCE EVIDENCE INDEX
Primary source artifacts used for this handoff:
- Dropbox: AI_Trading_Assistant_PROJECT_HANDOFF_2026-08-29.md
- Dropbox: AI_TRADING_ASSISTANT_MASTER_EXECUTION_ROADMAP_V1_2026-08-29.md
- Dropbox: AI_Trading_Assistant_FULL_PROJECT_V1/CANONICAL_E2E_INTEGRATION_PLAN_2026-08-28.md
- Dropbox: AI_Trading_Assistant_FULL_PROJECT_V1/AI_Trading_Assistant_MTF_ARCHITECTURE_V2/MTF_READER_SPEC_V2.json
- Dropbox: DECISION_BRAIN_V1_SPEC.json
- Dropbox: AI_Trading_Assistant_MURPHY_34_SOURCE_COVERAGE_LEDGER_2026-08-29.md
- Dropbox: VERSION_FREEZE_PLAN_V1.json
- Dropbox: AI_Trading_Assistant_CONTINUATION_CHECKPOINT_2026-08-29_SIX_TF_BRAIN_WIRING.md
- Dropbox: MTF_ALIGNMENT_GBPUSD_V1.zip

This document is a recovery/handoff record. It does not replace any source implementation or frozen contract.
