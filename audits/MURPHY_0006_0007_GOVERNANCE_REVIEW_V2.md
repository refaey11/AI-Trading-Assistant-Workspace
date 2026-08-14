# MURPHY 0006/0007 — GOVERNANCE REVIEW V2

Date: 2026-08-14
Status: GOVERNANCE NOT APPROVED / PRODUCTION FREEZE BLOCKED

## Scope
Review the current 0006/0007 operational contract against the available Murphy source/provenance artifacts and existing evaluator/QA evidence.

## Source-supported semantics
Available Murphy project source supports:
- up trendline: successive reaction lows;
- down trendline: successive reaction highs;
- tentative trendline: two points;
- confirmed trendline: third successful touch and reaction without breaking;
- additional successful tests strengthen validity.

## Current operational contract
The existing formal draft defines:
- 0006: LOW + UP; first eligible same-family pivot after line availability is the third-touch candidate; D1 range must intersect the line; next opposite-family confirmed pivot supplies the reaction; completed D1 bars must hold the line; confirmation available at reaction pivot availability.
- 0007: mirrored HIGH + DOWN logic.
- missing required evidence => NOT_EVALUABLE.
- no ATR/pip/arbitrary percentage/fixed lookback/automatic 3%/2-day binding; 2025 excluded.

## Governance finding
The operational chain is internally deterministic and has reproducibility evidence (15/15 reconciliation, 7/7 local tests, availability checks), but items such as "first eligible same-family pivot", "next opposite-family confirmed pivot", and the exact completed-D1 line-hold predicate are project operationalizations. The available source material does not establish these numeric/deterministic details as verbatim Murphy rules.

The authoritative Rule Registry search available in the current Workspace still reports 0006/0007 as requiring source-lock for successful touch, reaction, third touch, and confirmation timing. Therefore governance cannot promote the current operationalization to a production contract solely from historical reconciliation.

## Decision
KEEP:
- 0006/0007 = QA PASS FOR CURRENT OPERATIONAL CANDIDATE
- 0006/0007 != PRODUCTION FROZEN

## Required before approval
1. Recover authoritative original Rule Registry/Master Rule Database records for MURPHY_0006 and MURPHY_0007, or document that they are unrecoverable.
2. Perform explicit compatibility review of each operational clause against those records.
3. If no more specific source contract exists, obtain an explicit project governance decision accepting the operationalization as a project-level contract without representing it as verbatim Murphy.
4. Integrate the evaluator into the production path without changing semantics.
5. Run final deterministic 2016–2024 QA and availability/leakage checks.
6. Produce and approve the final freeze manifest.

## Prohibited
- Do not use 15/15 to imply source-level approval.
- Do not bind Murphy's generic 3% or 2-day examples automatically to 0006/0007.
- Do not tune on 2025.
- Do not invent thresholds to force a count.
