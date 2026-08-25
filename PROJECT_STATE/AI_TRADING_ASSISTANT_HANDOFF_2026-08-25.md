# AI TRADING ASSISTANT — DECISION BRAIN
# COMPLETE HANDOFF / NEW CHAT CHECKPOINT
# Date: 2026-08-25

## 0. PURPOSE OF THIS FILE
This document is the canonical handoff for moving the project to a new ChatGPT conversation without restarting historical work.

The next chat must BEGIN FROM THE CURRENT STATE BELOW. Do NOT rebuild old components from scratch. Do NOT assume old chat claims are correct without checking the repository artifacts listed here.

The project is an AI Trading Assistant / Decision Brain, NOT a trading indicator.

Core philosophy:
- John Murphy = technical context / market structure / directional framework.
- Steve Nison = confirmation / contradiction only; Nison does not independently generate direction.
- Trading in the Zone (TIZ) = psychology/process gate only; cannot generate direction.
- Similarity / historical memory = evidence only; never sole decision maker.
- Risk engine = hard execution/risk gate.
- Decision Brain = combines current market evidence + book knowledge + historical memory + risk/process constraints.
- 2025 is OOS / evaluation-only and MUST NOT be used for tuning, threshold selection, or strategy modification.

---

## 1. CURRENT PROJECT POSITION — THE IMPORTANT TRUTH

We are NOT yet allowed to publish official 2025 profitability numbers.

The latest successful final-evaluation artifact produced:
- 6,225 final decision events for 2025.
- 0 EXECUTABLE events.
- 6,225 NO_TRADE events.
- Final trade file was effectively empty (1 byte).
- The main observed reason was RULE_ALLOWLIST_REJECT.

We audited that result and discovered TWO separate issues:

### Issue A — synthetic Nison sentinel
The final event producer emitted `NISON_NONE` when it could not choose a directionally usable Nison rule. The frozen deny-by-default allowlist correctly rejected `NISON_NONE` because it is not a real rule ID.

A provenance/wiring patch was made so the synthetic sentinel should not be treated as an authoritative rule ID.

Relevant commit:
- `e8092c3dd5f3c4ae1b5855973a17e3847fe4c90f`

Relevant audit:
- `PROJECT_STATE/FINAL_78_RULE_COMPATIBILITY_AUDIT_2026-08-25.md`

### Issue B — deeper Murphy fan-in / final wiring problem
Even after diagnosing the Nison sentinel, the final OOS path was carrying only THREE Murphy source rule IDs into the final candidate stream:
- MURPHY_0021
- MURPHY_0022
- MURPHY_0023

This does NOT mean the Decision Brain project is designed around only 3 Murphy rules.
It means the CURRENT FINAL OOS WIRING IS INCOMPLETE.

This was confirmed in the final compatibility audit.

Relevant audit:
- `PROJECT_STATE/FINAL_78_RULE_COMPATIBILITY_AUDIT_2026-08-25.md`
- `PROJECT_STATE/FINAL_78_RULE_WIRING_AUDIT_2026-08-25.md`

A fail-closed audit utility was created:
- `OOS_2025/audit_final_78_rule_wiring_v1.py`

Relevant commit:
- `a1796cace494ccb0f4f760d4e5c7c348f68bcf3b`
- `86bc7ab0f98ef14ca973309eb1e3df5d101e5395`

Therefore:
**Do NOT continue to P&L using the current 3-Murphy-rule final stream.**
That would produce a result that does not represent the intended Decision Brain.

---

## 2. 78-RULE GOVERNANCE — READ THIS CAREFULLY

The frozen Decision Brain rule allowlist currently declares:
- 44 Nison rules.
- 34 Murphy rules.
- Total = 78 verified runtime rules.

The allowlist is deny-by-default.
Unknown or non-allowlisted rule IDs must be rejected.
MURPHY_0008 is explicitly blocked.

