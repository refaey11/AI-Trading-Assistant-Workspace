# Murphy 51 — Rule Factory Bulk Audit V1

Date: 2026-08-16
Branch: `pilot/rule-factory-v1`

## Purpose

Run one conservative Factory pass over the existing Murphy 51-rule state so the project does not repeat the same manual inventory work rule-by-rule.

This pass does **not** rewrite canonical Murphy semantics, does not reopen frozen rules, and does not invent thresholds/operators.

## Current bulk result

| Classification | Count | Meaning |
|---|---:|---|
| FROZEN / read-only | 12 | Already frozen by project governance; Factory only regression-checks them |
| PARTIAL / NEED SOLUTION | 21 | Existing source/features/contracts are useful, but one or more exact closure pieces remain |
| NOT_EVALUABLE / BLOCKED | 18 | Missing authoritative source/operator/evidence; keep blocked until defensible evidence exists |
| EXECUTABLE | 0 | No non-frozen rule is promoted by this audit without explicit all-gates evidence |
| **Total** | **51** | |

## Frozen set

`0003, 0004, 0006, 0007, 0008, 0021, 0022, 0023, 0025, 0026, 0028, 0029`

These are read-only for the Factory. The continuity backup explicitly records these 12 as frozen/closed and says frozen rules must not be reopened without new contradictory evidence or an approved semantic change.

## Important distinction

`PARTIAL / NEED SOLUTION` does **not** mean "bad". It means the existing work is reusable and the Factory has identified a specific missing closure item.

`NOT_EVALUABLE / BLOCKED` does **not** mean "never possible". It means the current authoritative evidence is insufficient. The next step is source/provenance/operator investigation, not invented numbers.

## Shared solution batches

The next work should be grouped by reusable primitives instead of 21 independent evaluators:

1. **0013–0020 — Pattern primitives**
   - Reuse existing Pivot/Geometry/Volume infrastructure.
   - Shared missing contracts: horizontal-level relationship, convergence/parallelism, flagpole relation, breakout confirmation.
   - Do not invent numeric convergence/slope tolerances; existing source reconciliation explicitly identifies these as open contracts.

2. **0042–0045 — Risk Gate Adapter**
   - Shared Risk Engine integration already has a contract and deterministic adapter tests.
   - Rule-specific operators still need authoritative source recovery.
   - Missing risk evidence must remain `needs_review`; it cannot become PASS by inference.

3. **0033 / 0037 / 0039 / 0040–0041 / 0046 / 0051**
   - Reuse shared context, indicator, risk, and evidence interfaces where compatible.
   - Investigate the smallest missing contract per rule.

4. **0030–0032 / 0034–0036 / 0038 / 0047–0049 / 0050**
   - Remain blocked where required evidence/feature is unavailable or a deterministic project policy is not approved.
   - No proxy substitution for unavailable breadth/TRIN/P&F/etc.

## Factory safety gates

- Canonical meaning is immutable.
- Frozen rules are read-only.
- No invented threshold/operator.
- No 2025 tuning or implementation selection.
- Similarity is evidence only.
- Risk and process gates remain hard gates.
- Existing components are audited and reused before any new implementation.
- A rule is not frozen merely because an evaluator artifact exists.

## Next action

Use the Factory work queue to run the **Problem/Solution Pass** in batches, starting with the shared primitives above. For each problem:

`source/provenance → compatibility audit → existing primitive → smallest missing operator/contract → deterministic tests → 2016–2024 QA → availability/no-lookahead → freeze candidate`

If authoritative evidence cannot close the missing contract, keep `NOT_EVALUABLE`.
