# Murphy 0008 PF-B1 Policy Approval Gate V1

Date: 2026-08-15
Status: OPEN — NO POLICY APPROVED
Scope: MURPHY_0008 / shared PF-B1 decisive-break primitive

## Finding
A comprehensive source/workspace/GitHub search did not identify an already-approved, production-frozen decisive-break contract that can be reused unchanged for MURPHY_0008.

## Source-supported policy families
Murphy Chapter 4 supports two general filter families for significant support/resistance penetration:
1. PRICE_FILTER — Murphy gives a 1–3% range as context-dependent examples; 3% is described particularly for major support/resistance, while shorter-term areas may use a smaller value.
2. TIME_FILTER — two successive closes beyond the level.

The source does not select one fixed project-wide value or one family for MURPHY_0008. The project must not silently choose 1%, 3%, ATR, pips, arbitrary lookback, or hidden tolerance.

## Current decision
PF-B1 remains NOT PRODUCTION FROZEN.
If no policy is explicitly approved, PF-B1 must return NOT_EVALUABLE for decisive-break confirmation.
MURPHY_0008 must not be forced into PASS/FAIL while decisive-break evidence is NOT_EVALUABLE.

## What is already closed
- 0008 source identity: Support → decisive downside break → later rally/retest → broken support becomes resistance.
- PIVOT_SEQUENCE_V2: canonical and availability/no-lookahead controlled.
- Existing PF-B1 architecture: compatible as the shared breakout interface.
- Feature Engineering V1 Higher-TF and V2 were inspected; neither is the authoritative support producer.
- Nison Support/Resistance materials are confirmation/context only and do not define Murphy's 0008 decisive-break operator.

## Remaining approval gate
An explicit governance decision must select:
- policy family: PRICE_FILTER or TIME_FILTER;
- permitted value/condition;
- applicable level context (e.g. major vs shorter-term);
- confirmation timestamp rule;
- availability/no-lookahead rule.

Selection must not use 2025 or historical performance optimization.

## Implementation rule
Until the above approval exists:
- no 0008 production evaluator;
- no backtest-driven threshold selection;
- no new breakout engine;
- status = NOT_EVALUABLE when decisive-break confirmation is required but policy is absent.

## Next gate after approval
1. Freeze PF-B1 contract.
2. Run deterministic unit tests.
3. Run 2016–2024 QA.
4. Run availability/no-lookahead audit.
5. Complete PF-H1 compatibility.
6. Implement 0008 evaluator/adapter.
7. Keep 2025 OOS and excluded from operator selection/tuning.