Canonical artifact:
- `governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json`

Important correction inside that artifact:
- The corrected authoritative integration count is 78, NOT 79.
- 44 Nison + 34 Murphy.
- Murphy 0008 is excluded/blocked.

Do NOT change the allowlist just to make a run pass.

---

## 3. CRITICAL GOVERNANCE NUANCE — FROZEN VS RUNTIME IMPLEMENTED

There are historical governance/runtime documents showing a different boundary:
`PROJECT_STATE/CURRENT_MURPHY_24_RUNTIME_STATUS_2026-08-22.md`

That document says:
- 24 Runtime Implemented / 35 frozen Murphy rules.
- It lists some rules as runtime verified and others as runtime-unproven/deferred.
- It explicitly says Runtime Implemented is distinct from Production Frozen governance.

This must be reconciled with the 78-rule integration allowlist.
Do NOT silently treat a governance list as proof of end-to-end live OOS execution.

The project needs one authoritative runtime registry answering, per rule:
1. DEFINED?
2. FROZEN?
3. RUNTIME IMPLEMENTED?
4. OOS PRODUCER EXISTS?
5. FINAL BRAIN INPUT WIRED?
6. ACTUALLY OBSERVED IN FINAL OOS?

This reconciliation is the next major engineering gate.

---

## 4. THE DECISION WE AGREED ON — THE WAY TO SAVE THE PROJECT

Do NOT rebuild the project.
Do NOT delete the 34 Murphy rules.
Do NOT fake 31 missing Murphy rules.
Do NOT force all 34 to generate signals every bar.
Do NOT tune thresholds on 2025.
Do NOT calculate official P&L from the incomplete final stream.

Instead, implement ONE governed architecture fix:

# CANONICAL RUNTIME RECONCILIATION + 78-RULE FAN-IN

For every authoritative rule, establish:

DEFINED -> FROZEN -> RUNTIME IMPLEMENTED -> OOS PRODUCER -> FINAL BRAIN INPUT

Then classify evidence correctly:

ACTIVE
- real evaluator exists
- real evidence/output exists
- valid provenance
- allowed to enter Decision Brain

NOT_EVALUABLE
- rule exists and is valid
- current timestamp lacks sufficient source facts/evidence
- do NOT invent signal
- do NOT delete the rule from architecture

DEFERRED / UNPROVEN
- runtime has not been independently established
- cannot be substituted by synthetic/inferred logic
- remains explicitly unavailable until independently verified

The Final Brain must receive a FAN-IN of evidence, not one selected rule per timestamp.

Correct conceptual flow:

34 Murphy rule evidence (whatever is truly available)
+
44 Nison evidence (whatever is truly available)
+
MTF / Market State
+
Historical / Similarity Memory evidence
+
TIZ process gate
+
Risk hard gate
=
Decision Brain assessment / final decision

This means one timestamp may carry multiple real rule IDs and multiple evidence records.
A single `source_rule_id` field must NOT be used as the sole representation of the whole evidence package.

---

## 5. WHAT HAS ALREADY BEEN SUCCESSFULLY COMPLETED

### A. Nison 2025 production
A governed Nison 2025 production pipeline exists and ran successfully.
It generates `NISON_2025_FULL_EVIDENCE.csv` and a manifest.

The evidence observed in the problematic run contained all 44 Nison rule IDs, but direction values were effectively UNKNOWN for the 2025 data, so the old candidate builder could not choose a directionally usable rule and emitted `NISON_NONE`.

This is an evidence availability issue, not proof that the 44 Nison rules are absent from the repository.

### B. Murphy 0021 fresh 2025
Murphy 0021 2025 producer exists and passed its dedicated verification in the successful CI chain.

### C. Murphy 0022/0023 PIT
Murphy 0022/0023 PIT was repaired and eventually reached SUCCESS.
The actual PIT logic was not the final blocker.

