# Murphy 0021–0023 — Canonical Integration Gate V1

Date: 2026-08-15
Status: INTEGRATION GATE OPEN — PRODUCTION FREEZE NOT GRANTED

## Historical artifact
The canonical clean artifact is:
`MURPHY_0021_0023_HISTORICAL_EVALUATION_2020_2024_CLEAN_V1.csv`

Verified record:
- 122,934 rows
- 2020–2024 only
- 2025 rows = 0
- Historical cleanliness/provenance = PASS

The previously observed 9 rows dated 2025-01-01 belong to a non-clean/raw artifact and are NOT a blocker for the canonical clean artifact.

## Evaluator
The existing 0021–0023 evaluator remains authoritative and unchanged.
- Dynamic MTF
- no added thresholds
- no spot-FX OI proxy
- CFTC futures OI input
- 2025 excluded from tuning/selection

## Integration gate
The remaining gate is evaluator-result -> canonical Decision-Brain evidence integration.

Required sequence:
1. Preserve the evaluator result losslessly at the bridge boundary.
2. Apply only an explicitly approved canonical mapping into the Rule Adapter evidence contract.
3. Execute deterministic adapter tests.
4. Reconcile all 122,934 clean historical results.
5. Run availability/no-lookahead checks.
6. Produce final freeze manifest only if every gate passes.

## Governance constraints
- Do not modify evaluator semantics.
- Do not invent thresholds, timeframes, lookbacks, OI proxies, strength, or confidence.
- Do not map NOT_EVALUABLE by assumption unless the canonical contract explicitly permits it.
- Do not use 2025 for tuning or selection.
- Do not reopen frozen rules.

## Current decision
Historical gate: PASS.
Canonical integration: OPEN.
Production Freeze: NOT GRANTED.
