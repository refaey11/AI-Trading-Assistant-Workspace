# AI TRADING ASSISTANT — DECISION BRAIN
# MASTER PROJECT STATE / CONTINUITY FILE
Date: 2026-09-03
Status: CURRENT HANDOFF — DO NOT RESTART OR REBUILD

============================================================
1. PROJECT IDENTITY
============================================================

Project:
AI Trading Assistant — Decision Brain

Mission:
Turn the existing trading project into one integrated Decision Brain that consumes:
Market Data → Market Snapshot → Market State + MTF → governed book evidence → historical/context memory → Decision Brain → Hard Gates → Risk → Trade Plan → Execution → MT5 → Result/P&L → Memory + n8n.

NON-NEGOTIABLE:
- This is NOT a simple indicator.
- Existing project knowledge/components are the source of truth.
- Audit, integrate, verify, and wire existing components. DO NOT rebuild from scratch.
- Backtest, Paper, Demo, and Live must use the same decision-runtime semantics.
- One canonical Decision Event should carry the integrated result.
- Fail-closed: if executable direction is absent, reject the trade. Never invent BUY/SELL.
- 2025 is protected OOS and MUST NOT be used for tuning, calibration, or rule changes.

============================================================
2. CURRENT HIGH-LEVEL ARCHITECTURE
============================================================

Canonical chain:

Market Data
  ↓
Market Snapshot
  ↓
Market State + Multi-Timeframe Reader
  ↓
Evidence Adapters
  ├─ John Murphy = primary technical context / structure / directional context
  ├─ Steve Nison = confirmation / contradiction only
  ├─ Trading in the Zone = process / psychology gate only
  ├─ Similarity Memory = historical evidence only
  ├─ Historical Context Memory = historical/context evidence
  └─ Historical Outcome Memory = outcome evidence
  ↓
Decision Brain
  ↓
Hard Gates
  ↓
Risk
  ↓
Trade Plan
  ↓
Execution Adapter
  ↓
MT5
  ↓
Fill / Position / Result
  ↓
Memory + n8n

Role rules:
- Murphy creates/anchors technical direction; other books do not independently create direction.
- Nison can confirm or contradict; it cannot create direction independently.
- TIZ is a process/psychology gate; unavailable TIZ evidence = NOT_EVALUABLE, never synthetic.
- Similarity/Historical evidence supports or weakens the decision; never sole decision maker.
- Risk is a hard execution gate.

============================================================
3. VERIFIED GATE / IMPLEMENTATION STATUS
============================================================

A) Gate 1 — Canonical Connect
STATUS: PASS

B) Gate 2 — Real Decision Replay
STATUS: PASS for the available 2016 artifacts at the time of the verified replay.

Verified artifact-level replay:
- 401 events
- 120 EXECUTABLE
- 56 CANDIDATE
- 225 NO_TRADE
- 120/120 executable events matched existing filtered execution outcome
- No unmatched executable events
- No duplicate decision IDs after setup-aware identity fix
- Win rate: 56.67%
- Profit Factor: 1.4554
- Expectancy: +0.17286R
- Total: +20.7432R
- Max DD: -11.9262R

IMPORTANT:
These figures are artifact-level verification for the available 2016 artifacts.
They are NOT an official 2016–2024 baseline and must not be presented as full-period final results.

C) Gate 3B — Execution Adapter
STATUS: PASS

D) Gate 3C — Bounded discovery + single-event Full Brain → Risk → Trade Plan E2E
STATUS: PASS / OPERATIONAL

Verified:
- GitHub Actions run: 33352436711
- Discover job: 99368252868
- Conclusion: SUCCESS
- Valid discovered event: 2024-12-31T16:00:00Z
- Full Brain → Risk → Trade Plan E2E succeeded for the bounded discovered event.
- NO_TRADE is an allowed decision, not a pipeline failure.
- Nison NOT_EVALUABLE is not a reason to rewrite/tune Nison.

IMPORTANT DISTINCTION:
Gate 3C single-event E2E is operational.
The full governed 2016–2024 backtest is NOT yet PASS.

