# MURPHY 0006/0007 — PROBLEMS / SOLUTIONS / EVIDENCE BACKUP V1

## Purpose
Permanent handoff record of the material problems encountered while formalizing Murphy 0006/0007, how each was resolved, and the evidence supporting the resolution. This exists to prevent repeated investigation and reliance on conversation memory.

## Final validated state
- 2016–2024 only.
- MURPHY_0006 = 8.
- MURPHY_0007 = 7.
- Total = 15.
- Historical row reconciliation = 15/15.
- Availability/lookahead violations = 0.
- 2025 confirmations = 0.
- Audit #14 on commit `c8497ef4a761856c6138a9c34c28ccd00305e99c`: 4 passed in 0.03s.
- Fresh replay did not read the reference-result artifact.
- Decision Brain integration is evidence/context only; autonomous live trading is NOT claimed.

## Problem 1 — D1/M1 lineage uncertainty
**Problem:** We needed to prove the daily series used by the evaluator was derived correctly from minute data.

**Solution:** Calendar-date aggregation reproduced the D1 reference exactly across 2,544 common 2016–2024 dates.

**Status:** CLOSED / PASS.

**Evidence:** `MURPHY_0006_0007_D1_LINEAGE_RECONCILIATION_V1.md`; Discovery Log Entry 001; `MURPHY_0006_0007_PRODUCTION_PATH_VALIDATION_V1.md`.

## Problem 2 — Invalid earlier blocker
**Problem:** An earlier blocker compared Pivot V2 event price `1.43519` with D1 low `1.40792`, treating different quantities as equivalent.

**Solution:** Identified as a category error and explicitly superseded.

**Status:** CLOSED / SUPERSEDED.

**Evidence:** Discovery Log Entry 002.

## Problem 3 — Geometry schema uncertainty
**Problem:** It was unclear whether Geometry V1 exposed enough fields for the evaluator.

**Solution:** Reconstructed the full 597,678,846-byte Rule Evaluator V2 workspace and directly inspected the Geometry build contract, manifest, QA and D1 output. Geometry V1 was proven to emit line identity, family, two anchors, slope, direction and availability.

**Status:** CLOSED.

**Evidence:** Discovery Log Entry 010; Geometry schema verification artifacts.

## Problem 4 — Geometry was expected to emit confirmation events
**Problem:** We initially had to determine whether Geometry V1 should emit third-touch, reaction and no-break.

**Solution:** The Geometry contract explicitly excludes pattern classification and breakout detection. Third-touch/reaction/no-break belong to the separate Murphy Confirmation Layer/operator. Geometry was not rebuilt.

**Status:** CLOSED.

**Evidence:** Discovery Log Entry 010; `MURPHY_0006_0007_FORMAL_PROJECT_CONTRACT_V1.md`.

## Problem 5 — PR #2 source contract vs production implementation
**Problem:** PR #2 contained a useful semantic contract but was draft-only and did not prove a production evaluator or complete upstream event schema.

**Solution:** Reused it as a semantic interface, not as production/frozen evidence. Geometry and evaluator validation were performed separately.

**Status:** CLOSED / CLARIFIED.

**Evidence:** `MURPHY_0006_0007_PR2_OPERATOR_FINDING_2026-08-13_V1.md`.

## Problem 6 — No exact numeric Murphy contract for 0006/0007
**Problem:** Murphy provides qualitative third-test/reaction/no-meaningful-break semantics, but not a verbatim deterministic numeric predicate specific to 0006/0007.

**Solution:** Adopted an explicit project operational contract and labeled it as an implementation translation, not verbatim Murphy numeric wording.

**Status:** CLOSED BY GOVERNANCE.

**Evidence:** `MURPHY_0006_0007_GOVERNANCE_DECISION_V1.md`; `MURPHY_0006_0007_FORMAL_PROJECT_CONTRACT_V1.md`; Discovery Log Entries 006–009.

## Problem 7 — 3% / 2-day examples could be misapplied
**Problem:** General Chapter 4 examples could have been incorrectly bound to 0006/0007.

**Solution:** Explicitly excluded automatic 3% and automatic 2-day binding from these rules.

**Status:** CLOSED / EXCLUDED.

**Evidence:** `MURPHY_0006_0007_NO_BREAK_CONTRACT_RECONCILIATION_V1.md`; Chapter 4 compatibility matrix; Formal Project Contract V1.

## Problem 8 — No-break governance blocker
**Problem:** `no_break_observation` existed, but it was observation-only and could not safely be renamed `no_break_valid` without an approved contract.

**Solution:** Formalized the line-hold semantics as a deterministic project operationalization: for 0006 completed D1 lows remain on/above the line between touch and reaction; for 0007 completed D1 highs remain on/below. Missing evidence remains `NOT_EVALUABLE`.

**Status:** RESOLVED AS PROJECT OPERATIONALIZATION; NOT CLAIMED AS VERBATIM MURPHY.

**Evidence:** `MURPHY_0006_0007_NO_BREAK_CONTRACT_RECONCILIATION_V1.md`; `MURPHY_0006_0007_FORMAL_PROJECT_CONTRACT_V1.md`.

## Problem 9 — Risk of invented tolerances
**Problem:** Possible shortcuts included ATR, pips, arbitrary percentages, arbitrary lookbacks and exact-collinearity.

**Solution:** All were explicitly prohibited. Exact collinearity was diagnostic only and never promoted to the touch definition.

**Status:** CLOSED / PROHIBITED.

