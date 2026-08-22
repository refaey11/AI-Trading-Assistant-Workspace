# Timeframe Full Six-TF As-Of Alignment — Final Evidence

Date: 2026-08-22

## Scope
Governed timeframe chain:
M5 -> M15 -> M30 -> H1 -> H4 -> D1

Development/validation window: 2020-01-01 through 2024-12-31.
2025 excluded from the test set.

## Source counts
- M5: 373,465 rows
- M15: 124,764 rows
- M30: 62,513 rows
- H1: 31,385 rows
- H4: 8,039 rows
- D1: 1,554 rows

## As-of validation
Each lower timeframe observation was mapped only to the latest available higher-timeframe observation whose timestamp was not in the future relative to the lower-timeframe observation.

Results:
- M5 -> M15: PASS; 0 future mappings; 0 missing mappings
- M15 -> M30: PASS; 0 future mappings; 0 missing mappings
- M30 -> H1: PASS; 0 future mappings; 0 missing mappings
- H1 -> H4: PASS; 0 future mappings; 0 missing mappings
- H4 -> D1: PASS; 0 future mappings; 0 missing mappings

All six timestamp series were monotonic and duplicate-free in the tested rows, with expected cadence for the timeframe labels.

## Conclusion
Six-timeframe source/alignment/no-lookahead evidence is CLOSED for the 2020–2024 test window.

This does NOT by itself prove:
- Dynamic Timeframe Selection runtime PASS
- Time/Session Context runtime PASS
- full Decision Brain E2E PASS

Those remain separate gates.

## Governance
No timeframe selection rule, session boundary, threshold, or trading direction was invented or tuned from 2025.