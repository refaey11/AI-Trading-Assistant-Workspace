# Murphy PF-B1 Policy Compatibility Matrix V1

Status: GOVERNANCE / COMPATIBILITY AUDIT — NOT PRODUCTION FROZEN
Date: 2026-08-15
Branch: audit/murphy-0008-pf-b1-v1

## 1. Purpose

Determine whether Murphy's source-described breakout filters can be bound to one shared production PF-B1 policy for 0008/0009/0010 and the later breakout consumers, without silently selecting a threshold or using historical performance to choose an operator.

## 2. Source boundary

Murphy Chapter 4 establishes the following source semantics:
- Support/resistance role reversal requires a significant penetration.
- Murphy gives 3% as a benchmark particularly for major support/resistance and notes that shorter-term areas may require a smaller value such as 1%.
- Murphy explicitly states that the analyst must decide what constitutes significant penetration.
- Murphy describes the two-day rule as an alternative time filter: two successive closes beyond the level; a one-day violation does not count.
- Murphy states that the 1–3% rule and the two-day rule are also applied to important support/resistance breaks, not only trendlines.

Source reference checked: Murphy, Technical Analysis of the Financial Markets, Chapter 4, Support/Resistance role reversal and trendline-break filter discussion.

## 3. Consumer compatibility

| Consumer | Break meaning | Price-filter family | Two-day family | Single universal binding justified by source? |
|---|---|---|---|---|
| 0008 | downside break of support; later role reversal | Source-compatible in principle; context-sensitive 1–3% | Source-compatible in principle | NO |
| 0009 | upside break of resistance; later role reversal | Source-compatible in principle; context-sensitive 1–3% | Source-compatible in principle | NO |
| 0010 | trendline penetration/break | Explicitly discussed by Murphy | Explicitly discussed by Murphy | NO without project policy |
| 0013–0020 | pattern breakout | Depends on pattern/source context; some rules require confirmed close outside boundary | Potentially compatible where source policy permits | NO |

## 4. Compatibility conclusion

No single fixed project-wide decisive-break operator is source-determined.

The source supports policy families, but does not select a universal percentage or a universal time-filter binding for all markets, timeframes, and rule contexts. Therefore:

- PF-B1 MUST NOT freeze 1% globally.
- PF-B1 MUST NOT freeze 3% globally.
- PF-B1 MUST NOT freeze two successive daily closes globally.
- PF-B1 MUST NOT select among these policies using 2016–2024 replay performance.
- PF-B1 MUST NOT use 2025 for policy selection.

## 5. Governance design required

PF-B1 should be frozen as a policy-injection contract, not as a hidden universal threshold:

```text
PF-B1 INPUT
  boundary
  completed OHLC data
  policy_id / approved policy object
  availability metadata

PF-B1 OUTPUT
  boundary_id
  direction
  raw_break_timestamp
  decisive_confirmation_timestamp
  availability_timestamp
  status = CONFIRMED | NOT_CONFIRMED | NOT_EVALUABLE
```

The approved policy object must state:
- policy family
- exact deterministic condition
- applicable rule/context
- source/provenance reference
- confirmation timestamp semantics
- availability/no-lookahead semantics

If the caller has no approved policy binding, decisive-break status MUST be `NOT_EVALUABLE`.

## 6. 0008 decision

MURPHY_0008 remains evaluator-blocked until a project governance decision binds PF-B1 to an approved policy for the 0008 context.

The correct next gate is therefore NOT backtesting and NOT threshold tuning. The next gate is a governance decision on the policy binding, followed by deterministic tests and fresh 2016–2024 QA.

## 7. Prohibitions

Do not introduce ATR, pips, arbitrary lookbacks, hidden tolerance bands, or a percentage selected by replay optimization.
Do not use 2025 for operator selection or tuning.
Do not duplicate the breakout engine per rule.

## 8. Evidence distinction

The Murphy source supplies qualitative semantics and policy families. Any exact project operator is an operationalization and must be labeled as such; it must not be represented as verbatim Murphy wording.