Important PIT properties confirmed in the work:
- no lookahead
- no proxy
- no interpolation
- 2025 remained evaluation-only
- no tuning / threshold selection

### D. Risk execution
A Python import-path failure for `risk_engine` was fixed.
The risk stage then progressed successfully.

### E. Decision Brain import path
A second import-path failure for `RECOVERED_SOURCES` was fixed so the final Decision Brain could be imported.

### F. `os` import failure
Murphy 0022/0023 script had a post-computation failure because `os` was not imported.
The actual PIT calculations had already completed.
A small import patch fixed this class of error.

### G. CircleCI
A second CircleCI account was connected to the GitHub repository and used to run the CI/OOS pipeline after the original GitHub CI capacity issue.

Primary external services involved:
- GitHub repository: `refaey11/AI-Trading-Assistant-Workspace`
- CircleCI: `https://app.circleci.com/home`
- Dropbox: project source/data storage and artifact exchange
- Kaggle: temporary compute environment used for heavy runs / data inspection

The user does not have a computer available, so browser/cloud execution is important.

---

## 6. IMPORTANT FILES / AREAS IN GITHUB

### OOS 2025
`OOS_2025/`

Relevant items include:
- `KAGGLE_FINAL_TEST_RUNNER_V1.py`
- `run_nison_2025_full_production_v1.py`
- `verify_nison_2025_full_production_v1.py`
- `run_murphy_0021_2025_fresh_v1.py`
- `run_current_78_rule_coverage_v1.py`
- `build_historical_context_execution_inputs_v1.py`
- `build_historical_risk_evidence_v1.py`
- `core_profitability_eval_v1.py`
- `CORE_PROFITABILITY_EVAL_POLICY_V1.json`
- `OFFICIAL_PROFITABILITY_EVAL_READINESS_V1.md`
- `MURPHY_2025_COVERAGE_SNAPSHOT_V1.json`

### Murphy runtime
`MURPHY_EVALUATORS_V1/`

Key file:
- `murphy_runtime_entrypoint_v1.py`

Current entrypoint shows dispatch for a subset of Murphy rule IDs, not a full 34-rule runtime fan-in.

### Decision Brain source
`RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py`

Important role boundary:
- this V1 Decision Brain is an evidence aggregator / market-state assessment layer
- it is not itself supposed to create an unrestricted trading signal
- current implementation consumes MTF, structure, volume, historical memory evidence

### Governance
`governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json`

This is frozen integration governance and must be preserved.

### Project state / audits
`PROJECT_STATE/`

Important recent audits:
- `FINAL_78_RULE_COMPATIBILITY_AUDIT_2026-08-25.md`
- `FINAL_78_RULE_WIRING_AUDIT_2026-08-25.md`
- `CURRENT_MURPHY_24_RUNTIME_STATUS_2026-08-22.md`
- previous baseline / Murphy audits / freeze records

---

## 7. DATA SOURCES CURRENTLY USED

Authoritative 2025 H1 source:
`GBPUSD_H1_2016_2025_MASTER.csv`

Known mounted Kaggle path:
`/kaggle/input/datasets/fitnesswithmooh/ai-trading-assistant-oos-market-data-2025/GBPUSD_H1_2016_2025_MASTER/GBPUSD_H1_2016_2025_MASTER.csv`

Authoritative M1 source family:
`GBPUSD_M1_MASTER_2016_2026_V1`

Known market-state path:
`/kaggle/input/datasets/fitnesswithmooh/market/GBPUSD_MARKET_STATE.csv`

Project workspace root in Kaggle:
`/kaggle/input/datasets/fitnesswithmooh/ai-trading-assistant-workspace1`

The current OOS input used:
- 2025 H1 rows: 6,225
- total historical H1 rows: 61,417

