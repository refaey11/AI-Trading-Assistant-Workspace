# Murphy 0008 — PF-B1 Governance Approval Package V1

Status: GOVERNANCE PACKAGE / NOT FROZEN
Date: 2026-08-15

## Decision requested
Approve or reject the project operational policy for PF-B1 used by Murphy 0008. No production evaluator change is authorized by this document alone.

## Source semantics (Murphy)
0008 requires support, a decisive downside penetration/break, a later rally/retest, and role reversal where the broken support acts as resistance. Murphy discusses price and time breakout filters, including a two-successive-closes time filter and a 1–3% price-filter range in the broader discussion. The source does not select one fixed project-wide policy for 0008.

## Project constraints
- Do not infer the 0008 operator from historical performance.
- Do not use 2025 for selection or tuning.
- Do not add ATR, pips, arbitrary percentages, lookbacks, or tolerance bands.
- Reuse PF-H1/PF-B1; do not create a bespoke breakout engine.
- If policy is not approved, PF-B1 returns NOT_EVALUABLE and 0008 must not be forced to PASS/FAIL.

## Candidate policy under governance review
TIME_FILTER
- condition: two successive completed D1 closes beyond the support boundary in the downside direction
- first close: candidate break only
- second successive completed close: decisive confirmation
- confirmation timestamp: close of second completed D1 bar
- availability: confirmation becomes available only after that bar is complete
- later retest evidence begins strictly after confirmation

## Why this is a candidate, not a frozen rule
The two-day concept is source-supported as a filter family, but selecting it for 0008 is a project governance decision. This package does not claim that Murphy explicitly states “0008 = two D1 closes.”

## Evidence already completed in this audit branch
- PF-B1 no-lookahead chronology defined.
- Edge cases defined: wick-only breach, single-close breach, second bar unavailable, late support availability, and same-bar retest.
- A comparative experiment was recorded for 2016–2024, but historical performance must not be used to choose the policy.

## Approval gates after policy approval
1. Freeze PF-B1 contract and provenance.
2. Implement deterministic PF-B1 unit tests.
3. Re-audit PF-H1 compatibility; no horizontal tolerance may be invented.
4. Implement 0008 only from the shared primitives.
5. Run fresh 2016–2024 QA independently of reference-result artifacts.
6. Run availability/no-lookahead audit.
7. Create 0008 problem/solution/evidence backup.
8. Keep 2025 OOS and untouched.
9. Freeze only after all gates pass.

## Current decision
PENDING GOVERNANCE APPROVAL.
