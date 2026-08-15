# Murphy 51 — Current Canonical Status V6

Date: 2026-08-15
Status: CANONICAL CORRECTION

## Completed / Frozen — 10 of 51
- 0003 — Production Frozen
- 0004 — Production Frozen
- 0006 — Frozen at Evaluator + Decision-Brain-Evidence level
- 0007 — Frozen at Evaluator + Decision-Brain-Evidence level
- 0008 — Production Frozen
- 0021 — Production Frozen
- 0022 — Production Frozen
- 0023 — Production Frozen
- 0025 — Completed: evaluator, deterministic rule suite, full 2016–2024 replay, availability/no-lookahead, problems/solutions, backup, and freeze record completed.
- 0026 — Completed: evaluator, deterministic rule suite, full 2016–2024 replay, availability/no-lookahead, problems/solutions, backup, and freeze record completed.

## QA Pass / Freeze Candidate — not completed
- 0028
- 0029

## Correction
V5 incorrectly downgraded 0021–0023 to QA Pass / Freeze Candidate. This is corrected here. The authoritative freeze snapshot commit `a707d0144edfec0b573d5410e76a9ef39f828ac1` explicitly records 0021–0023 as PRODUCTION FROZEN with evaluator/unit-test PASS, Integration Contract V2 PASS, source-locked evaluator-to-evidence bridge PASS, deterministic bridge tests 10/10 PASS, historical validation, complete availability evidence, and zero future OI violations.

No re-testing or re-opening of 0021–0023 is required. The correction is a status reconciliation only.

## 0025–0026 evidence
- Deterministic rule tests: 10/10 PASS.
- Full historical replay: 55,192 H1 rows, 2016–2024.
- 0025: 6,024 PASS / 48,801 FAIL / 367 NOT_EVALUABLE.
- 0026: 5,718 PASS / 49,107 FAIL / 367 NOT_EVALUABLE.
- Historical replay checks: 8/8 PASS.
- Availability/no-lookahead checks: 8/8 PASS.
- Future-reference violations: 0.
- 2025 rows in historical replay: 0.
- Missing four-week reference remains NOT_EVALUABLE.
- Four-week window: four completed ISO calendar weeks preceding the current ISO week; current week excluded.
- 0025: current High >= preceding four-week High -> Bullish.
- 0026: current Low <= preceding four-week Low -> Bearish.

## Governance
- Historical status files are snapshots; newer authoritative freeze/completion records determine current state.
- Do not downgrade a frozen rule based only on an older status file.
- Compatibility audit is required before new integration.
- Do not invent operators, thresholds, tolerances, timeframes, lookbacks, or proxies.
- 2025 is OOS and must not be used for tuning/selection.
- NOT_EVALUABLE is preferred over fabricated evidence.
- Test specifications must be executed, not merely written, before Freeze for future rules.
- Any semantic change to a frozen rule requires a new audit and re-freeze.