The user previously confirmed the following source / workspace structure exists:
- OOS_2025
- PROJECT_INDEX
- risk_engine
- TESTS / tests
- contracts
- NISON_RUNTIME
- AUDITS / audits
- decision_brain
- bridges
- RECOVERED_SOURCES/DECISION_BRAIN_V1
- TRADING_IN_THE_ZONE
- compatibility
- governance
- evidence
- etc.

---

## 8. CIRCLECI / CI STRUCTURE

The repository has `.circleci/config.yml` and many governed jobs.
Jobs include tests and runtime checks for:
- Nison runtime groups
- dynamic MTF
- market state contract
- market reader contract
- market scenario contract
- historical context memory
- historical outcome memory
- similarity memory
- memory integration
- Decision Brain integration
- final E2E readiness
- risk execution runtime
- TIZ execution adapter
- pre-OOS freeze guard
- rule allowlist
- Rule Adapter allowlist gate
- frozen execution bridge
- 2025 OOS contract
- three-book decision evaluator
- Nison 2025 full production
- 78-rule coverage
- Murphy 0021 2025 fresh
- Murphy 0022/0023 2025 PIT

The latest phase has used CircleCI as the main cloud runner because GitHub Actions quota/credits were exhausted.

---

## 9. WHAT THE 78-RULE COVERAGE JOB ACTUALLY MEANS

`run_current_78_rule_coverage_v1.py` is a COVERAGE / REPORTING job.
It does not itself execute every rule end-to-end.
It counts rule rows/availability from Nison evidence and the Murphy snapshot.

Its own notes explicitly say:
- coverage/reporting only
- Murphy snapshot is reporting-only
- missing evidence stays NOT_EVALUABLE
- Final Decision Brain assembly and profitability are separate jobs
- 2025 evaluation-only / no tuning

Therefore:
**DO NOT confuse a 78-rule coverage report with proof that all 78 rules entered the live final Decision Brain event stream.**

---

## 10. THE FAILED 2025 FINAL DECISION RESULT — HOW TO INTERPRET IT

Previous final artifact:
`FINAL_2025_DECISION_EVENTS.csv`

Observed:
- 6,225 events
- 0 EXECUTABLE
- 6,225 NO_TRADE
- final trade file empty
- main reason `RULE_ALLOWLIST_REJECT`

This result is NOT a valid strategy profitability result.
It is a pipeline/wiring failure result.

Therefore:
- do not report it as 0% win rate
- do not report it as a losing strategy
- do not report it as the official OOS result
- do not tune around it

The result is useful only as a diagnostic artifact proving the final wiring was incomplete.

---

## 11. CURRENT WORKING METHOD / RULES OF ENGAGEMENT

When continuing the project:

1. AUDIT BEFORE PATCH
Always inspect existing source, contracts, tests, and audits before writing a new implementation.

2. PRESERVE EXISTING KNOWLEDGE
Never rebuild Murphy/Nison/TIZ/Memory from scratch when existing artifacts are available.

3. SEPARATE SEMANTICS FROM WIRING
If the runtime rule definition is correct but the event wiring is wrong, fix the adapter/wiring only.

4. FAIL CLOSED
Unknown rule IDs, synthetic placeholders, missing provenance, and unverified rules cannot silently become authoritative.

5. NO SYNTHETIC RULE LOGIC
Never invent thresholds/definitions merely to create output.

6. NOT_EVALUABLE IS A VALID STATE
It means evidence is unavailable/insufficient, not that the rule should disappear.

7. OOS INTEGRITY
2025 is evaluation-only. No tuning, no threshold selection, no strategy adjustment based on 2025.

8. TRACEABILITY
Every final decision must be explainable by the evidence package and provenance.

9. DO NOT DECLARE PROFITABILITY UNTIL EXECUTABLE EVENTS EXIST
P&L is downstream of valid Decision Events + execution eligibility + risk.

10. RECORD IMPORTANT STATE
Any major milestone/decision should be checkpointed to GitHub and Dropbox so a new chat can resume without history loss.

