# AI Trading Assistant — Decision Brain
## Project State / Chat Backup / Handoff — 2026-08-31

## 0. PURPOSE
This file is the continuity record for the project. A new ChatGPT chat must continue from this state and MUST NOT restart or rebuild existing components.

## 1. PROJECT IDENTITY — NON-NEGOTIABLE
- Project: AI Trading Assistant — Decision Brain.
- This is a decision system, not a trading indicator.
- Murphy = technical context / market structure / directional context.
- Nison = confirmation / contradiction only; does not independently generate direction.
- Trading in the Zone = psychology / process gate; cannot generate market direction.
- Similarity Engine / Historical Memory = evidence only; never the sole decision maker and never generates direction.
- Decision Brain combines current market evidence, book knowledge, historical memory and risk.
- Risk is a hard execution gate.
- 2025 is OOS and MUST NOT be used for tuning, calibration, or rule changes.
- Do not rebuild existing knowledge/components; audit and integrate what already exists.

## 2. VERIFIED GATE 3C STATE — COMPLETED
Gate 3C bounded event discovery and single-event E2E are operational.

Verified run:
- GitHub Actions run: 33352436711
- Discover job: 99368252868
- Conclusion: SUCCESS
- Full Brain -> Risk -> Trade Plan E2E step: SUCCESS
- Result artifact: gate3c-auto-discovery-result uploaded successfully
- Valid event discovered: 2024-12-31T16:00:00Z

Interpretation:
- Gate 3C single-event operational E2E is working.
- NO_TRADE is a valid decision, not a pipeline failure.
- Nison NOT_EVALUABLE must not automatically trigger rule rewriting or tuning; it must be interpreted through the existing governed contracts/source facts.

## 3. HISTORICAL DEBUGGING — CLOSED / NOT CURRENT BLOCKERS
Earlier failures that were debugged:
1. Dropbox 401 errors occurred with an invalid/expired token state.
2. Dropbox 409 errors occurred when paths did not match the actual Dropbox object/path contract.
3. H1/event timestamp mismatch occurred when the selected event timestamp was absent from the H1 slice.
4. An unbounded event search ran for about 20 minutes and was cancelled.
5. Bounded discovery was introduced so the system finds a common H1 + Market State + complete Nison event and tests candidates instead of hanging on one invalid timestamp.

These are historical debugging events. Do not reopen them unless a new log proves they have returned.

## 4. OFFICIAL DEVELOPMENT BACKTEST — WHAT ALREADY EXISTS
Official runner:
- BACKTEST/DEV_BACKTEST_RUNNER_V1.py

Official plan:
- BACKTEST/DEV_BACKTEST_RUNNER_PLAN_V1.md

Development scope:
- 2016-2024 only.
- 2025 remains locked OOS.

Required governed inputs/logic include the authoritative H1, Murphy, Nison, Market State/context, MTF, Historical Context Memory, Historical Outcome Memory, Similarity metadata, Context-Aware Retrieval metadata and TIZ/process context as required by the governed architecture.

Required development outputs named by the plan:
- unified_78_events_2016_2024.csv
- decision_events_2016_2024.csv
- executed_trades_2016_2024.csv
- execution_funnel_2016_2024.json
- backtest_metrics_2016_2024.json
- validation_manifest_2016_2024.json

No official profitability claim is allowed unless the validation checks pass for timestamp/as-of correctness, lookahead/leakage, MTF consumption, memory leakage, execution funnel and frozen cost/slippage assumptions.

## 5. CURRENT WORKFLOW
GitHub workflow:
- .github/workflows/development-decision-brain-backtest-2016-2024.yml

The workflow exists and is manually dispatchable.
The screenshot/Actions page confirmed the workflow is present as:
- Development Decision Brain Backtest 2016-2024

## 6. CURRENT RUN — BLOCKED AT MURPHY ACQUISITION
The latest attempted 2016-2024 development run reached the Murphy acquisition step and failed before the actual backtest.

Observed log:
- Workflow step: Recover current Murphy development evidence from Dropbox project workspace
- Script tried several guessed CSV paths.
- Every candidate returned HTTP 409 Conflict.
- Final error: `No source-backed Murphy 2016-2024 evidence found.`
- Exit code: 1.

IMPORTANT: this means the 2016-2024 backtest has NOT YET RUN. Do NOT call this a backtest failure and do NOT interpret it as a Decision Brain failure.

## 7. ROOT CAUSE NOW VERIFIED
Dropbox search found the authoritative Murphy source at:
- `/New 8/MURPHY_HISTORICAL_34_RULE_FANIN_2016_2024.zip`

Dropbox metadata verified:
- title: MURPHY_HISTORICAL_34_RULE_FANIN_2016_2024.zip
- path_display: /New 8/MURPHY_HISTORICAL_34_RULE_FANIN_2016_2024.zip
- modified: 2026-08-28T01:17:55Z
- Dropbox file id: id:u18dZfxRtWwAAAAAAAADIQ

