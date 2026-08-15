# Murphy 0025–0026 — Final Freeze Manifest V1
Date: 2026-08-15
Status: FREEZE CANDIDATE — PRODUCTION FREEZE DECISION PENDING

## Rule operators
0025: current High >= highest High from the preceding four completed ISO calendar weeks -> Bullish.
0026: current Low <= lowest Low from the preceding four completed ISO calendar weeks -> Bearish.
Current week excluded.

## QA evidence
- Deterministic replay: 5/5 PASS.
- Full historical replay: 55,192 rows (2016–2024).
- Four-Week reference rows: 54,825.
- 0025: 6,024 PASS / 48,801 FAIL / 367 NOT_EVALUABLE.
- 0026: 5,718 PASS / 49,107 FAIL / 367 NOT_EVALUABLE.
- Historical checks: 8/8 PASS.
- Availability/no-lookahead checks: 8/8 PASS.
- Future-reference violations: 0.
- 2025 historical rows: 0.

## Implementation finding
Existing H1 new_four_week_high/new_four_week_low fields are not treated as authoritative row-level triggers. The evaluator uses current High/Low against the authoritative weekly Four-Week reference.

## Governance
No fixed-bar substitution, new thresholds, or 2025 tuning. Missing references remain NOT_EVALUABLE. Any evaluator/contract/feature semantic change requires a new compatibility audit and re-freeze.

## Decision
Technical QA gates PASS. This file is a final freeze candidate. Production Frozen status requires an explicit governance decision and must not be inferred from this manifest alone.