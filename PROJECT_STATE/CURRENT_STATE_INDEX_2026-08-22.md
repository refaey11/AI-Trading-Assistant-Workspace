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
**20 Runtime Implemented / 35 active-rule scope**

## Rule 0018 / 0019 — LIVE STATUS
- Governance/source semantics: **FROZEN**
- Freeze record: `CURRENT_MURPHY_0018_0019_FINAL_FREEZE_RECORD_2026-08-22.md`
- Runtime binding: **PENDING EXECUTABLE INTEGRATION**
- Official runtime count: still **20**, and must not become 22 until executable binding and integration tests pass.

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

### HISTORICAL / SUPERSEDED FOR LIVE-STATE PURPOSES
- `MURPHY_0018_0019_RULE_ADAPTER_COMPATIBILITY_AUDIT_V1(4)` — earlier adapter limitation
- `MURPHY_0018_0019_GOVERNANCE_DECISION_PACKET_V1(4)` — earlier governance stage
- `MURPHY_0018_0019_FINAL_GATE_STATUS_V1(4)` — earlier gate snapshot
- `MURPHY_0018_0019_PFB1_FULL_COVERAGE_REEXEC_V4(3)` — technical re-execution evidence

## Workspace rule
- `PROJECT_STATE/` = live current status only.
- `ARCHIVE/HISTORICAL/` = old snapshots and superseded artifacts.
- Every new live status file must start with `CURRENT_` or be referenced here.
- Historical artifacts cannot change live status unless explicitly promoted here.

## Immediate next work
Bind frozen Rules 0018 and 0019 into the unified runtime and run integration tests. Only after a real executable binding and passing tests may the runtime count move from 20 to 22.