The current GitHub workflow incorrectly looks for CSV files at `/AI_Trading_Assistant_FULL_PROJECT_V1/...` and root-level guessed paths. The authoritative object is a ZIP under `/New 8/`.

Therefore the immediate fix is WIRING/ACQUISITION ONLY:
- download the verified ZIP from `/New 8/MURPHY_HISTORICAL_34_RULE_FANIN_2016_2024.zip`
- unzip it
- locate the source-backed Murphy evidence CSV inside
- pass that CSV to the existing DEV_BACKTEST_RUNNER_V1.py

Do NOT change Murphy rules/semantics.
Do NOT substitute a legacy Murphy artifact.
Do NOT change Risk.
Do NOT change Nison.
Do NOT tune on 2025.

## 8. VERIFIED DROPBOX DEVELOPMENT SOURCES CURRENTLY PRESENT
Dropbox `/New 8/` currently contains, among other relevant governed assets:
- GBPUSD_H1_2016_2025_MASTER.zip
- GBPUSD_MARKET_STATE 6.csv
- NISON_2016_2024_FULL_EVIDENCE.csv
- NISON_DEVELOPMENT_2016_2024_MANIFEST.json
- MURPHY_HISTORICAL_34_RULE_FANIN_2016_2024.zip
- AI_TRADING_ASSISTANT_BACKTEST_PLAN.txt
- AI_TRADING_ASSISTANT_BACKTEST_ONLY_PLAN_2026-08-28.txt
- MURPHY_CANONICAL_INTEGRATION_STATE_V2_2026-08-28.txt
- GATE3C_RISK_BRIDGE_PASS_2026-08-30.md
- GATE3C_SINGLE_EVENT_E2E_PROGRESS_2026-08-30.md

## 9. LAST FOUR IMPORTANT STEPS / EVENTS
### Step 1 — Gate 3C single-event E2E
- Bounded discovery found a valid common event.
- Event: 2024-12-31T16:00:00Z.
- Full Brain -> Risk -> Trade Plan E2E passed.
- Artifact uploaded.

### Step 2 — Development 2016-2024 workflow was confirmed/used
- Existing official workflow was identified: Development Decision Brain Backtest 2016-2024.
- Existing official runner was identified: BACKTEST/DEV_BACKTEST_RUNNER_V1.py.
- No new parallel backtest architecture should be created.

### Step 3 — Development run started
- H1/Nison acquisition path was present in the workflow.
- Run progressed into source acquisition.

### Step 4 — Current blocker identified and verified
- Murphy acquisition failed with HTTP 409 for all guessed paths.
- Dropbox search independently verified the real authoritative Murphy object is `/New 8/MURPHY_HISTORICAL_34_RULE_FANIN_2016_2024.zip`.
- Therefore the next action is a narrow workflow source-path/acquisition fix, then rerun 2016-2024.

## 10. WHERE WE ARE RIGHT NOW
Current stage:
**2016-2024 Development Backtest — SOURCE ACQUISITION / MURPHY PATH FIX**

Not yet reached:
- actual 2016-2024 governed backtest execution
- validation_manifest_2016_2024.json acceptance
- Freeze
- 2025 OOS
- Demo

## 11. EXACT NEXT STEPS
1. Fix only the Murphy acquisition step in `.github/workflows/development-decision-brain-backtest-2016-2024.yml` to use the verified `/New 8/MURPHY_HISTORICAL_34_RULE_FANIN_2016_2024.zip` and extract the CSV.
2. Commit the wiring fix to `main`.
3. Run the Development Decision Brain Backtest 2016-2024 workflow.
4. If source acquisition passes, let the official `DEV_BACKTEST_RUNNER_V1.py` run.
5. Inspect the validation manifest and all required artifacts.
6. Only if the validation gate is clean: freeze the development version.
7. Then run 2025 OOS once, with NO tuning/calibration from 2025.
8. After OOS acceptance, proceed to Demo.

## 12. DO NOT DO THESE THINGS
- Do not restart the project.
- Do not rebuild Nison.
- Do not rebuild Murphy.
- Do not rewrite Decision Brain direction logic.
- Do not treat NOT_EVALUABLE as a generic failure.
- Do not use 2025 for tuning.
- Do not use the diagnostic/simplified backtest launcher as official performance.
- Do not declare 2016-2024 backtest PASS until the official runner and validation manifest actually pass.

## 13. CONTINUATION INSTRUCTION FOR THE NEXT CHAT
Start by reading this file and the current GitHub workflow. The next concrete engineering action is the Murphy source acquisition fix described in Section 7. After that, run the existing 2016-2024 governed backtest. Do not create a new architecture.