============================================================
4. CURRENT BACKTEST POSITION
============================================================

Development scope:
2016–2024

Protected OOS:
2025

Official development runner:
BACKTEST/DEV_BACKTEST_RUNNER_V1.py

Official plan:
BACKTEST/DEV_BACKTEST_RUNNER_PLAN_V1.md

Required outputs:
- unified_78_events_2016_2024.csv
- decision_events_2016_2024.csv
- executed_trades_2016_2024.csv
- execution_funnel_2016_2024.json
- backtest_metrics_2016_2024.json
- validation_manifest_2016_2024.json

Latest known position:
2016–2024 governed backtest is READY TO RERUN after Murphy source-path acquisition fix.

Earlier failure classification:
The previous 2016–2024 run failed at source acquisition (~03:43 on Aug 31), NOT because of Decision Brain/backtest logic.
The failure was:
“No source-backed Murphy 2016-2024 evidence found.”

Source-path fix:
Commit:
073520e2b3162fbed9d803a7ddee4f384adf4b0d

Commit purpose:
fix: use actual Murphy 2016-2024 Dropbox source

The fix:
- downloads the actual authoritative Murphy 2016–2024 ZIP
- extracts it
- validates timestamp + rule_id/source_rule_id
- requires >=34 unique Murphy rules
- requires scope through 2024
- passes the selected governed CSV into the existing runner
- does NOT change Murphy semantic rules

Authoritative Murphy source located in Dropbox:
Path:
 /New 8/MURPHY_HISTORICAL_34_RULE_FANIN_2016_2024.zip

Dropbox file id:
 id:u18dZfxRtWwAAAAAAAADIQ

Modified:
2026-08-28T01:17:55Z

IMMEDIATE NEXT ACTION:
Run the latest “Development Decision Brain Backtest 2016-2024” workflow from main.
If it fails:
1. classify the FIRST failing step,
2. fix only that named gap,
3. do not rebuild,
4. do not retune strategy semantics,
5. do not touch protected 2025 OOS.

============================================================
5. MURPHY CURRENT STATE
============================================================

Current authoritative count:
51 total Murphy rules
34 governed / closed
17 remain open / deferred

DO NOT USE the old 33/51 wording as current state.

Current diagnostic producer map:
BACKTEST/MURPHY_34_PRODUCER_MAP_V1.json

Scope:
governed_murphy_34

Locked year:
2025

Known classes/status examples:
- 0003/0004: runtime murphy_0003_0004_runtime_v2; historical_structure_candidate; blocked until full joint structure semantics verified.
- 0006/0007: runtime murphy_0006_0007_runtime_v1; provisional QA; blocked until production frozen confirmation stream.
- 0018/0019: trendline convergence adapter/evaluator; producer not yet bound.
- 0021/0022/0023: source-backed fan-in; eligible.
- 0025/0026: source-backed feature replay; eligible.
- 0028/0029: source-backed historical; eligible.
- 0030–0032: Point-and-Figure required; not bound.
- 0033: producer-specific required; not bound.
- 0034–0038: recovered runtime; pending historical binding.
- 0039: process context, non-directional.
- 0040/0041: PSAR / ADX producer families discovered, pending binding.
- 0042–0045: account-context / non-market / non-directional.
- 0047: producer family discovered, pending binding.
- 0048/0049: source not verified, non-directional.
- 0050: checklist gate.
- 0051: trade plan gate.

Within current 34:
- 25 directional
- 9 non-directional

Current fan-in bridge:
BACKTEST/MURPHY_34_HISTORICAL_PRODUCER_FANIN_V1.py

Conservative behavior:
- no inferred Murphy semantics
- no invented thresholds
- no invented direction
- no invented missing values
- missing required fields => NOT_EVALUABLE
- source-backed evidence is passed to canonical evaluator
- synthetic evidence = false
- threshold invention = false
- direction generation = false
- strict as-of semantics required

