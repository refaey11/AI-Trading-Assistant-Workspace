# AI Trading Assistant — Decision Brain
## Project State / Chat Backup / Handoff — 2026-08-31

## 0. PURPOSE
This is the continuity record for the current project state. A new ChatGPT chat must continue from here and MUST NOT restart, rebuild, retune, or replace existing components.

## 1. PROJECT IDENTITY — NON-NEGOTIABLE
- Project: AI Trading Assistant — Decision Brain.
- It is a decision system, not a trading indicator.
- Murphy = technical context / market structure / directional context.
- Steve Nison = confirmation / contradiction only; never independent direction.
- Trading in the Zone = psychology / process gate; cannot generate direction.
- Similarity Engine / Historical Memory = historical evidence only; never the sole decision maker and never direction generation.
- Decision Brain combines current market evidence, governed book knowledge, historical memory and risk.
- Risk is a hard execution gate.
- 2025 is OOS and MUST NOT be used for tuning/calibration/rule changes.
- Existing project knowledge and components are source of truth; audit/integrate, do not rebuild.

## 2. VERIFIED GATE 3C — COMPLETED
Gate 3C bounded event discovery and single-event E2E are operational.
- GitHub Actions run: 33352436711
- Discover job: 99368252868
- Conclusion: SUCCESS
- Full Brain -> Risk -> Trade Plan E2E: SUCCESS
- Result artifact: gate3c-auto-discovery-result uploaded
- Valid discovered event: 2024-12-31T16:00:00Z

Interpretation:
- Gate 3C single-event operational E2E is working.
- NO_TRADE is an allowed decision and is not a pipeline failure.
- Nison NOT_EVALUABLE observations are not a reason to rewrite/tune Nison rules.

## 3. HISTORICAL DEBUGGING ALREADY CLOSED
Earlier development issues:
- Dropbox 401: token/access problem at that time.
- Dropbox 409: incorrect/non-authoritative source paths.
- H1 timestamp mismatch: selected event absent from H1 slice.
- Unbounded event search ran ~20 minutes and was cancelled.
- Bounded event discovery was introduced to search for a common valid H1 + Market State + complete Nison event and to avoid hanging on invalid events.

Do not reopen these unless a new log proves recurrence.

## 4. OFFICIAL DEVELOPMENT BACKTEST
Official runner:
- `BACKTEST/DEV_BACKTEST_RUNNER_V1.py`

Official plan:
- `BACKTEST/DEV_BACKTEST_RUNNER_PLAN_V1.md`

Scope:
- Development validation: 2016-2024 only.
- 2025: locked OOS; no tuning/calibration from it.

The governed plan requires the authoritative historical inputs and the current Decision Brain/Risk/Execution contracts, with validation for timestamp/as-of correctness, lookahead/leakage, MTF consumption, memory leakage, execution funnel, and frozen costs/slippage.

Required development outputs:
- `unified_78_events_2016_2024.csv`
- `decision_events_2016_2024.csv`
- `executed_trades_2016_2024.csv`
- `execution_funnel_2016_2024.json`
- `backtest_metrics_2016_2024.json`
- `validation_manifest_2016_2024.json`

No official profitability claim before the validation gate is clean.

## 5. DEVELOPMENT WORKFLOW
Workflow:
- `.github/workflows/development-decision-brain-backtest-2016-2024.yml`

The workflow is manually dispatchable and is the intended 2016-2024 path.

## 6. LATEST 2016-2024 RUN FAILURE — WHAT IT ACTUALLY MEANS
The run log supplied on 2026-08-31 at about 03:43 showed:
- Failure occurred in `Recover current Murphy development evidence from Dropbox project workspace`.
- The old acquisition logic tried several guessed CSV paths.
- Every guessed path returned HTTP 409 Conflict.
- Final error: `No source-backed Murphy 2016-2024 evidence found.`
- Exit code: 1.

IMPORTANT:
This was a SOURCE ACQUISITION FAILURE, not a backtest/Decision Brain failure. The official 2016-2024 runner had not yet been reached in that attempt.

## 7. MURPHY SOURCE — VERIFIED AND FIXED
Dropbox search independently verified the authoritative source:
- `/New 8/MURPHY_HISTORICAL_34_RULE_FANIN_2016_2024.zip`
- Dropbox file id: `id:u18dZfxRtWwAAAAAAAADIQ`
- modified: `2026-08-28T01:17:55Z`

The GitHub workflow has now been corrected to use that exact verified ZIP, unzip it, inspect CSV candidates, require timestamp + rule_id/source_rule_id, require at least 34 unique Murphy rules, require scope through 2024, and then pass the selected governed CSV to the existing backtest runner.

