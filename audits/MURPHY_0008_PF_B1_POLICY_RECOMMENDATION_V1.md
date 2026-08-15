# Murphy 0008 — PF-B1 Policy Recommendation V1

Date: 2026-08-15
Status: GOVERNANCE RECOMMENDATION — NOT FROZEN
Branch: audit/murphy-0008-pf-b1-v1

## Purpose
Close the 0008 decisive-break governance gap without creating a bespoke breakout engine, changing source semantics, or tuning against historical outcomes.

## Evidence recovered
- Rule 0008 semantic identity: support -> decisive downside break -> later rally/retest -> former support acts as resistance.
- Existing upstream feature: `break_structure_down`.
- Existing shared architecture: PF-H1 horizontal level + PF-B1 breakout confirmation.
- Project Ready Batch explicitly requires reuse of the existing breakout/filter contract and forbids a new threshold.
- Current workspace does not expose a production-frozen 0008-specific decisive-break operator.
- Murphy source discusses significant penetration and describes price/time filters; the source does not select a project-specific 0008 operator.

## Recommendation
Use a TIME_FILTER policy candidate based on two successive completed D1 closes beyond the relevant support boundary.

This is a PROJECT GOVERNANCE RECOMMENDATION, not a claim that Murphy's text literally defines Rule 0008 as a two-day rule.

## Proposed deterministic behavior
For a valid support boundary:
1. `break_structure_down` identifies a downside break candidate.
2. Require the first completed D1 close below the support boundary.
3. Require the immediately following completed D1 close to also be below the same boundary.
4. Only after the second close is complete may PF-B1 return `CONFIRMED`.
5. Confirmation availability timestamp equals the close/availability timestamp of the second completed D1 bar.
6. If the second required close is unavailable or the evidence is ambiguous, return `NOT_EVALUABLE` rather than infer a result.

## Important constraints
- No 3% threshold.
- No 1% threshold.
- No ATR filter.
- No pip tolerance.
- No hidden lookback.
- No 2025 tuning or operator selection.
- No new bespoke breakout engine.
- Reuse `break_structure_down` as the upstream candidate signal.

## Why this candidate is preferred
- Deterministic after approval.
- Avoids choosing an arbitrary percentage value.
- Fits existing D1 completed-bar and availability infrastructure.
- Provides a clean no-lookahead boundary.
- Can be shared through PF-B1 rather than hard-coded into 0008.

## Required approval gate
This document does NOT freeze PF-B1. Before production use, Governance must explicitly approve:
- `policy_family = TIME_FILTER`
- `timeframe = D1`
- `condition = two successive completed closes beyond the support boundary`

If Governance does not approve this policy, PF-B1 remains `NOT_EVALUABLE` and no historical tuning may be used to choose an alternative.

## Post-approval sequence
1. Bind PF-B1 to the approved policy.
2. Unit-test confirmation and availability/no-lookahead behavior.
3. Audit PF-H1 support representation without inventing horizontal tolerance.
4. Implement the smallest 0008 role-reversal evaluator using the shared primitives.
5. Run 2016–2024 historical QA.
6. Perform leakage/provenance audit.
7. Keep 2025 locked OOS.
8. Freeze only after all required gates pass.
