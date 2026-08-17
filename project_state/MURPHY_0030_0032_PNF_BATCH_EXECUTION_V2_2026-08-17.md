# MURPHY 0030–0032 — P&F Batch Execution V2
Date: 2026-08-17
Status: TECHNICAL QA EVIDENCE COMPLETE / PRODUCTION FREEZE GATE REMAINS

## Scope
Batch execution of the existing shared P&F core for:
- MURPHY_0030 — P&F bullish support
- MURPHY_0031 — P&F long stop reference
- MURPHY_0032 — P&F short stop reference

The 12 already-frozen Murphy rules were not touched.

## Existing implementation reused
- `src/murphy_0030_0032/pnf_3box_reference.py`
- `src/murphy_0030_0032/pnf_3box_log_reference.py`
- Existing `tests/murphy_0030_0032/` suite

The implementation already records the source-bounded construction boundary: X-column High-first continuation, O-column Low-first continuation, 3-box reversal, bullish support reference, and stop references without invented offsets.

## Existing deterministic QA evidence
The prior QA artifact records 7/7 local tests passing, including:
- X High-first
- O Low-first
- 3-box reversal
- bullish support origin
- long/short stop reference direction
- deterministic replay
- prefix snapshot / no-lookahead boundary

## Additional execution performed for this batch
Canonical workspace D1 data used: 2,544 rows covering 2016-01-03 through 2024-12-31.

For calibration-only walk-forward construction checks, the existing project candidate operationalization was used exactly as documented in the box-policy gate: sample standard deviation of log returns over the prior three calendar years. No profitability metric and no 2025 data were used.

Fold construction QA was executed for 2019–2024 because each fold requires three prior calendar years of calibration data.

Results:
- 2019: box_pct 0.625736%; deterministic construction PASS; prefix replay PASS.
- 2020: box_pct 0.483552%; deterministic construction PASS; prefix replay PASS.
- 2021: box_pct 0.551939%; deterministic construction PASS; prefix replay PASS.
- 2022: box_pct 0.537156%; deterministic construction PASS; prefix replay PASS.
- 2023: box_pct 0.643739%; deterministic construction PASS; prefix replay PASS.
- 2024: box_pct 0.588047%; deterministic construction PASS; prefix replay PASS.

## Interpretation
These results establish deterministic historical construction and prefix/no-lookahead behavior for the existing 3-box core under calibration-only fold inputs. The percentages above are diagnostic execution evidence, not Murphy source values.

## Remaining production gate
The production evaluator still requires an explicit governance freeze of the GBPUSD box-size operationalization and bootstrap policy. Murphy does not provide one universal GBPUSD numeric box size, so the project must not silently relabel the operationalization as Murphy/Tower source truth.

No 2025 data was used for tuning, selection, calibration, or optimization.

## Rule status
0030–0032 are not falsely marked Production Frozen by this artifact. They are technically validated to the current execution boundary and remain at the explicit production-governance gate until the box/bootstrapping policy is formally frozen.