Known producer families:
FOUR_WEEK_LOOKBACK
DMI_ADX
PARABOLIC_SAR
OSCILLATOR_DIVERGENCE
TRENDLINE_GEOMETRY
OBV
VOLUME_CONFIRMATION
OPEN_INTEREST
PIVOT_SEQUENCE
PIVOT_SEQUENCE_V2

============================================================
6. IMPORTANT ARCHIVE / MULTIPART BREAKTHROUGH
============================================================

The four .bcut files under /mnt/data/019–022 were initially confusing but were reconstructed successfully.

Key facts:
- They contain 4-byte header length + JSON metadata + raw payload.
- Part 03 reconstructed payload:
  /mnt/data/reconstructed_part03_payload.bin
- Reconstructed payload size:
199,219,966 bytes
- This matched the Dropbox Part 03 metadata.
- Python zipfile could list 241 central-directory members.
- Some local headers/data are in earlier volume parts, so not every member can be read from Part 03 alone.

Part 03 central directory confirms producer families/files including:
- FOUR_WEEK_LOOKBACK 2016–2024
- DMI_ADX D1/H4/H1 2016–2024
- PARABOLIC_SAR D1/H4/H1 2016–2024
- OSCILLATOR_DIVERGENCE H4/D1/H1 2020–2024
- TRENDLINE_GEOMETRY multiple timeframes
- OBV 2020–2024
- VOLUME_CONFIRMATION_V2 2020–2024
- OPEN_INTEREST 2020–2024
- PIVOT_SEQUENCE V1/V2 multiple timeframes
- Murphy evaluator historical files for 0003/0004, 0021–0023, 0027–0029
- exact mapping/contracts/audits

Successfully directly readable from Part 03:
- PIVOT_SEQUENCE V1 H1 (~15 MB)
- PIVOT_SEQUENCE V2 H1 (~2.1 MB)

Do not expose temporary download URLs.

Multipart metadata:
- Part 01: 199,229,440 bytes; modified 2026-08-19 13:09:23Z
- Part 02: 199,229,440 bytes; modified 2026-08-19 04:52:34Z
- Part 03: 199,219,966 bytes; modified 2026-08-19 13:09:35Z

============================================================
7. THREE-BOOK / KNOWLEDGE GOVERNANCE
============================================================

Murphy:
Primary technical context and directional structure.

Nison:
44/44 frozen historically.
Used only for confirmation/contradiction.
Never independent direction generation.

Trading in the Zone:
0/7 authoritative historically for integration.
Process/psychology only.
If unavailable, use NOT_EVALUABLE rather than synthetic evidence.

Rule Adapter contract:
Uploaded/known file:
rule_adapter_contract_v1.json

Contract purpose:
Normalize existing book-rule outputs into Brain evidence without duplicating source rules.

Source-of-truth hierarchy:
- Master KB
- 3-book integration
- KB audit

Do NOT copy 102 registry rules into Decision Brain.

Adapter output concepts:
- evidence
- gate
- conflict
- decision_hint
- confidence_delta

Precedence:
1. process failure blocks
2. risk failure blocks
3. Murphy invalidation blocks directional setup
4. Nison confirms/contradicts
5. Similarity supports/weakens
6. Brain synthesizes

Known adapter contract status:
DESIGN_ONLY

IMPORTANT:
Do not silently promote DESIGN_ONLY to production semantics without evidence.

============================================================
8. MEMORY / CONTEXT / MTF STATUS
============================================================

Historical Context Memory:
Connected to the evidence path.

Historical Outcome Memory:
Connected to the evidence path.

Similarity Engine:
Connected as historical evidence only.
Cannot be sole decision maker.
Cannot generate direction.

Context-Aware Retrieval:
Part of evidence retrieval path.

Market State:
Connected.

Multi-Timeframe Reader:
Exists and is connected conceptually.
Still must be verified in the full 2016–2024 governed replay for:
- correct timestamp alignment
- correct as-of semantics
- correct consumption by Decision Brain
- no future leakage

============================================================
9. RISK / TRADE PLAN / EXECUTION STATUS
============================================================

Risk:
Connected as hard gate.

