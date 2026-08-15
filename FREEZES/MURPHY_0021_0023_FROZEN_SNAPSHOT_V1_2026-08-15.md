# Murphy 0021–0023 — Frozen Snapshot V1

Date: 2026-08-15
Status: PRODUCTION FROZEN

## Scope
0021, 0022, 0023 only.

## Evidence gates
- Evaluator + unit tests: PASS
- Integration Contract V2: PASS
- Source-locked evaluator-to-evidence bridge: PASS
- Deterministic bridge tests: 10/10 PASS
- Historical 2020–2024 population: 122,934 rows
- Raw source: 122,943 rows; 9 rows dated 2025-01-01 excluded
- Historical PASS decisions: 31,510
- PASS decisions with required availability evidence: 31,510/31,510
- Future OI availability violations: 0
- Missing evidence remains NOT_EVALUABLE/non-PASS

## Governance
- No evaluator rebuild.
- No added thresholds.
- No hard-coded execution timeframe.
- No spot-FX OI proxy.
- 2025 excluded from tuning/selection.
- Adapter is normalization-only.
- Decision Brain remains the synthesis layer.

## Provenance
Canonical clean artifact identity:
`MURPHY_0021_0023_HISTORICAL_EVALUATION_2020_2024_CLEAN_V1.csv`

Accessible raw provenance archive SHA256:
`b73d6f16893087c11f5b1cb5a8fbf2c6876779695624088cc96e1fa0850a71f2`

The raw archive is not claimed byte-identical to a separately unavailable CLEAN_V1 payload.

## Change control
Any modification to evaluator semantics, integration mapping, thresholds, timeframe policy, OI source, or evidence interpretation invalidates this freeze and requires a new audit and freeze version.
