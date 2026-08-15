# Murphy 0021–0023 Final Backup V1 — 2026-08-15

## Frozen scope
- MURPHY_0021
- MURPHY_0022
- MURPHY_0023

## Backup provenance
Exact source archive used in the completed historical reconciliation:
`MURPHY_EVALUATORS_V1(3).zip`

Source SHA256:
`b73d6f16893087c11f5b1cb5a8fbf2c6876779695624088cc96e1fa0850a71f2`

## Frozen evidence
- Historical population: 122,934 rows, 2020–2024.
- Raw source: 122,943 rows.
- Excluded 2025 rows: 9.
- Adapter bridge deterministic tests: 10/10 PASS.
- Availability/no-lookahead gate: PASS for historical PASS decisions.
- Future OI violations: 0.
- Missing required evidence remains NOT_EVALUABLE/non-PASS.
- No evaluator semantics, thresholds, execution timeframe, or OI proxy were changed.
- Adapter remains normalization-only; Decision Brain remains synthesis layer.

## Canonical artifact note
Canonical clean artifact identity remains:
`MURPHY_0021_0023_HISTORICAL_EVALUATION_2020_2024_CLEAN_V1.csv`

The separately recorded CLEAN_V1 payload was not independently available for byte-level SHA equality, so this backup does not claim byte identity. The raw archive plus reconciliation reports are retained as provenance evidence.

## Backup contents created locally
- Exact source archive.
- Full historical reconciliation package.
- Availability/no-lookahead audit package.
- Freeze backup manifest.

## GitHub status
This manifest is stored in the canonical repository so the frozen scope and backup provenance are discoverable from the workspace.
