# Murphy 0030 P&F Box Policy Decision Gate V1

Status: OPEN / PRE-FREEZE
Date: 2026-08-15

## Decision
Do not freeze the candidate box policy yet.

## Required evidence before freeze
1. Source-faithful Murphy semantics remain unchanged.
2. Candidate operationalization is deterministic and independently reproducible.
3. Calibration-only computation is demonstrated for every intended walk-forward fold.
4. No OOS data, profitability, or performance metric is used to choose or alter the formula.
5. P&F engine behavior is deterministic under the candidate percentage box policy.
6. High/Low intrabar ordering ambiguity is explicitly handled without an unapproved assumption.
7. Prefix replay and no-lookahead tests pass.
8. Governance explicitly approves the operationalization as project-defined, not Murphy/Tower source truth.

## Current candidate
box_pct = 100 * sample_std(log(C_t / C_{t-1})) using the prior three calendar years available inside calibration.

Current diagnostic values are informational only and are not frozen parameters.

## Decision outcomes
- PASS: freeze the operationalization and proceed to 0030 evaluator.
- FAIL: reject candidate and keep 0030 NOT_EVALUABLE until a compliant construction is available.
- SOURCE-SUPERSEDED: replace candidate only if an authoritative reproducible Tower formula is recovered.

## Prohibited shortcuts
- Selecting box size by historical profitability.
- Testing many box formulas and choosing the winner.
- Treating the candidate as Murphy/Tower formula.
- Using 2025 for tuning.
- Assuming High-before-Low or Low-before-High on D1 without approved evidence.
