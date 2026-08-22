# CURRENT STATE INDEX — 2026-08-22

## Purpose
Single entry point for the live project state. When multiple versions exist, read this index first.

## Current operational source of truth
1. This index
2. `PROJECT_STATE/CURRENT_MURPHY_0018_0019_FINAL_FREEZE_RECORD_2026-08-22.md`
3. `PROJECT_STATE/MURPHY_20_RULE_RUNTIME_STATUS_2026-08-22.md`
4. Rule-specific newest explicit final/approval record
5. Canonical/frozen source artifacts
6. Historical audits and recovery files

## Active runtime count
**22 Runtime Implemented / 35 active-rule scope**

## Rule 0018 / 0019 — LIVE STATUS
- Governance/source semantics: **FROZEN**
- Freeze record: `CURRENT_MURPHY_0018_0019_FINAL_FREEZE_RECORD_2026-08-22.md`
- Executable evaluator module: `MURPHY_EVALUATORS_V1/murphy_0018_0019_evaluator.py`
- Exact semantics: 0018 = converging boundaries + both slopes negative; 0019 = converging boundaries + both slopes positive.
- Missing evidence: `NOT_EVALUABLE`.
- Upstream binding: `TRENDLINE_GEOMETRY → Convergence Adapter → 0018/0019 Evaluator`.
- Repository runtime entry point: `MURPHY_EVALUATORS_V1/murphy_0018_0019_runtime_entry.py`.
- Full-path integration: recorded PASS (6/6 test cases).
- Runtime status: **IMPLEMENTED**.

## Historical evidence order for 0018/0019
### CURRENT EVIDENCE
- `MURPHY_0018_0019_FINAL_BACKUP_AND_CHANGELOG_V1(5)` — 2026-08-19 21:35
  - Governance decision: `APPROVED`
  - Prepared as freeze candidates
  - 7/7 integration QA preserved
  - Missing evidence = `NOT_EVALUABLE`
  - 2025 remains OOS
- `CURRENT_MURPHY_0018_0019_FINAL_FREEZE_RECORD_2026-08-22.md`
  - Explicit owner-authorized final freeze promotion for governance/source semantics
- Runtime integration commits:
  - `19574e6f8a6b65069ba0c4104f5ac34e6e1cc1b2` — geometry/convergence binding
  - `33316a927b28efd6924a49e92da83dac8ca412f3` — runtime entry point

## Workspace rule
- `PROJECT_STATE/` = live current status only.
- `ARCHIVE/HISTORICAL/` = old snapshots and superseded artifacts.
- Every new live status file must start with `CURRENT_` or be referenced here.
- Historical artifacts cannot change live status unless explicitly promoted here.

## Immediate next work
Proceed to the next highest-priority unresolved Murphy runtime rules from the current exact mappings, starting with a compatibility audit before any new integration.
