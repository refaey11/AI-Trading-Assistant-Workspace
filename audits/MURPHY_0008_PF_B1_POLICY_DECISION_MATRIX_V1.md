# Murphy 0008 — PF-B1 Policy Decision Matrix V1

Status: GOVERNANCE REVIEW / NOT PRODUCTION FROZEN
Date: 2026-08-15
Branch: audit/murphy-0008-pf-b1-v1

## Objective
Determine whether the Murphy source and existing project contracts authorize a deterministic PF-B1 decisive-break policy for Rule 0008 without importing an unrelated context or tuning on outcomes.

## Source-derived candidates
| Candidate | Source presence | Context in supplied project evidence | Direct authorization for generic 0008 PF-B1 |
|---|---|---|---|
| Price filter, 1–3% family | Yes | Murphy break-filter discussion / contextual examples | No fixed 0008 value selected by source |
| Two successive closes | Yes | Murphy time-filter discussion / contextual examples | No explicit 0008 binding selected by source |
| Decisive/significant downside penetration | Yes | Support/resistance role-reversal semantics | Semantic requirement, not a deterministic numeric operator |
| ATR/pips/arbitrary %/lookback/tolerance | No | Not source-locked for 0008 | Prohibited |

## Existing project contracts
The current PF-B1 implementation specification is a proposal, not a production-frozen contract. It requires reuse of an existing approved breakout/filter contract when one exists; otherwise decisive confirmation is NOT_EVALUABLE.

The project also explicitly prohibits silently converting Murphy's general price-filter/two-day examples into a mandatory 0008 threshold.

## 0008-specific decision
No single decisive-break policy is authorized for 0008 by the currently reconciled source/project materials.

Therefore:
- Do not select 1%.
- Do not select 3%.
- Do not select two consecutive closes.
- Do not select by historical performance.
- Do not use 2025.

## What can be operationalized now
1. Consume an available support boundary from the approved upstream path.
2. Detect and timestamp an observable raw downside boundary crossing/penetration event using completed data.
3. Preserve the raw event separately from decisive confirmation.
4. If no approved decisive-break policy is supplied, return NOT_EVALUABLE for decisive confirmation.
5. Continue to treat the later rally/retest and role reversal as separate 0008 evidence stages.

## Why we do not collapse the stages
Calling the later retest itself the breakout confirmation would mix two separate semantic requirements of 0008: (a) decisive downside break and (b) later return/role reversal. The project architecture explicitly places PF-B1 before the later rally/retest stage.

## Reuse conclusion
No existing production-frozen PF-B1 contract has been identified. The existing PF-B1 proposal is reusable as the interface/governance boundary, but it cannot yet be frozen as the decisive-break operator.

## Next gate
An explicit project governance decision must authorize a source-faithful decisive-break policy for 0008. That decision must be made independently of 2025 and must be validated with deterministic tests, availability/no-lookahead checks, and 2016–2024 QA before production freeze.

## Final status
PF-B1 interface: COMPATIBLE
Raw-break event: OPERATIONALIZABLE
Decisive-break confirmation: OPEN GOVERNANCE GAP
0008 evaluator: BLOCKED FROM PRODUCTION IMPLEMENTATION UNTIL GAP IS CLOSED
