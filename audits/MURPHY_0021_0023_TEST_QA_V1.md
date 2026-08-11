# Murphy 0021–0023 Test & QA V1

Date: 2026-08-12

## Existing evaluator

Artifact: `MURPHY_0021_0023_EVALUATOR_CONTRACT_V1.json`

Status in source artifact: `IMPLEMENTED_AND_UNIT_TESTED`.

Operationalization:
- price rising/falling = current completed close vs previous completed close
- volume rising = existing `volume_direction == UP`
- OI rising = existing CFTC futures `oi_direction == UP`
- thresholds_added = false
- proxy_oi = false
- Runtime/Dynamic MTF; no hard-coded execution timeframe
- OI scope = CME British Pound futures 096742, not spot-FX OI
- 2025_used = false

## Unit-test verification

Existing unit-test artifact:
`MURPHY_0021_0023_UNIT_TESTS_V1.csv`

All listed unit tests are marked `True`:
- 0021 bullish
- 0021 bearish
- 0021 no confirmation
- 0022 pass
- 0022 fail wrong OI
- 0023 pass
- 0023 fail wrong price
- 0022 missing OI

## Historical evidence

The source package contains:
- `MURPHY_0021_0023_HISTORICAL_EVALUATION_2020_2024.csv`
- `MURPHY_0021_0023_HISTORICAL_SUMMARY_V1.csv`

The artifact existence establishes that a 2020–2024 historical evaluation package was produced. The currently retrieved excerpt does not expose the full row-level historical results, so this audit does not invent or summarize performance metrics that are not visible.

## QA decision

**UNIT TESTS: PASS (based on preserved test artifact).**

**HISTORICAL QA: ARTIFACT PRESENT / METRICS NOT YET RE-READ FROM FULL CONTENT.**

**SEMANTIC FREEZE: NOT GRANTED YET.**

Reason: the Master Handoff explicitly warns that evaluator-file existence does not mean a rule is semantically frozen. Exact rule semantics must still be reviewed against the authoritative Murphy source, and the evaluator must then be integrated through the existing Rule Adapter without adding thresholds or changing the source rule.

## Next action

1. Verify exact 0021–0023 source wording against the Master Rule Database/source excerpt.
2. Re-read the full 2020–2024 historical summary/results.
3. Compatibility-audit Rule Adapter integration.
4. Run integration tests.
5. Only then consider READY/FROZEN status under the official project gates.

2025 remains OOS and is not used for tuning or implementation selection.
