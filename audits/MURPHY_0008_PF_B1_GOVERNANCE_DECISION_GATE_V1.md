# Murphy 0008 — PF-B1 Governance Decision Gate V1

Status: GOVERNANCE DECISION REQUIRED — NOT FROZEN

## Source semantics
0008 is Support → decisive downside break → later rally/retest → broken support functions as resistance.

## Existing project evidence
- No already-approved production-frozen decisive-break contract was found in the current Workspace/GitHub audit record.
- PF-B1 remains a shared proposal intended for 0008/0009/0010 and other breakout-style rules.
- The project explicitly requires NOT_EVALUABLE when decisive-break evidence is not deterministically established.

## Candidate operationalization under review
TIME_FILTER: two successive completed D1 closes beyond the support boundary.
- First completed D1 close beyond support: candidate only.
- Second successive completed D1 close beyond support: decisive-break confirmation.
- Confirmation availability is the close of the second completed D1 bar.
- Later retest evidence starts strictly after confirmation.

## Critical governance separation
This candidate is NOT claimed to be verbatim wording of Murphy Rule 0008. Murphy's broader discussion includes time/price breakout filters, including a two-day example, but the project handoff explicitly prohibits silently converting that example into the hard 0008 threshold.

The candidate therefore requires explicit project Governance approval before PF-B1 can be frozen or consumed by a production 0008 evaluator.

## Prohibited shortcuts
- No 3% threshold selection.
- No 2-day selection based on backtest performance.
- No ATR/pip/arbitrary percentage/lookback/tolerance invention.
- No 2025 tuning or operator selection.
- No duplicate breakout engine.

## Validation gate after approval
1. Deterministic PF-B1 tests.
2. Availability/no-lookahead tests.
3. Fresh 2016–2024 replay independent of reference-result artifacts.
4. PF-H1 compatibility/closure.
5. 0008 evaluator/adapter evidence-only implementation.
6. Role-reversal tests and provenance/evidence backup.
7. Freeze only after all gates pass.

## Current decision
PENDING GOVERNANCE APPROVAL.
Until approval, PF-B1 and 0008 remain NOT FROZEN and production evaluation must not be claimed.
