# Frozen Regression Harness V1

Status: PILOT / READ-ONLY BASELINE
Branch: `pilot/frozen-regression-v1`

## Purpose
Protect the canonical Murphy Frozen baseline while validating the Rule Factory.

## Canonical baseline
The project reconciliation commit `256cfd2928e033670c7ec26a761db45d34df33aa` records 12 Murphy rules as Frozen. The harness treats that reconciliation as the status baseline; it does not redefine individual rule semantics.

## Safety rule
No Frozen rule is edited by this harness. The harness is comparison-only.

## Required comparison
For each canonical Frozen rule, once its authoritative contract/evaluator artifact is resolved:

1. Load the original Frozen contract/evaluator.
2. Run the original evaluator on the same context.
3. Run the Rule Factory adapter on the same context.
4. Compare status and canonical evidence exactly.
5. Compare availability/chronology metadata.
6. Reject any semantic change.

## Promotion invariant
A Frozen baseline must remain `FROZEN`. It must never be downgraded or reinterpreted by the Factory.

## Important limitation
The current GitHub search surface did not return all 12 individual Frozen evaluator artifacts by rule ID. Therefore this commit establishes the harness/governance boundary but does **not** claim a completed 12-rule execution. No synthetic evaluator or invented rule contract is permitted merely to make the test pass.

## Pass criterion
`Original Output == Factory Output` for every resolved Frozen rule, with no canonical-semantic drift.

## Fail criterion
Any mismatch, missing authoritative artifact, or non-deterministic output blocks Factory promotion.

## 2025 rule
2025 remains excluded from tuning/selection.
