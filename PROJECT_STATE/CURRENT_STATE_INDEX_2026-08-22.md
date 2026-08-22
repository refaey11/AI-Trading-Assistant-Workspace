# CURRENT STATE INDEX — 2026-08-22

## Purpose
Single entry point for the live project state. When multiple versions exist, read this index first.

## Current operational source of truth
1. This index
2. `PROJECT_STATE/CURRENT_MURPHY_34_RUNTIME_STATUS_2026-08-22.md`
3. `PROJECT_STATE/CURRENT_MURPHY_0047_0049_RUNTIME_AUDIT_2026-08-22.md`
4. `PROJECT_STATE/CURRENT_MURPHY_0030_0033_RUNTIME_AUDIT_2026-08-22.md`
5. `PROJECT_STATE/CURRENT_MURPHY_0047_0049_RECONCILIATION_2026-08-22.md`
6. `PROJECT_STATE/CURRENT_MURPHY_27_RUNTIME_STATUS_2026-08-22.md`
7. `PROJECT_STATE/CURRENT_MURPHY_0025_0026_RUNTIME_AUDIT_2026-08-22.md`
8. `PROJECT_STATE/CURRENT_PF_B1_H1_GOVERNANCE_FREEZE_2026-08-22.md`
9. `PROJECT_STATE/CURRENT_MURPHY_0018_0019_FINAL_FREEZE_RECORD_2026-08-22.md`
10. Rule-specific newest final/approval record
11. Canonical/frozen source artifacts
12. Historical audits and recovery files

## Active runtime count
**34 Runtime Implemented / 35 active-rule scope**

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
- 0048 — Murphy TRIN 10-day MA > 1.20 evaluator + tests + unified runtime entry-point wiring; 186/186 historical labels reconciled
- 0049 — Murphy TRIN < 0.70 evaluator + tests + unified runtime entry-point wiring; 122/122 historical labels reconciled

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
- Runtime status: **VERIFIED**.

## Rules 0030–0032 — LIVE STATUS
- Governance/source status: **PRODUCTION FROZEN**.
- Runtime status: **VERIFIED**.

## Rule 0033 — LIVE STATUS
- Governance/source status: **LOCAL_PRODUCTION_FROZEN** in the canonical workspace; GitHub preserves the implementation/provenance mirror.
- Runtime status: **VERIFIED**.

## Rule 0047 — LIVE STATUS
- Runtime status: **VERIFIED**.
- Operator: `index_new_high AND ad_fails_high` from normalized canonical replay evidence.
- Historical reconciliation: 25 expected condition rows vs 25 `rule_0047` rows; 0 mismatches.

## Rules 0048 / 0049 — LIVE STATUS
- Historical closure counts: 0048 = **186**, 0049 = **122**.
- 0048 operator: `trin_ma10 > 1.20`.
- 0049 operator: `trin < 0.70`.
- Final replay reconciliation: 0048 = **186/186 exact**, 0049 = **122/122 exact**; 0 mismatches for either rule.
- Runtime evaluator: `MURPHY_EVALUATORS_V1/murphy_0048_0049_runtime_v1.py`.
- Unified entry point: `MURPHY_EVALUATORS_V1/murphy_runtime_entrypoint_v1.py`.
- Unit tests: 6/6 PASS.
- Runtime status: **VERIFIED**.
- Murphy source thresholds only; no inferred/common-market substitute logic.

## Historical 0047–0049 closure reconciliation
- Final occurrence counts: 0047 = **25**, 0048 = **186**, 0049 = **122**.
- The `24` stated in `CLOSURE.md` is stale metadata; authoritative CSV/replay evidence supports 25 for 0047.
- Coverage: 2016-01-04 through 2020-02-10; 1,033 final trading-day replay rows; 6 NYSE closure rows excluded.
- Synthetic rows: false. Proxy substitution: false. New thresholds: false. New timeframes: false.

## Current runtime set
0003, 0004, 0006, 0007, 0008, 0018, 0019, 0021, 0022, 0023, 0025, 0026, 0028, 0029, 0030, 0031, 0032, 0033, 0047, 0048, 0049, 0034–0045, 0050

## Remaining frozen-only / runtime-unproven rules
0051

## Workspace rule
- `PROJECT_STATE/` = live current status only.
- `ARCHIVE/HISTORICAL/` = old snapshots and superseded artifacts.
- Every new live status file must start with `CURRENT_` or be referenced here.
- Historical artifacts cannot change live status unless explicitly promoted here.

## Immediate next work
Proceed to 0051 compatibility audit, evaluator integration, deterministic tests, and unified runtime verification. 2025 remains OOS and must not be used for tuning or selection.
