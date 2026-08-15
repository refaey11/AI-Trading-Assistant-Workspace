# Murphy 51 — Current Canonical Status V6

Date: 2026-08-15
Status: CANONICAL CORRECTION + 0028 FREEZE

## Completed / Frozen — 11 of 51
- 0003 — Production Frozen
- 0004 — Production Frozen
- 0006 — Frozen at Evaluator + Decision-Brain-Evidence level
- 0007 — Frozen at Evaluator + Decision-Brain-Evidence level
- 0008 — Production Frozen
- 0021 — Production Frozen
- 0022 — Production Frozen
- 0023 — Production Frozen
- 0025 — Production Frozen
- 0026 — Production Frozen
- 0028 — Production Frozen

## QA Pass / Freeze Candidate — not completed
- 0029

## 0028 Freeze Evidence
- Full historical evidence: 2016–2024.
- Historical QA: PASS.
- Integrated availability/no-lookahead: PASS.
- Duplicate events: 0.
- Missing availability: 0.
- 2025 rows used: 0.
- Evidence rows: 5,819.
- 0028 PASS: 2,889.
- 0028 FAIL: 2,930.
- RSI(14) controlled recovery was reverse-validated against the existing 2020–2024 divergence artifact before historical extension.
- Existing rule semantics, evaluator, divergence contract, Pivot Sequence V2, and source-locked bridge were preserved.
- Freeze record: `project_state/MURPHY_0028_PRODUCTION_FREEZE_V1.md`.

## Governance
- Historical status files are snapshots; newer authoritative freeze/completion records determine current state.
- Do not downgrade a frozen rule based only on an older status file.
- Compatibility audit is required before new integration.
- Do not invent operators, thresholds, tolerances, timeframes, lookbacks, or proxies.
- 2025 is OOS and must not be used for tuning/selection.
- NOT_EVALUABLE is preferred over fabricated evidence.
- Any semantic change to a frozen rule requires a new audit and re-freeze.
