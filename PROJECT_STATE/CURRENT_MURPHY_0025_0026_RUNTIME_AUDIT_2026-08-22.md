# Murphy 0025 / 0026 — Current Runtime Audit

Date: 2026-08-22

## Canonical rule status
0025 and 0026 are **PRODUCTION FROZEN / COMPLETED** according to the authoritative historical freeze record.

## Frozen semantics
- 0025: current High >= preceding four completed ISO calendar weeks' High -> Bullish.
- 0026: current Low <= preceding four completed ISO calendar weeks' Low -> Bearish.
- Current ISO week is excluded.
- Missing four-week reference -> NOT_EVALUABLE.
- No invented thresholds, tolerances, proxies, or alternate lookback definitions.

## Verified historical evidence
- Deterministic tests: 10/10 PASS.
- Historical replay: 55,192 H1 rows, 2016-2024.
- 0025: 6,024 PASS / 48,801 FAIL / 367 NOT_EVALUABLE.
- 0026: 5,718 PASS / 49,107 FAIL / 367 NOT_EVALUABLE.
- Historical replay checks: 8/8 PASS.
- Availability/no-lookahead: 8/8 PASS.
- Future-reference violations: 0.
- 2025 rows: 0.

## Runtime determination
The available GitHub evidence proves evaluator + deterministic tests + historical QA + freeze evidence, but does **not** prove a repository runtime entry-point / unified-runtime wiring for 0025 or 0026.

Therefore:
- 0025 Runtime: **NOT_PROVEN**
- 0026 Runtime: **NOT_PROVEN**
- Active runtime count remains **25/35**.

## Next action
Audit existing Four-Week Lookback evaluator/adapter and repository runtime entry-point. Reuse existing infrastructure; do not rebuild it. Promote to Runtime only after executable routing and integration tests are demonstrated.
