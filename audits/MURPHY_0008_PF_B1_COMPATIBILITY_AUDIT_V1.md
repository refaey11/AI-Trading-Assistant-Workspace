# Murphy 0008 — PF-B1 Breakout Contract Compatibility Audit V1

Date: 2026-08-15
Status: SOURCE SEMANTICS RESOLVED / PF-B1 GOVERNANCE OPEN / EVALUATOR NOT STARTED

## 1. Rule identity

0008 is the Murphy support-to-resistance role-reversal rule:
- existing support
- decisive downside break
- later rally/retest toward the broken support
- broken support acts as resistance
- bearish role-reversal evidence

The project Ready Batch records 0008 as SOURCE SEMANTICS RESOLVED / EVALUATOR PENDING and explicitly says to reuse the existing breakout/filter contract rather than invent a new threshold.

## 2. Murphy source audit

The supplied Murphy Chapter 4 archive was inspected directly. The source material distinguishes support/resistance and role reversal, and describes support becoming resistance after a decisive downside break. The same chapter also discusses breakout filters, including a price-filter example and a two-consecutive-daily-close time filter in the trendline/breakout context.

Important source boundary: the inspected material does not provide a single project-specific deterministic software predicate defining exactly when the 0008 break must be classified as decisive. Therefore the source does not authorize silently selecting 3%, 2-day, ATR, pips, or another threshold as the 0008 production operator.

## 3. Workspace compatibility findings

Existing project primitives/contracts found:

### PF-H1 — Horizontal Level
Purpose: represent a support/resistance boundary.
Outputs include level_id, level_price, role, availability_timestamp, and status.
The proposal explicitly forbids inventing a numeric horizontal tolerance and returns NOT_EVALUABLE until an approved deterministic level contract exists.

### PF-B1 — Breakout Confirmation
Purpose: normalize breakout evidence for pattern rules.
Outputs include boundary_id, direction, breakout_timestamp, confirmation_timestamp, availability_timestamp, and status.
The contract requires reuse of an approved project breakout/filter definition and states that Murphy's general 3% or 2-day examples must not be silently converted into mandatory project rules.

0008/0009/0010 are explicitly listed as compatible consumers of PF-B1.

## 4. GitHub search result

GitHub repository/history was searched for 0008, decisive break, breakout confirmation, and related PR/commit terms. No separate production-frozen 0008 decisive-break evaluator or authoritative PF-B1 implementation was found through the accessible GitHub search surface.

Therefore the existing PF-B1 remains a governance/deterministic-contract proposal, not a production-frozen operator.

## 5. Compatibility decision

DO NOT implement 0008 evaluator yet.

The correct dependency chain is:

PF-H1 / approved support level
→ PF-B1 / approved decisive downside break
→ later rally/retest toward broken support
→ role reversal evidence
→ 0008 Murphy adapter

The project must not bypass PF-B1 by inventing a direct close-below-support rule solely to obtain historical matches.

## 6. Missing contract

The only material blocker identified for the 0008 evaluator is the project-approved deterministic definition of a decisive break. The contract must specify, at minimum:
- which completed price evidence is authoritative;
- how break direction is established;
- when the breakout becomes knowable (availability timestamp);
- what status is returned when evidence is insufficient or ambiguous.

No numerical threshold is selected by this audit.

## 7. Required next action

1. Complete governance/source reconciliation for PF-B1.
2. Reuse PF-B1 once an approved deterministic breakout definition exists.
3. Validate PF-H1 support-level representation for 0008 without inventing tolerance.
4. Implement only the smallest missing 0008 role-reversal evaluator.
5. Add deterministic tests and availability/no-lookahead tests.
6. Run 2016–2024 historical QA.
7. Keep 2025 locked OOS and never use it for operator selection/tuning.
8. Create a 0008 problem/solution/evidence backup before freeze.

## 8. Evidence references

- `MURPHY_READY_BATCH_0008_0014_V1.txt`
- `MURPHY_0013_0020_PRIMITIVE_CLOSURE_PROPOSAL_V1.md`
- `MURPHY_PATTERN_PRIMITIVES_IMPLEMENTATION_SPEC_V1.md`
- `MURPHY_0013_0020_SOURCE_RECONCILIATION_V2.md`
- Supplied Murphy Chapter 4 archive: `01_John_Murphy_Technical_Analysis(6).zip`

## 9. Decision

0008 is NOT blocked by source identity or architecture.
0008 IS blocked by the missing approved PF-B1 decisive-break operator.

No evaluator code or historical tuning should start until that contract is closed.
