# Gate A Remediation Findings — 2026-11-16

## Scope
Read-only analysis of Gate A run 43792615471 and its uploaded artifact. No source CSV, source timestamp, runtime, risk rule, or 2025 OOS data was modified. PR #118 remains Draft.

## Confirmed result
- Governed scope projections passed for Historical Context, Historical Outcome, and Market State.
- H1 and Nison passed the input preflight.
- Gate A remains BLOCKED only on MTF and Murphy input checks.
- This gate is input-shape/window validation only. It did not verify producer formulas, as-of joins, MTF close alignment, Murphy semantic eligibility, TIZ, risk execution, costs, or profitability.

## Governed projections
- Historical Context: 273,387 rows retained for 2016-2024; 30,805 rows from 2025 excluded.
- Historical Outcome: 273,183 rows retained; 30,805 rows from 2025 excluded; 204 additional 2024 rows excluded because the 48-hour outcome horizon was not fully mature before 2025-01-01 UTC.
- Market State: 55,192 rows retained; 6,225 rows from 2025 excluded.
- Source files were not modified; source and output SHA-256 values are recorded in the run artifact.
- 2025 remains locked and was not used for development/tuning/calibration.

## MTF findings
- Annual assembly includes 671,601 rows from 2016-2024 and excludes 2025/2026 files.
- All 671,601 timestamps are naive. The yearly assembler correctly labels the timezone mode NAIVE_UNRESOLVED and does not rewrite timestamps.
- 2,512 blank values are counted in five `*_trend_regime` columns:
  - D1_trend_regime: 1,955
  - H4_trend_regime: 371
  - H1_trend_regime: 107
  - M30_trend_regime: 53
  - M15_trend_regime: 26
- The current input preflight and `mtf_source_contract_gate_v1.py` require all six `*_trend_regime` fields plus `mtf_trend_score` to be numeric.
- The existing `DEV_BACKTEST_RUNNER_V1.py` contains a categorical mapping for values BULL_TREND, BEAR_TREND, TRANSITION, UNKNOWN. This is evidence of a contract mismatch between the current numeric-only MTF gate and a categorical runtime consumer; it is NOT sufficient evidence to change the source contract or recode source values.
- Next required evidence: authoritative MTF producer/schema definition, actual non-empty token distribution for each regime column, meaning of blank values, and timestamp timezone/session convention. Until then, no categorical conversion, zero-fill, imputation, or timezone assignment is permitted.

## Murphy findings
- 32,400 of 87,225 fan-in timestamps are naive; 54,825 are offset-aware.
- Rule-level inspection shows the naive records are associated with 2020-2024 rows carrying MURPHY_0021, MURPHY_0022, MURPHY_0023, MURPHY_0028, and MURPHY_0029.
- The offset-aware records are associated with MURPHY_0025 and MURPHY_0026, including 2016-2024.
- The archive manifest identifies separate producer artifacts for the historical evaluator outputs and Four-Week Lookback replay, but its creation_utc field does not establish the timezone semantics of each event timestamp.
- Do not append +00:00 to naive rows. Obtain source evaluator timestamp contract or producer code and prove whether timestamps are UTC, broker-local, exchange-local, or availability-time values before any normalization.

## Additional integration blockers (not cleared by Gate A)
- Existing DEV_BACKTEST_RUNNER_V1.py currently uses pd.to_datetime(..., utc=True) on inputs, which would silently interpret naive timestamps as UTC if run before timezone provenance is resolved. Do not run it on the current MTF/Murphy sources.
- The runner's build_row() consumes fields named trend and h4_trend and maps categories, while the assembled MTF schema exposes M5/M15/M30/H1/H4/D1_trend_regime and mtf_trend_score. This is a concrete field-contract mismatch requiring a compatibility audit before any replay.
- The runner currently sets several validation manifest claims to literal true and is diagnostic-only; those flags are not evidence of successful as-of/MTF/memory validation.
- Risk/SLTP contract reconciliation remains separately required.

## Decision
Keep Gate A BLOCKED. Do not merge PR #118, do not run the full backtest, and do not enable live trading. Next work is producer/schema recovery and a field-by-field contract reconciliation, followed by tests that prove semantics without mutating source data.
