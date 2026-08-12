# Murphy 0006/0007 — Candidate QA V3 Correction

Status: CORRECTED / CANDIDATE-ONLY
Date: 2026-08-13

## Issue found
The first rebuilt candidate dataset was labeled 2016–2024 but the runner did not explicitly cap candidate timestamps at 2024-12-31. The canonical D1 pivot source contains later observations, so the first rebuild included 2025 and 2026 candidate timestamps.

This was caught during the historical QA gate before any confirmation or PASS/FAIL promotion.

## Correction
The corrected population is restricted to candidate timestamps from 2016-01-01 through 2024-12-31 inclusive.

Corrected candidates:
- MURPHY_0006: 166
- MURPHY_0007: 181
- Total: 347

Raw observations on corrected population:
- 0006 daily-range/line intersections: 32
- 0007 daily-range/line intersections: 30
- 0006 directionally-consistent reaction candidates: 163
- 0007 directionally-consistent reaction candidates: 178
- Total rows with a reaction candidate: 347

## QA checks passed after correction
- 403-row preliminary population detected as period-leaky and rejected.
- Corrected candidates all fall within 2016–2024.
- Candidate pivot availability exists for all 347 rows.
- Candidate availability is not earlier than candidate timestamp.
- Reaction availability is not earlier than reaction candidate timestamp for matched reactions.
- Candidate keys are deterministic/unique.
- Rule mapping remains 0006 = LOW/UP and 0007 = HIGH/DOWN.
- Evidence status remains CANDIDATE_ONLY.
- No 2025/2026 candidate or reaction is included in the corrected dataset.

## Provenance
Canonical inputs remain:
- PIVOT_SEQUENCE_V2
- TRENDLINE_GEOMETRY_V1
- D1 OHLC / DMI_ADX 2016–2024

Corrected local dataset SHA-256:
`3ca710e97679fdc5025311c145e6d73bd5c1111cb15657c87ed05c6100335167`

## Decision
The earlier 403-row candidate population is NOT a valid 2016–2024 historical QA population and must not be used for scoring, tuning, or confirmation.
The corrected 347-row dataset is the only candidate population eligible for the next QA gate.

No thresholds, touch tolerances, reaction thresholds, or no-break rules were introduced.
2025 remains excluded from tuning/optimization.
