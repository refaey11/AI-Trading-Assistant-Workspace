# Murphy 0008 — PF-B1 Governance Decision Gate V1

Status: FROZEN FOR 0008 VALIDATION — NOT PRODUCTION FROZEN

## Governance decision
PF-B1 is frozen for the 0008 validation path:

`TIME_FILTER = two successive completed D1 closes beyond the Support boundary.`

- First completed D1 close beyond Support: candidate only.
- Second successive completed D1 close beyond Support: decisive-break confirmation.
- Confirmation availability: close of the second completed D1 bar.
- Later retest evidence starts strictly after confirmation.

## Source semantics
0008 is Support → decisive downside break → later rally/retest → broken support functions as resistance.

## Critical source/governance separation
This freeze does NOT claim that Murphy wrote "0008 = two days" verbatim. Murphy's broader discussion provides the Two-Day Rule as a breakout confirmation policy for important Support/Resistance contexts. The project is adopting the two-successive-D1-close operator as its explicit operationalization for this 0008 validation path.

## Hard exclusions
- No 3% threshold selection.
- No selection/tuning from backtest performance.
- No ATR/pip/arbitrary percentage/lookback/tolerance invention.
- No 2025 tuning or operator selection.
- No duplicate breakout engine.

## Validation gates now authorized
1. Deterministic PF-B1 tests.
2. Availability/no-lookahead tests.
3. Fresh 2016–2024 replay independent of reference-result artifacts.
4. PF-H1 compatibility/closure without invented tolerance.
5. 0008 evaluator/adapter evidence-only implementation.
6. Role-reversal tests and provenance/evidence backup.
7. Production freeze only after all gates pass.

## Production status
PF-B1 is FROZEN FOR THE 0008 VALIDATION PATH. This is not a production freeze of the broader PF-B1 module or of 0008. 0008 remains NOT PRODUCTION FROZEN until all validation gates pass.

2025 remains strictly OOS and must not be used for policy selection or tuning.
