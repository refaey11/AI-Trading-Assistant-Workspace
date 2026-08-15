# Murphy 0030–0032 — P&F Implementation / QA V1

Date: 2026-08-16
Status: IMPLEMENTATION READY FOR CONTRACT REVIEW — NOT PRODUCTION FROZEN

## 1. Source reconciliation

The Master Candidate Rules record maps:
- MURPHY_0030 → Chapter 11, P&F bullish support; use bullish support trendline as structural reference.
- MURPHY_0031 → Chapter 11, P&F long stop placement; stop below previous O column.
- MURPHY_0032 → Chapter 11, P&F short stop placement; stop above previous X column.

The supplied Murphy Chapter 11 source also states:
- X columns represent rising prices and O columns falling prices.
- 3-box reversal is a supported construction method.
- For a 3-box daily chart, when the current column is X, inspect High first; continue X boxes if possible and ignore Low for that day. Only when High cannot continue is Low checked for a 3-box reversal.
- When the current column is O, inspect Low first; continue O boxes if possible and ignore High for that day. Only when Low cannot continue is High checked for a 3-box reversal.
- Bullish support is drawn at 45 degrees upward/right from the base of the lowest O column.
- Long stops are placed below the previous O column; short stops above the previous X column.

## 2. Implementation delivered

Shared core:
`src/murphy_0030_0032/pnf_3box_reference.py`

Tests:
`tests/murphy_0030_0032/test_pnf_3box_reference.py`

The core deliberately keeps two items explicit rather than inventing them:
1. Box-size selection.
2. Initial chart bootstrap.

These are project parameters/operationalization boundaries, not claims that Murphy supplied one fixed GBPUSD production value.

## 3. Deterministic QA

Local test run:
- 7 tests passed.
- X-column High-first behavior: PASS.
- O-column Low-first behavior: PASS.
- 3-box reversal creation: PASS.
- Bullish support origin: PASS.
- Long/short stop reference direction: PASS.
- Deterministic replay: PASS.
- Prefix snapshot immutability / no-lookahead boundary: PASS.

## 4. Historical smoke test

Input: canonical workspace D1 series.
Rows: 2,544 (2016–2024).

Diagnostic box-size runs (NOT selected by profitability):
- 0.00584 absolute price units → 262 columns.
- 0.00600 absolute price units → 256 columns.

These runs prove the implementation can consume the historical D1 path. They do NOT freeze either value.

## 5. Box-size boundary

Murphy describes multiple valid P&F scales and also describes Kenneth Tower's logarithmic approach, where a volatility screen over the prior three years determines a percentage box size. The exact Tower screening formula is not supplied in the project source.

Therefore:
- Do not hard-code 0.58%, 0.584%, 0.6%, or another value as Murphy's GBPUSD box size.
- Do not choose a value using 2025 or historical profitability.
- The production box policy remains a separate governance gate.

## 6. Freeze gate

Current state:
- Source semantics: RESOLVED.
- Shared P&F construction core: IMPLEMENTED.
- Deterministic unit tests: PASS.
- Historical data compatibility smoke test: PASS.
- Production box-size policy: PENDING.
- Full 2016–2024 rule-specific QA: PENDING box-policy approval.
- Availability/no-lookahead audit on production evaluator: PENDING.
- Decision Brain evidence integration: PENDING freeze.

0030–0032 therefore remain NOT PRODUCTION FROZEN.

## 7. Governance boundary

This artifact does not claim that a prototype implementation is verbatim Murphy. It records the executable translation of the source-supported construction semantics and keeps unresolved project choices explicit instead of silently tuning them.
