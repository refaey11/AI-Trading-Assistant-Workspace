# CURRENT STATE INDEX — 2026-08-22

## Purpose
Single entry point for the live project state. When multiple versions exist, read this index first.

## Current operational source of truth
1. This index
2. `PROJECT_STATE/CURRENT_MURPHY_31_RUNTIME_STATUS_2026-08-22.md`
3. `PROJECT_STATE/CURRENT_MURPHY_0030_0033_RUNTIME_AUDIT_2026-08-22.md`
4. `PROJECT_STATE/CURRENT_MURPHY_0047_0049_RUNTIME_AUDIT_2026-08-22.md`
5. `PROJECT_STATE/CURRENT_MURPHY_0047_0049_RECONCILIATION_2026-08-22.md`
6. `PROJECT_STATE/CURRENT_MURPHY_27_RUNTIME_STATUS_2026-08-22.md`
7. `PROJECT_STATE/CURRENT_MURPHY_0025_0026_RUNTIME_AUDIT_2026-08-22.md`
8. `PROJECT_STATE/CURRENT_PF_B1_H1_GOVERNANCE_FREEZE_2026-08-22.md`
9. `PROJECT_STATE/CURRENT_MURPHY_0018_0019_FINAL_FREEZE_RECORD_2026-08-22.md`
10. Rule-specific newest final/approval record
11. Canonical/frozen source artifacts
12. Historical audits and recovery files

## Active runtime count
**32 Runtime Implemented / 35 active-rule scope**

## Newly Runtime Implemented
- 0006 — executable evaluator + tests + repository runtime entry-point integration
- 0007 — executable evaluator + tests + repository runtime entry-point integration
- 0008 — PF-H1/PF-B1 promoted minimal contracts + role-reversal evaluator + tests + runtime entry-point integration
- 0025 — executable evaluator + tests + unified runtime entry-point wiring; entry-point smoke test PASS
- 0026 — executable evaluator + tests + unified runtime entry-point wiring; entry-point smoke test PASS
- 0030 — frozen P&F bullish support reference adapter + unified runtime entry-point wiring; smoke PASS
- 0031 — frozen P&F long stop reference adapter + unified runtime entry-point wiring; smoke PASS
- 0032 — frozen P&F short stop reference adapter + unified runtime entry-point wiring; smoke PASS
- 0033 — frozen contextual candle-filter evaluator adapter + unified runtime entry-point wiring; smoke PASS
- 0047 — normalized index/A-D divergence evaluator + unified runtime entry-point wiring; 4/4 smoke PASS; 25/25 historical replay labels reconciled

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

## Rules 0030–0032 — LIVE STATUS
- Governance/source status: **PRODUCTION FROZEN**.
- Shared core: `src/murphy_0030_0032/pnf_3box_reference.py`.
- Rule semantics: 0030 = P&F bullish support reference; 0031 = BELOW_PREVIOUS_O_COLUMN; 0032 = ABOVE_PREVIOUS_X_COLUMN.
- Project operationalization (bootstrap/box scaling) remains explicitly project-defined, not Murphy/Tower numeric source truth.
- Runtime adapters: `MURPHY_EVALUATORS_V1/murphy_0030_0032_runtime_v1.py`.
- Unified entry point integrated: `MURPHY_EVALUATORS_V1/murphy_runtime_entrypoint_v1.py`.
- Smoke verification: PASS for all three outputs and missing-evidence NOT_EVALUABLE behavior.
- 2025 remains OOS; no profitability-based parameter selection.

## Rule 0033 — LIVE STATUS
- Governance/source status: **LOCAL_PRODUCTION_FROZEN** in the canonical workspace; GitHub preserves the implementation/provenance mirror.
- Semantics: neutral contextual candle filter; reversal candle + short-term trend + Stochastics %D presignal; no independent BUY/SELL generation.
- Runtime adapter: `MURPHY_EVALUATORS_V1/murphy_0033_runtime_v1.py`.
- Unified entry point integrated and smoke-verified.
- Historical QA: 273,387 rows, 2016–2024; prefix/no-lookahead PASS; 2025 excluded.

## Rule 0047 — LIVE STATUS
- Governance/source status: historical closure evidence reconciled.
- Runtime status: **VERIFIED**.
- Operator: `index_new_high AND ad_fails_high` from normalized canonical replay evidence.
- Historical reconciliation: 25 expected condition rows vs 25 `rule_0047` rows; 0 mismatches.
- Runtime evaluator: `MURPHY_EVALUATORS_V1/murphy_0047_runtime_v1.py`.
- Unified entry point: `MURPHY_EVALUATORS_V1/murphy_runtime_entrypoint_v1.py`.
- Deterministic smoke: 4/4 PASS.
- 2025 not used.

## Rules 0048 / 0049 — LIVE STATUS
- Historical closure counts remain 186 / 122 and source TRIN evidence is available.
- Exact source-locked rule operators are not recovered in the current runtime audit.
- Runtime status: **NOT_EVALUABLE / UNPROVEN**.
- No inferred/common-market TRIN thresholds or proxy logic allowed.

## Historical 0047–0049 closure reconciliation
- Final occurrence counts: 0047 = **25**, 0048 = **186**, 0049 = **122**.
- The `24` stated in `CLOSURE.md` is stale metadata; authoritative CSV/replay evidence supports 25 for 0047.
- Coverage: 2016-01-04 through 2020-02-10; 1,033 final trading-day replay rows; 6 NYSE closure rows excluded.
- Synthetic rows: false. Proxy substitution: false. New thresholds: false. New timeframes: false.

## Current runtime set
0003, 0004, 0006, 0007, 0008, 0018, 0019, 0021, 0022, 0023, 0025, 0026, 0028, 0029, 0030, 0031, 0032, 0033, 0047, 0034–0045, 0050

## Remaining frozen-only / runtime-unproven rules
0048, 0049, 0051

## Workspace rule
- `PROJECT_STATE/` = live current status only.
- `ARCHIVE/HISTORICAL/` = old snapshots and superseded artifacts.
- Every new live status file must start with `CURRENT_` or be referenced here.
- Historical artifacts cannot change live status unless explicitly promoted here.

## Immediate next work
Proceed to 0048–0049 operator-contract investigation, then 0051. 2025 remains OOS and must not be used for tuning or selection.
