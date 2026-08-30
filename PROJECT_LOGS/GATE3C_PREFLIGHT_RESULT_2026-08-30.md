# Gate 3C Pre-flight Result

Date: 2026-08-30
Scope: Small deterministic pre-flight only; no full backtest run.
Source artifact: gate3c-single-event-result.zip / gate3c_result.json

## Result
PREFLIGHT: PASS

## Verified invariants
- query_as_of: 2020-01-03T06:00:00+00:00 (not 2025)
- future_data_allowed: false
- oos_tuning: false
- brain_v1_unchanged: true
- full_fanin_verified: true
- Similarity/Memory direction generation: false
- Nison direction generation: false
- TIZ direction generation: false
- TIZ status: NOT_EVALUABLE (not fabricated PASS)
- Risk risk_pass: true; authoritative: true; risk gate overridable: false
- Similarity future current_context excluded: true
- Similarity historical rows retained: 36
- Decision was derived as NO_TRADE, not forced

## Important boundary
This PASS is for the pre-flight contract/invariant checks only. It is NOT a Gate 3C execution PASS and does NOT authorize a full 2016-2024 backtest yet.

## Observed event outcome
Decision Brain result: NO_TRADE / REJECTED / confidence 0.0.
Execution plan: NOT_EXECUTABLE because decision_not_approved.

## Next action
Fix the Gate 3C contract so a valid NO_TRADE result is distinguished from an integration failure, without changing Decision Brain V1 logic, Murphy/Nison/TIZ semantics, or Risk rules. Only after the governed single-event E2E contract is proven should the project proceed to Freeze and the one governed 2016-2024 profitability test.
