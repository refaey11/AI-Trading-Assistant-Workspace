# Murphy 51 — Current Canonical Status V5

Date: 2026-08-15

## Completed / Frozen — 7 of 51
- 0003 — Production Frozen
- 0004 — Production Frozen
- 0006 — Frozen at Evaluator + Decision-Brain-Evidence level
- 0007 — Frozen at Evaluator + Decision-Brain-Evidence level
- 0008 — Production Frozen
- 0025 — Completed: evaluator, deterministic rule suite, full 2016–2024 replay, availability/no-lookahead, problems/solutions, backup, and freeze record completed.
- 0026 — Completed: evaluator, deterministic rule suite, full 2016–2024 replay, availability/no-lookahead, problems/solutions, backup, and freeze record completed.

## QA Pass / Freeze Candidate — not completed
- 0021
- 0022
- 0023
- 0028
- 0029

## Open / dependency states
- 0002 — Source and semantics verified; generic Timing Producer dependency remains open. Not frozen.
- Other rules retain their previously verified states until individually reconciled.

## 0025–0026 evidence record
- Deterministic rule tests: 10/10 PASS.
- Full historical replay: 55,192 H1 rows, 2016–2024.
- 0025: 6,024 PASS / 48,801 FAIL / 367 NOT_EVALUABLE.
- 0026: 5,718 PASS / 49,107 FAIL / 367 NOT_EVALUABLE.
- Historical replay checks: 8/8 PASS.
- Availability/no-lookahead checks: 8/8 PASS.
- Future-reference violations: 0.
- 2025 rows in historical replay: 0.
- Missing four-week reference remains NOT_EVALUABLE.
- Four-week window is the four completed ISO calendar weeks preceding the current ISO week; current week excluded.
- 0025 operator: current High >= preceding four-week High -> Bullish.
- 0026 operator: current Low <= preceding four-week Low -> Bearish.

## Governance
- Old handoffs are historical snapshots; newer authoritative freeze/completion records determine current state.
- Do not reopen frozen rules casually.
- Compatibility audit is required before new integration.
- Do not invent operators, thresholds, tolerances, timeframes, lookbacks, or proxies.
- 2025 is OOS and must not be used for tuning/selection.
- NOT_EVALUABLE is preferred over fabricated evidence when required inputs are missing.
- For every future rule, test specifications must be executed, not merely written, before Freeze.