Gate 3C proved that:
Full Brain → Risk → Trade Plan
can operate end-to-end for a real bounded event.

Trade Plan:
Connected in Gate 3C.

Execution Adapter:
Gate 3B PASS.

MT5:
NOT YET real execution.
Sequence remains:
Backtest → protected OOS → Paper → MT5 Demo → Reconciliation → Controlled Live.

============================================================
10. OFFICIAL BASELINE — STILL NOT LOCKED
============================================================

Known candidate / historical results:
TRUE_BACKTEST_V2:
- 1,892 trades
- PF 1.2813
- Expectancy +0.08891R
- Total +169.67R
- Max DD -12.61R

FOLD_B_FINAL:
V2 + 4H
- locked threshold 0.52
- 0.75 ATR
- 2R
- 2025 average expectancy +0.18657R
- PF 1.52545
- Total +405.28R

BASELINE_BACKTEST_V1:
V3, 2025, 55/45, 1R/1.5R proxy
NOT a true bar-level execution baseline.

Official baseline gate required:
- calibration 2016–2023 → OOS 2024
- calibration 2016–2024 → OOS 2025
- SAME signal
- SAME k
- SAME SL/TP
- SAME ambiguity handling
- SAME costs
- NO OOS tuning

Only after this protocol is completed can V2+4H be called OFFICIAL BASELINE.

============================================================
11. BRANCH / WORKSPACE DRIFT
============================================================

GitHub repo:
refaey11/AI-Trading-Assistant-Workspace

Default branch:
main

Relevant branches:
- canonical-decision-pipeline-v1
- diagnostic/murphy-34-recovery-2026-09-02

Known divergence:
canonical-decision-pipeline-v1 vs main:
main ahead by 11, behind by 1, total 11 commits.

main vs diagnostic/murphy-34-recovery-2026-09-02:
diagnostic branch ahead by 353, behind by 64.

Interpretation:
The project is NOT “broken”.
There is implementation drift / branch sprawl and many diagnostic layers accumulated.
DO NOT solve this by blindly merging everything.
Use main + verified source-of-truth artifacts and only pull in changes that close a named gap.

No Dropbox workspace reorganization has been completed yet.
No bulk file moves should be done casually.
The proposed conceptual folders remain:
00_MASTER_INDEX
01_GATES
02_DECISION_BRAIN
03_MURPHY
04_NISON
05_TIZ
06_MEMORY_RETRIEVAL
07_BACKTEST
08_DATA_PRODUCERS
09_ARCHIVE

============================================================
12. AUTHORITATIVE PROJECT DOCUMENTS
============================================================

Important GitHub files:
- PROJECT_INDEX/MASTER_PROJECT_STATE_2026-08-19.md
- PROJECT_INDEX/MURPHY_33_MASTER_FREEZE_MANIFEST_V1.json
  NOTE: historical artifact; do not use its 33-count as current.
- PROJECT_INDEX/MURPHY_CANONICAL_RECONCILIATION_REGISTRY_V1.json
- PROJECT_INDEX/DO_NOT_TOUCH.md
- PROJECT_INDEX/MASTER_EXECUTION_ROADMAP_V1_2026-08-29.md
- PROJECT_STATE/2026-08-31_GATE3C_BACKTEST_HANDOFF.md
- PROJECT_STATE/AI_TRADING_ASSISTANT_CHECKPOINT_2026-09-02.md
- DECISION_BRAIN_CURRENT_STATE_CHECKPOINT_2026-08-31.md

Historical handoff:
PROJECT_INDEX/COMPLETE_HANDOFF_PROJECT_STATE_2026-08-21.md
This is historical and must be read in context, not used to overwrite the current state.

Dropbox authoritative/important source family:
- /New 8/MURPHY_HISTORICAL_34_RULE_FANIN_2016_2024.zip
- H1 master
- market state
- Nison full evidence
- Nison manifest
- backtest plans
- Murphy canonical state
- Gate3C risk bridge
- Gate3C progress

============================================================
13. ANTI-LOOP / DO-NOT-DO RULES
============================================================