---

## 12. NEXT TASK — EXACTLY WHAT TO DO FIRST IN THE NEW CHAT

DO NOT start with the P&L.
DO NOT rerun the old final runner yet.

Start with:

### STEP 1 — Canonical Rule Registry Audit
Build a table for all authoritative 78 integration rules:
- rule_id
- family
- frozen/governance status
- runtime implementation status
- evaluator path
- OOS producer path
- test path
- current 2025 observed rows
- current 2025 PASS rows
- current 2025 NOT_EVALUABLE rows
- final-brainevidence wired? yes/no
- authoritative/deferred status

### STEP 2 — Reconcile the Murphy count conflict
The project currently contains evidence of:
- 78 integration allowlist = 34 Murphy + 44 Nison
- a separate Murphy runtime status document describing 24 runtime implemented / 35 frozen

This must be reconciled from canonical source artifacts.
Do not assume either number blindly.

### STEP 3 — Inspect all existing Murphy evaluators
Especially:
`MURPHY_EVALUATORS_V1/murphy_runtime_entrypoint_v1.py`

Compare it to the authoritative Murphy rule registry.
Determine which rules already have usable runtime evaluators and which are only governance/frozen/evidence status.

### STEP 4 — Build a GOVERNED MURPHY FAN-IN ADAPTER
Do NOT create fake evaluators.
Create one adapter that gathers all real per-rule outputs that actually exist.
For rules without runtime support, emit explicit NOT_EVALUABLE/DEFERRED metadata.

### STEP 5 — Build a timestamp-level evidence package
Do not pick one `source_rule_id` per timestamp.
Allow a list/set of valid rule IDs plus per-rule evidence/provenance.

Example conceptual output:
```
timestamp
murphy_evidence = [
  {rule_id: MURPHY_0021, status: PASS, ...},
  {rule_id: MURPHY_0022, status: FAIL, ...},
  {rule_id: MURPHY_0034, status: NOT_EVALUABLE, ...}
]
nison_evidence = [...]
tiz_gate = {...}
memory_evidence = [...]
risk_evidence = {...}
```

### STEP 6 — Update the Rule Adapter boundary
The allowlist should validate EACH real rule ID in the package.
Synthetic sentinels like `NISON_NONE` must never be introduced as rule IDs.

### STEP 7 — Add fail-closed integration tests
Tests should prove:
- all valid rule IDs are accepted
- unknown IDs rejected
- synthetic sentinel rejected/ignored as provenance placeholder, not accepted as a rule
- deferred rules cannot become authoritative
- one timestamp may contain many real evidence rule IDs
- Nison cannot generate direction alone
- TIZ cannot generate direction
- memory cannot generate direction alone

### STEP 8 — Re-run the same 2025 OOS
No strategy tuning.
No threshold changes.
No 2025-based optimization.

### STEP 9 — Inspect Final Events
Check:
- rule IDs actually present
- evidence counts
- EXECUTABLE vs NO_TRADE
- rejection reasons
- provenance completeness

### STEP 10 — ONLY THEN calculate profitability
If valid executable events exist, compute:
- trades
- wins/losses
- win rate
- profit factor
- expectancy R
- total R
- P&L
- max drawdown
- best case / core / worst case

Then record the official OOS result.

---

## 13. THE TARGET ARCHITECTURE WE ARE TRYING TO REACH

The Final Decision Brain should conceptually be:

CURRENT MARKET
-> Market State / MTF / Structure
-> Murphy contextual evidence (all available verified runtime outputs)
-> Nison confirmation / contradiction evidence
-> Historical / Similarity evidence
-> TIZ process gate
-> Decision Brain assessment
-> Risk hard gate
-> Execution eligibility
-> Trade outcome / P&L

Important role constraints:
- Murphy can provide contextual direction.
- Nison confirms/contradicts; does not independently create direction.
- TIZ does not create direction.
- Similarity is memory/evidence only.
- Risk can block execution.