**Evidence:** `MURPHY_0006_0007_ACTUAL_DATA_COMPATIBILITY_AUDIT_V1.md`; Formal Project Contract V1; Discovery Log Entry 009.

## Problem 10 — Raw OHLC availability
**Problem:** Initial archive inspection found Pivot/Geometry outputs but not the referenced complete D1 raw OHLC file.

**Solution:** Reconstructed the full workspace, rebuilt D1 from the supplied M1 master by calendar-date OHLC aggregation, and used that rebuilt D1 for the fresh replay.

**Status:** CLOSED FOR THE FRESH REPLAY PATH.

**Evidence:** `MURPHY_0006_0007_ACTUAL_DATA_COMPATIBILITY_AUDIT_V1.md`; `MURPHY_0006_0007_PRODUCTION_PATH_VALIDATION_V1.md`; Discovery Log Entry 012.

## Problem 11 — Skipping the first eligible third-touch candidate
**Problem:** A later candidate could be selected to manufacture a preferred historical match.

**Solution:** Corrected operator enforces the first eligible same-family pivot and regression coverage protects the behavior.

**Status:** CLOSED / TESTED.

**Evidence:** Production Path Validation V1; Formal Project Contract V1; Audit #14 artifact.

## Problem 12 — Reaction timing / lookahead risk
**Problem:** Reaction could be accepted before it was causally available.

**Solution:** Reaction event timestamp must be strictly after touch; pivot availability is the no-lookahead eligibility gate; confirmation availability is reaction pivot availability.

**Status:** CLOSED / TESTED.

**Evidence:** Production Path Validation V1; Formal Project Contract V1.

## Problem 13 — Circular validation risk
**Problem:** A 15-row reference artifact could be read and reproduced, falsely appearing as an independent replay.

**Solution:** Fresh replay did not read the reference-result artifact. It rebuilt D1 and independently reproduced 8 + 7 = 15.

**Status:** CLOSED.

**Evidence:** Production Path Validation V1; Discovery Log Entry 012.

## Problem 14 — 2025 OOS contamination
**Problem:** 2025 could contaminate operator selection or tuning.

**Solution:** 2025 was excluded from tuning, selection and replay; the contract explicitly prohibits 2025 tuning.

**Status:** CLOSED / OOS PROTECTED.

**Evidence:** Production Path Validation V1; Formal Project Contract V1; Audit #14 artifact.

## Problem 15 — CI success vs Decision Brain production integration
**Problem:** Passing deterministic tests does not prove that the evaluator is wired into the Decision Brain runtime.

**Solution:** Implemented a separate Decision Brain adapter that maps already-evaluated 0006/0007 evidence into the generic evidence shape. It does not calculate the rule or create a trade; `confidence_delta=0`.

**Status:** CLOSED AT EVIDENCE-ADAPTER LEVEL; LIVE AUTONOMOUS TRADING NOT CLAIMED.

**Evidence:** `MURPHY_0006_0007_PRODUCTION_INTEGRATION_VALIDATION_V1.md`; Audit #14 artifact.

## Problem 16 — Repeated rediscovery across chats
**Problem:** The same blockers were being rediscovered repeatedly.

**Solution:** Established an append-only Discovery Log recording discoveries, corrections, decisions and evidence references.

**Status:** CLOSED AS PROCESS CONTROL.

**Evidence:** `MURPHY_0006_0007_DISCOVERY_LOG_V1.md`; Audit #14 artifact.

## Problem 17 — Risk of overstating Freeze
**Problem:** QA PASS, replay PASS, CI PASS and Production Freeze are different claims.

**Solution:** Explicitly separated evaluator/evidence freeze from autonomous live trading. Freeze gates and manifests are maintained separately.

**Status:** CLOSED / STATUS CLARIFIED.

**Evidence:** `MURPHY_0006_0007_FORMAL_PROJECT_CONTRACT_V1.md`; `MURPHY_0006_0007_FREEZE_MANIFEST_CANDIDATE_V1.md`; `MURPHY_0006_0007_PRODUCTION_INTEGRATION_VALIDATION_V1.md`.

## Permanent rules for future work
1. Do not reopen 0006/0007 casually.
2. Do not change Pivot V2 or Geometry V1 without a new compatibility/source audit.
3. Do not tune against 2025.
4. Do not add ATR/pip/3%/2-day/hidden-lookback thresholds to recover historical counts.
5. Do not use historical result counts as permission to tune the operator.
6. Treat Murphy as the semantic source and the Project Operational Contract as the executable translation.
7. Treat Decision Brain integration as evidence/context unless a separate governance decision explicitly changes that boundary.
8. If a new issue appears, start from this backup and `MURPHY_0006_0007_DISCOVERY_LOG_V1.md` before doing any new investigation.

## Primary evidence pack
- `audits/MURPHY_0006_0007_DISCOVERY_LOG_V1.md`
- `audits/MURPHY_0006_0007_ACTUAL_DATA_COMPATIBILITY_AUDIT_V1.md`
- `audits/MURPHY_0006_0007_PR2_OPERATOR_FINDING_2026-08-13_V1.md`
- `audits/MURPHY_0006_0007_NO_BREAK_CONTRACT_RECONCILIATION_V1.md`
- `audits/MURPHY_0006_0007_FORMAL_PROJECT_CONTRACT_V1.md`
- `audits/MURPHY_0006_0007_PRODUCTION_PATH_VALIDATION_V1.md`
- `audits/MURPHY_0006_0007_PRODUCTION_INTEGRATION_VALIDATION_V1.md`
- Uploaded artifact: `0006-0007-deterministic-audit-14.zip`
