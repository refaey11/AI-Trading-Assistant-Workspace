# CURRENT STATE INDEX — 2026-08-22

## Purpose
This is the single entry point for the current project state. When multiple versions of the same work exist, **read this index first**.

## Current operational source of truth
1. `PROJECT_STATE/MURPHY_20_RULE_RUNTIME_STATUS_2026-08-22.md`
2. This index
3. Rule-specific newest explicit final/approval record
4. Canonical/frozen source artifacts
5. Historical audits, recovery files, and changelogs

## Active runtime count
**20 Runtime Implemented / 35 active-rule scope**

## Rule 0018 / 0019 latest evidence order
### CURRENT
- `MURPHY_0018_0019_FINAL_BACKUP_AND_CHANGELOG_V1(5)` — 2026-08-19 21:35
  - Governance decision: `APPROVED`
  - Status wording: approved integration and prepared as freeze candidates
  - 7/7 Integration QA recorded in the preserved implementation package
  - Missing evidence remains `NOT_EVALUABLE`
  - 2025 remains OOS

### HISTORICAL / SUPERSEDED FOR CURRENT-STATE PURPOSES
- `MURPHY_0018_0019_RULE_ADAPTER_COMPATIBILITY_AUDIT_V1(4)` — 2026-08-19 14:22
  - `DESIGN_ONLY`; `NOT_FROZEN`
  - Explains an earlier adapter limitation; it must not override the later governance approval.
- `MURPHY_0018_0019_GOVERNANCE_DECISION_PACKET_V1(4)` — 2026-08-19 04:36
  - Earlier governance stage.
- `MURPHY_0018_0019_FINAL_GATE_STATUS_V1(4)` — 2026-08-19 04:35
  - Earlier gate snapshot.
- `MURPHY_0018_0019_PFB1_FULL_COVERAGE_REEXEC_V4(3)` — 2026-08-19 04:21
  - Technical re-execution evidence.

## Workspace organization rule from now on
- `PROJECT_STATE/` = current status only.
- `ARCHIVE/HISTORICAL/` = old snapshots, superseded audits, and prior-stage artifacts.
- Every new status file must start with `CURRENT_` or be referenced by this index.
- No old artifact may change the live project count unless it is explicitly promoted here.

## Immediate next work
Continue runtime implementation on the remaining rules while keeping 0018/0019 as **approved freeze candidates pending recorded executable runtime binding**, unless a newer explicit final freeze/runtime artifact is found.
