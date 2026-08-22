# CURRENT Murphy 0029 Freeze Reconciliation — 2026-08-22

## Current evidence
- 0029 Runtime Adapter + historical replay are present.
- Historical QA window: 2016-2024.
- 5,819 events; 2,930 PASS; 2,889 FAIL.
- Duplicates: 0.
- Required-field gaps: 0.
- Availability-before-pivot violations: 0.
- 2025 rows: 0.
- Existing shared evaluator/divergence evidence is reused; no semantic rebuild.

## Governance status
- Uploaded continuity backup says a later dedicated production-freeze record exists for 0029.
- The dedicated freeze record is not currently discoverable through the GitHub code-search surface, so the GitHub mirror cannot independently verify the final governance record yet.
- Therefore this record keeps 0029 as `FREEZE_CANDIDATE_REQUIRES_RECONCILIATION` rather than fabricating a freeze.

## Runtime status
- Executable adapter: READY
- Historical replay: PASS
- Official active runtime count: unchanged at 22/35 until governance/provenance freeze is mirrored and the unified runtime integration test passes.

## Boundaries
- Do not rebuild the shared 0027-0029 evaluator.
- Do not alter divergence semantics, timeframe, lookback, thresholds, or availability semantics.
- 2025 remains OOS.
- Missing evidence remains NOT_EVALUABLE.