Verified GitHub fix commit:
- `073520e2b3162fbed9d803a7ddee4f384adf4b0d`
- message: `fix: use actual Murphy 2016-2024 Dropbox source`
- created: 2026-08-31T03:45:16Z

This is a WIRING/SOURCE ACQUISITION fix only. It does not change Murphy rule semantics.

## 8. VERIFIED DROPBOX SOURCES PRESENT IN /New 8/
Relevant sources verified in Dropbox include:
- `GBPUSD_H1_2016_2025_MASTER.zip`
- `GBPUSD_MARKET_STATE 6.csv`
- `NISON_2016_2024_FULL_EVIDENCE.csv`
- `NISON_DEVELOPMENT_2016_2024_MANIFEST.json`
- `MURPHY_HISTORICAL_34_RULE_FANIN_2016_2024.zip`
- `AI_TRADING_ASSISTANT_BACKTEST_PLAN.txt`
- `AI_TRADING_ASSISTANT_BACKTEST_ONLY_PLAN_2026-08-28.txt`
- `MURPHY_CANONICAL_INTEGRATION_STATE_V2_2026-08-28.txt`
- `GATE3C_RISK_BRIDGE_PASS_2026-08-30.md`
- `GATE3C_SINGLE_EVENT_E2E_PROGRESS_2026-08-30.md`

## 9. LAST FOUR IMPORTANT STEPS / EVENTS
### 1) Gate 3C single-event E2E passed
- Bounded discovery found `2024-12-31T16:00:00Z`.
- Full Brain -> Risk -> Trade Plan E2E passed.
- Result artifact uploaded.

### 2) Official 2016-2024 development workflow identified and used
- Existing workflow: `Development Decision Brain Backtest 2016-2024`.
- Existing runner: `BACKTEST/DEV_BACKTEST_RUNNER_V1.py`.
- No parallel backtest architecture should be created.

### 3) First 2016-2024 attempt reached source acquisition and failed
- H1/Nison acquisition logic was present.
- Murphy acquisition failed because the workflow was using guessed CSV paths.
- The failure was HTTP 409 path mismatch, not a model/backtest failure.

### 4) Murphy source path was independently verified and workflow fixed
- Dropbox confirmed `/New 8/MURPHY_HISTORICAL_34_RULE_FANIN_2016_2024.zip`.
- GitHub commit `073520e2...` corrected the workflow to download the verified ZIP, extract it, validate the CSV schema/scope, and use it.
- Therefore the OLD 03:43 failure should NOT be rerun as-is; the workflow must be run from the latest fixed `main` version.

## 10. CURRENT EXACT POSITION
Current stage:
**2016-2024 Development Backtest — READY TO RERUN AFTER MURPHY SOURCE-PATH FIX**

Completed:
- Gate 3C bounded discovery: YES
- Gate 3C single-event E2E: YES
- Authoritative Murphy source located: YES
- Murphy workflow acquisition fix committed: YES

Not completed yet:
- Successful end-to-end 2016-2024 governed backtest run
- `validation_manifest_2016_2024.json` acceptance
- Development freeze
- 2025 OOS
- Demo

## 11. WHAT WE ARE WORKING ON RIGHT NOW
ONLY this:
**Run the latest fixed `Development Decision Brain Backtest 2016-2024` workflow.**

The next expected checkpoint is the Murphy acquisition step. It should now download:
`/New 8/MURPHY_HISTORICAL_34_RULE_FANIN_2016_2024.zip`

Then:
1. extract and validate Murphy CSV
2. acquire H1 / Market State / Nison
3. run `DEV_BACKTEST_RUNNER_V1.py`
4. produce the required 2016-2024 artifacts
5. inspect `validation_manifest_2016_2024.json`

## 12. NEXT 4 PROJECT STEPS — AFTER CURRENT RUN
1. **2016-2024 governed backtest PASS**
2. **Freeze development version** if all acceptance checks pass
3. **2025 OOS** — no tuning/calibration/rule changes from 2025
4. **Demo** after OOS acceptance

## 13. DO NOT DO
- Do not restart the project.
- Do not rebuild Murphy.
- Do not rebuild Nison.
- Do not rewrite Decision Brain direction logic.
- Do not treat a single `NOT_EVALUABLE` as a generic system failure.
- Do not use 2025 for tuning.
- Do not treat the old 03:43 Murphy 409 as a current backtest failure after the 03:45 source-path fix.
- Do not declare 2016-2024 PASS until the official runner and validation manifest actually pass.
- Do not substitute a diagnostic/simplified backtest for the governed runner.

## 14. CONTINUATION INSTRUCTION FOR THE NEXT CHAT
Read this handoff first. The immediate action is to run the latest `Development Decision Brain Backtest 2016-2024` workflow from `main`. If it fails, classify the failure from the first failing step before changing anything. Preserve the architecture and governance above.