DO NOT:
- restart the project
- rebuild Decision Brain from scratch
- create a new strategy layer without a named gap
- duplicate book-rule logic inside Brain
- retune 2025
- use 2025 to calibrate
- replace valid existing adapters because a source is temporarily unavailable
- invent missing historical evidence
- invent thresholds
- invent direction
- treat NOT_EVALUABLE as BUY/SELL
- confuse single-event Gate 3C PASS with full 2016–2024 backtest PASS
- label artifact-level 2016 results as official baseline
- keep creating audits/freezes/evaluators that do not close a named gap
- merge diagnostic branch wholesale into main

ANTI-LOOP RULE:
Every change must answer:
“What exact verified gap does this close?”

============================================================
14. WHAT IS CONNECTED TO THE BRAIN — CURRENT TRUTH
============================================================

YES / CONNECTED:
- Market State
- Murphy technical context path
- Nison confirmation/contradiction path
- TIZ process gate path (with NOT_EVALUABLE when unavailable)
- Historical Context Memory
- Historical Outcome Memory
- Similarity evidence path
- Context-Aware Retrieval
- Risk hard gate
- Trade Plan
- Execution Adapter

CONNECTED BUT REQUIRES FULL-REPLAY VERIFICATION:
- Multi-Timeframe correctness across 2016–2024
- Full historical Murphy 34 coverage across all governed events
- producer-by-producer as-of/timestamp correctness

NOT YET:
- successful governed 2016–2024 full backtest
- accepted validation manifest for 2016–2024
- development freeze based on that accepted replay
- protected 2025 OOS validation
- Paper trading
- MT5 Demo
- final live reconciliation / controlled live

============================================================
15. WHAT TO DO NEXT — SINGLE PATH
============================================================

1. Run the latest main-branch Development Decision Brain Backtest 2016–2024 workflow.
2. Confirm the authoritative Murphy 34 source is acquired and validated.
3. Confirm the six required outputs are produced.
4. Inspect the FIRST failure only, if any.
5. Validate the canonical Decision Event semantics and as-of timestamps.
6. Accept or reject the 2016–2024 validation manifest.
7. Freeze development semantics only after the governed replay passes.
8. Run protected 2025 OOS with no tuning.
9. Then proceed to Paper → MT5 Demo → reconciliation → controlled live.

============================================================
16. SIMPLE STATUS BOARD
============================================================

PROJECT:
ACTIVE — NOT BROKEN

CANONICAL CONNECT:
PASS

REAL DECISION REPLAY:
PASS (available 2016 artifact scope)

GATE 3B:
PASS

GATE 3C SINGLE-EVENT E2E:
PASS / OPERATIONAL

FULL 2016–2024 GOVERNED BACKTEST:
NOT YET PASS

MURPHY:
34/51 GOVERNED/CLOSED
17 OPEN/DEFERRED

NISON:
44/44 FROZEN

TIZ:
PROCESS GATE ONLY; NOT_EVALUABLE WHEN UNAVAILABLE

RISK:
HARD GATE CONNECTED

TRADE PLAN:
CONNECTED / VERIFIED IN GATE 3C

MT5:
NOT YET LIVE EXECUTION

2025:
PROTECTED OOS — DO NOT TOUCH FOR TUNING

CURRENT BLOCKER:
Complete and validate the governed 2016–2024 backtest using the corrected authoritative Murphy source path.

============================================================
17. CONTINUITY INSTRUCTION FOR ANY NEW CHAT
============================================================

Read THIS FILE FIRST.

Then:
- verify current main branch state
- verify the named workflow/result artifacts
- continue from the status board
- do not restart
- do not rebuild
- do not overwrite current state with historical handoffs
- do not use the old 33/51 Murphy count
- do not call Gate 3C incomplete merely because the full 2016–2024 replay is pending
- distinguish:
  Gate 3C single-event E2E = PASS/operational
  full 2016–2024 governed backtest = NOT YET PASS

SOURCE OF CONTINUITY:
This file is the central handoff/reference document for the AI Trading Assistant — Decision Brain project as of 2026-09-03.
