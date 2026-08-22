# CURRENT STATE INDEX — 2026-08-22

## Purpose
Single entry point for the live project state. When multiple versions exist, read this index first.

## Current operational source of truth
1. This index
2. `PROJECT_STATE/CURRENT_MURPHY_24_RUNTIME_STATUS_2026-08-22.md`
3. `PROJECT_STATE/CURRENT_MURPHY_0018_0019_FINAL_FREEZE_RECORD_2026-08-22.md`
4. Rule-specific newest explicit final/approval record
5. Canonical/frozen source artifacts
6. Historical audits and recovery files

## Active runtime count
**24 Runtime Implemented / 35 active-rule scope**

## Newly Runtime Implemented
- 0006 — executable evaluator + tests + repository runtime entry-point integration
- 0007 — executable evaluator + tests + repository runtime entry-point integration

## Rule 0018 / 0019 — LIVE STATUS
- Governance/source semantics: **FROZEN**
- Executable evaluator module: `MURPHY_EVALUATORS_V1/murphy_0018_0019_evaluator.py`
- Exact semantics: 0018 = converging boundaries + both slopes negative; 0019 = converging boundaries + both slopes positive.
- Missing evidence: `NOT_EVALUABLE`.
- Upstream binding: `TRENDLINE_GEOMETRY → Convergence Adapter → 0018/0019 Evaluator`.
- Full-path integration: recorded PASS (6/6 test cases).
- Runtime status: **IMPLEMENTED**.

## Current runtime set
0003, 0004, 0006, 0007, 0018, 0019, 0021, 0022, 0023, 0028, 0029, 0034–0045, 0050

## Remaining frozen-only / runtime-unproven rules
0008, 0025, 0026, 0030, 0031, 0032, 0033, 0047, 0048, 0049, 0051

## Workspace rule
- `PROJECT_STATE/` = live current status only.
- `ARCHIVE/HISTORICAL/` = old snapshots and superseded artifacts.
- Every new live status file must start with `CURRENT_` or be referenced here.
- Historical artifacts cannot change live status unless explicitly promoted here.

## Immediate next work
Proceed to the next highest-priority unresolved Murphy runtime rules from the current exact mappings, starting with compatibility audit before any new integration. 2025 remains OOS and must not be used for tuning.
