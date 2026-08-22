# Murphy 0047–0049 — Reconciliation Record

Date: 2026-08-22
Status: RECONCILED — HISTORICAL CLOSURE EVIDENCE

## Discrepancy resolved
The CLOSED package contained one metadata inconsistency for Rule 0047:
- `CLOSURE.md` reported 24 occurrences.
- `CLOSURE_STATUS.json` reported 25 occurrences.
- `RULE_0047_FINAL_OCCURRENCES.csv` contains 25 rows.
- `FINAL_REPLAY_0047_0049_TRADING_DAYS.csv` contains 25 rows where `rule_0047=True`.

The 25-row CSV/replay evidence agrees with the 25 occurrence count in `CLOSURE_STATUS.json` and is therefore the authoritative reconciled count. The `24` in `CLOSURE.md` is a stale metadata typo and must not be used for runtime mapping.

## Reconciled final counts
- 0047: 25 occurrences
- 0048: 186 occurrences
- 0049: 122 occurrences

## Coverage / controls
- Requested period: 2016-01-04 through 2020-02-10
- Final replay trading-day rows: 1,033
- NYSE closure rows excluded: 6
- 2025 used: false
- Synthetic rows: false
- Proxy substitution: false
- New thresholds: false
- New timeframes: false

## Ingestion quality
The accompanying ingestion quality report contains 1,039 source rows, zero duplicate dates, zero missing required fields, zero negative required fields, and two zero-denominator/all-zero rows. These are retained as source-quality facts; they are not converted into fabricated evidence.

## Runtime boundary
This reconciliation does NOT by itself promote 0047–0049 to Runtime. It only resolves the historical closure-count discrepancy. Runtime promotion still requires the compatibility audit, executable evaluator, deterministic tests, and unified runtime entry-point verification.

## Provenance
Source packages reviewed:
- MURPHY_0047_0049_CLOSED_FINAL_V1
- MURPHY_0047_0049_UNICORN_2016_2020_INGESTION_V1
