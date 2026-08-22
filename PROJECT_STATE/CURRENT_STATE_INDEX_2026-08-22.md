# CURRENT STATE INDEX — 2026-08-22

## Purpose
Single entry point for the live project state. When multiple versions exist, read this index first.

## Current operational source of truth
1. This index
2. `PROJECT_STATE/CURRENT_MURPHY_27_RUNTIME_STATUS_2026-08-22.md`
3. `PROJECT_STATE/CURRENT_MURPHY_0025_0026_RUNTIME_AUDIT_2026-08-22.md`
4. `PROJECT_STATE/CURRENT_PF_B1_H1_GOVERNANCE_FREEZE_2026-08-22.md`
5. `PROJECT_STATE/CURRENT_MURPHY_0018_0019_FINAL_FREEZE_RECORD_2026-08-22.md`
6. Rule-specific newest final/approval record
7. Canonical/frozen source artifacts
8. Historical audits and recovery files

## Active runtime count
**27 Runtime Implemented / 35 active-rule scope**

## Newly Runtime Implemented
- 0006 — executable evaluator + tests + repository runtime entry-point integration
- 0007 — executable evaluator + tests + repository runtime entry-point integration
- 0008 — PF-H1/PF-B1 promoted minimal contracts + role-reversal evaluator + tests + runtime entry-point integration
- 0025 — executable evaluator + tests + unified runtime entry-point wiring; entry-point smoke test PASS
- 0026 — executable evaluator + tests + unified runtime entry-point wiring; entry-point smoke test PASS

## Rule 0008 — LIVE STATUS
- Runtime status: **IMPLEMENTED**
- Governance dependency: `CURRENT_PF_B1_H1_GOVERNANCE_FREEZE_2026-08-22.md`
- Evaluator: `MURPHY_EVALUATORS_V1/murphy_0008_runtime.py`
- Runtime entry point: `MURPHY_EVALUATORS_V1/murphy_0008_runtime_entry.py`
- Exact role-reversal evidence requires strictly ordered completed-bar events: breakout → retest → role reversal.
- Missing/ambiguous evidence: `NOT_EVALUABLE`.
- No ATR, percentage, pip, volume, or other invented numeric threshold.
- Historical replay evidence 2020–2024: 39 matched breakout events; 36 role-reversal candidates; 3 no-retest; 0 chronology violations.
- 2025 excluded from tuning/evaluation.

## Rules 0025 / 0026 — LIVE STATUS
- Governance/source status: **PRODUCTION FROZEN / COMPLETED**.
- Evidence: evaluator + deterministic tests + full 2016–2024 replay + availability/no-lookahead + freeze record.
- 0025: current High >= preceding four completed ISO calendar weeks' High -> Bullish.
- 0026: current Low <= preceding four completed ISO calendar weeks' Low -> Bearish.
- Missing four-week reference: `NOT_EVALUABLE`.
- Historical QA: 55,192 H1 rows; 0025 = 6,024 PASS / 48,801 FAIL / 367 NOT_EVALUABLE; 0026 = 5,718 PASS / 49,107 FAIL / 367 NOT_EVALUABLE; 10/10 deterministic tests; 8/8 replay checks; 8/8 availability/no-lookahead checks; 0 future-reference violations; 0 2025 rows.
- Runtime status: **VERIFIED**.
- Entry-point smoke test: PASS for 0025 PASS/FAIL/NOT_EVALUABLE cases and 0026 PASS/FAIL/NOT_EVALUABLE cases.

## Current runtime set
0003, 0004, 0006, 0007, 0008, 0018, 0019, 0021, 0022, 0023, 0025, 0026, 0028, 0029, 0034–0045, 0050

## Remaining frozen-only / runtime-unproven rules
0030, 0031, 0032, 0033, 0047, 0048, 0049, 0051

## Workspace rule
- `PROJECT_STATE/` = live current status only.
- `ARCHIVE/HISTORICAL/` = old snapshots and superseded artifacts.
- Every new live status file must start with `CURRENT_` or be referenced here.
- Historical artifacts cannot change live status unless explicitly promoted here.

## Immediate next work
Proceed to the next highest-priority unresolved Murphy runtime rules from the current exact mappings, starting with compatibility audit before any new integration. 2025 remains OOS and must not be used for tuning.