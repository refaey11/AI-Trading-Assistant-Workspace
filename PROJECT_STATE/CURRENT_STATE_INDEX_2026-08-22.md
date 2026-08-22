# CURRENT STATE INDEX — 2026-08-22

## Purpose
Single entry point for the live project state. When multiple versions exist, read this index first.

## Current operational source of truth
1. This index
2. `PROJECT_STATE/CURRENT_MURPHY_35_RUNTIME_STATUS_2026-08-22.md`
3. `PROJECT_STATE/CURRENT_MURPHY_0047_0049_RUNTIME_AUDIT_2026-08-22.md`
4. `PROJECT_STATE/CURRENT_MURPHY_0030_0033_RUNTIME_AUDIT_2026-08-22.md`
5. `PROJECT_STATE/CURRENT_MURPHY_0047_0049_RECONCILIATION_2026-08-22.md`
6. Rule-specific newest final/approval record
7. Canonical/frozen source artifacts
8. Historical audits and recovery files

## Active runtime count
**35 Runtime Implemented / 35 active-rule scope**

## Newly Runtime Implemented
- 0006 — executable evaluator + tests + repository runtime entry-point integration
- 0007 — executable evaluator + tests + repository runtime entry-point integration
- 0008 — PF-H1/PF-B1 promoted minimal contracts + role-reversal evaluator + tests + runtime entry-point integration
- 0025 — executable evaluator + tests + unified runtime entry-point wiring; entry-point smoke test PASS
- 0026 — executable evaluator + tests + unified runtime entry-point wiring; entry-point smoke test PASS
- 0030 — frozen P&F bullish support reference adapter + unified runtime entry-point wiring; smoke PASS
- 0031 — frozen P&F long stop reference adapter + unified runtime entry-point wiring; smoke PASS
- 0032 — frozen P&F short stop reference adapter + unified runtime entry-point wiring; smoke PASS
- 0033 — frozen contextual candle-filter evaluator + unified runtime entry-point wiring; smoke PASS
- 0047 — normalized index/A-D divergence evaluator + unified runtime entry-point wiring; 4/4 smoke PASS; 25/25 historical replay labels reconciled
- 0048 — Murphy TRIN 10-day MA > 1.20 evaluator + tests + unified runtime entry-point wiring; 186/186 historical labels reconciled
- 0049 — Murphy TRIN < 0.70 evaluator + tests + unified runtime entry-point wiring; 122/122 historical labels reconciled
- 0051 — process-gate evaluator + tests + unified runtime entry-point dispatch; PASS/FAIL/NOT_EVALUABLE smoke 3/3

## Rule 0051 — LIVE STATUS
- Governance/source status: **PROCESS_GATE_FROZEN / CLOSED**.
- Gate: `PLAN_COMPLETE`.
- Required fields: direction, stance, position_size, acceptable_loss, profit_objective, entry, order_type, stop_loss.
- PASS: all eight fields explicitly present and non-empty.
- FAIL: any required field explicitly missing/empty.
- NOT_EVALUABLE: required field status unknown/unavailable.
- Direction generation: **false**; the gate checks completeness of an already-produced plan and does not generate BUY/SELL or invent risk/execution policy.
- Source QA: deterministic tests 3/3 PASS; historical market replay NOT_APPLICABLE_AS_MARKET_SIGNAL; 2025 not used.
- Runtime evaluator: `MURPHY_EVALUATORS_V1/murphy_0051_runtime_v1.py`.
- Runtime tests: `MURPHY_EVALUATORS_V1/test_murphy_0051_runtime_v1.py`.
- Unified entry point: `MURPHY_EVALUATORS_V1/murphy_runtime_entrypoint_v1.py`.
- Full-path dispatch smoke executed against the same adapter/entry-point logic: **3/3 PASS** for PASS / FAIL / NOT_EVALUABLE.
- Verification boundary: GitHub Actions CI was not manually triggered because the available GitHub connector exposes workflow inspection but not workflow dispatch. The recorded PASS is direct execution smoke, not a claimed CI run.

## Rules 0047–0049 — LIVE STATUS
- 0047 runtime: VERIFIED; operator `index_new_high AND ad_fails_high`; 25/25 historical labels reconciled.
- 0048 runtime: VERIFIED; operator `trin_ma10 > 1.20`; 186/186 exact historical match.
- 0049 runtime: VERIFIED; operator `trin < 0.70`; 122/122 exact historical match.
- 2025 not used; no proxy substitution; no invented thresholds.

## Historical 0047–0049 closure reconciliation
- Final occurrence counts: 0047 = **25**, 0048 = **186**, 0049 = **122**.
- The `24` stated in `CLOSURE.md` is stale metadata; authoritative CSV/replay evidence supports 25 for 0047.
- Coverage: 2016-01-04 through 2020-02-10; 1,033 final trading-day replay rows; 6 NYSE closure rows excluded.
- Synthetic rows: false. Proxy substitution: false. New thresholds: false. New timeframes: false.

## Remaining frozen-only / runtime-unproven rules
**None in the 35-rule active scope.**

## Workspace rule
- `PROJECT_STATE/` = live current status only.
- `ARCHIVE/HISTORICAL/` = old snapshots and superseded artifacts.
- Every new live status file must start with `CURRENT_` or be referenced here.
- Historical artifacts cannot change live status unless explicitly promoted here.

## Immediate next work
The 35-rule Murphy runtime scope is complete. Next work should be integration-level validation of the broader Decision Brain, not reopening these frozen rule contracts. 2025 remains OOS and must not be used for tuning or selection.
