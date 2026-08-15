# Murphy 0030–0032 Compatibility Audit V2

Date: 2026-08-16
Status: BLOCKED — evaluator semantics require correction before historical QA

## Authoritative project registry findings

The project `MASTER_TRADING_RULES_V2.json` currently classifies all three rules as `INCOMPLETE_NEEDS_RULE_DEFINITION` and `UNTESTED`.

- MURPHY_0030: P&F bullish support; required conditions are X/O structure plus use of the bullish support trendline as a structural reference. It has no entry trigger and no confirmation.
- MURPHY_0031: P&F long stop placement; in a P&F uptrend, stop is below the previous O column.
- MURPHY_0032: P&F short stop placement; in a P&F downtrend, stop is above the previous X column.

## Compatibility issue found

The current evaluator labels MURPHY_0030 as a `PNF_BULLISH_SUPPORT_REFERENCE` and returns the base/bottom of the lowest O column as `reference_price`.

That is only a partial representation of the rule. The authoritative Chapter 11 project note defines the object as a **45-degree bullish support trendline drawn from the base of the lowest O column**, not merely a static horizontal support price.

Therefore:
- the lowest-O origin can be retained as evidence;
- the evaluator must not imply that the origin itself is the completed trendline;
- no entry/direction signal may be generated from 0030;
- a future trendline projection must be explicitly modeled only if its source contract is locked.

## 0031 / 0032

The stop references are compatible with the registry wording:
- 0031 → below previous O column in an uptrend.
- 0032 → above previous X column in a downtrend.

However, these are risk-management references, not entry signals. They must remain risk evidence and must not be promoted into directional Decision Brain evidence by themselves.

## Box/bootstrap boundary

The registry does not define the exact software bootstrap or Kenneth Tower conversion formula. Therefore the current project Box Policy and bootstrap remain operationalization proposals. They cannot be presented as verbatim Murphy rules.

## Required correction before historical replay

1. Change 0030 evidence schema to distinguish `support_origin` from `trendline`.
2. Mark 0030 as structural/reference-only, with no directional trigger.
3. Mark 0031/0032 as risk-only references.
4. Keep box-size and bootstrap assumptions outside the Murphy source claim.
5. Add tests proving no rule can emit an entry trigger.
6. Then run the canonical 2019–2024 historical evaluator.

## Governance

Current status remains `NOT_EVALUABLE / INCOMPLETE_NEEDS_RULE_DEFINITION`.
No merge or production freeze is permitted from this audit.