---

## 14. PREVIOUS TECHNICAL FIXES / DEBUGGING HISTORY

These are useful because a future chat should not rediscover them as if they were new:

### Missing KAGGLE_FINAL_TEST_RUNNER path
A prior Kaggle command looked for:
`OOS_2025/KAGGLE_FINAL_TEST_RUNNER_V1.py`
and initially failed because of workspace/input path mismatch.
The file DOES exist in the GitHub repo at:
`OOS_2025/KAGGLE_FINAL_TEST_RUNNER_V1.py`

### Coverage script argument error
`run_current_78_rule_coverage_v1.py` requires:
- `--nison-csv`
- `--murphy-snapshot`
- `--output`

### Nison production CLI
`run_nison_2025_full_production_v1.py` requires:
- `--input`
- `--output`
- `--manifest`
Optional:
- `--context`

### `os` failure
Murphy 0022/0023 script failed after computation because `os` was not imported.

### `risk_engine` failure
Final OOS failed importing `risk_engine` from OOS_2025 context.
Fix: add correct project root / import path wiring.

### `RECOVERED_SOURCES` failure
Final Decision Brain import failed because `RECOVERED_SOURCES` was not visible from OOS_2025 execution context.
Fix: add project root / import path wiring.

### `NISON_NONE` failure
Final event producer used a synthetic sentinel for missing directional Nison evidence.
Fix direction: remove synthetic sentinel from authoritative rule IDs.

### Murphy fan-in failure
Final stream only carried 0021/0022/0023, which is the main blocker now.

---

## 15. CURRENT CHECKPOINT / WHERE WE STOPPED

We are currently stopped at:

**CANONICAL RUNTIME RECONCILIATION + MURPHY 34-RULE FAN-IN**

Not at profitability.
Not at official baseline.
Not at project freeze.

The immediate goal is to make the Final Decision Brain input faithful to the actual verified project scope and explicit about missing/deferred evidence.

After that, the same 2025 OOS test should be rerun unchanged.

---

## 16. WHAT THE NEW CHAT SHOULD SAY BACK BEFORE DOING WORK

The next chat should acknowledge:

“I have the handoff. I will NOT restart the project. I understand that the current blocker is not P&L; it is the incomplete Final Decision Brain evidence wiring. I will first reconcile the authoritative Murphy/Nison rule registry, then build/verify the governed multi-rule evidence fan-in, then rerun the same frozen 2025 OOS, and only after valid executable events exist will I calculate P&L.”

Then start from Step 1 above.

---

## 17. CHECKPOINT REFERENCES

Recent commits / artifacts used in this phase:
- `e8092c3dd5f3c4ae1b5855973a17e3847fe4c90f` — Nison provenance / `NISON_NONE` wiring correction
- `a1796cace494ccb0f4f760d4e5c7c348f68bcf3b` — final 78-rule wiring audit
- `86bc7ab0f98ef14ca973309eb1e3df5d101e5395` — fail-closed final 78-rule wiring audit script
- `5931bc27285db41b412b044f5bf40ef69d783027` — previous complete project checkpoint

Recent checkpoint stored in Dropbox:
`/AI_Trading_Assistant_PROJECT_CHECKPOINT_2026-08-25_FINAL.md`

---

## 18. FINAL WARNING FOR THE NEXT CHAT

Do NOT say:
- “all 78 rules are active”
- “Murphy is complete because the allowlist says 34”
- “0 trades means the strategy failed”
- “we can just enable the missing rules”
- “let’s tune the thresholds until trades appear”

Instead say:
- “The architecture has 78 frozen integration rule IDs, but end-to-end runtime/final OOS wiring is incomplete and must be reconciled.”
- “The current 0-trade result is diagnostic, not official performance.”
- “We need governed fan-in and canonical rule registry before profitability.”

END OF HANDOFF
