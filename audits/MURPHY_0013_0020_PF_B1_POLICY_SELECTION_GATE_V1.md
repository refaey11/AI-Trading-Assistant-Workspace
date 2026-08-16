# Murphy 0013-0020 — PF-B1 Policy Selection Gate V1

Status: GOVERNANCE DECISION — BLOCKED / NO POLICY SELECTED
Date: 2026-08-16

## Question
Can an existing breakout policy be selected for Murphy 0013-0020 without inventing or tuning a new operator?

## Source-backed findings
The project materials identify two Murphy-supported policy families: a price filter and a two-successive-closes time filter. The source does not select one universal value for every market/timeframe, and the project explicitly prohibits silently binding the general 3% or two-day examples to 0013-0020.

The 0013-0020 primitive contract therefore requires an existing approved breakout/filter contract. If none exists, PF-B1 must return NOT_EVALUABLE.

## Compatibility result
No source-backed evidence in the accessible project material establishes an already-approved, production-frozen PF-B1 policy for 0013-0020.

The historical 0008 records contain a later canonical freeze-status conflict, but the preserved PF-B1 governance material still says that the decisive-break operator was not approved/frozen at the relevant source-era snapshot. That conflict is not sufficient authority to transfer a policy to 0013-0020.

## Decision
DO NOT SELECT:
- 3%
- 1%
- two consecutive closes
- ATR threshold
- pip threshold
- arbitrary percentage
- arbitrary lookback
- backtest-optimized threshold

PF-B1 remains `NOT_EVALUABLE` for complete 0013-0020 rule confirmation until an explicit policy is approved under project governance.

## What is already usable
The shared PF-B1 interface, fail-closed behavior, chronology/availability fields, and no-lookahead requirements are usable as architecture. No duplicate breakout engine should be created.

## Next approval gate
A project-authorized policy decision must explicitly specify:
- policy family
- permitted condition/value
- applicable context
- confirmation timestamp rule
- availability/no-lookahead rule
- historical QA protocol using 2016-2024 only for validation as permitted
- 2025 locked OOS

This document does not itself approve a policy or production-freeze PF-B1.
