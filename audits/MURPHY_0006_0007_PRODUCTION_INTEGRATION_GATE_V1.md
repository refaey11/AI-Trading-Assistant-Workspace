# MURPHY 0006/0007 — PRODUCTION INTEGRATION GATE V1

Date: 2026-08-14
Status: OPEN — explicitly isolated from replay QA

## What is proven
The corrected 0006/0007 operator reproduces 8 + 7 = 15 on a fresh 2016–2024 replay using canonical Pivot V2 and Geometry V1 inputs. Governance has conditionally approved the operationalization.

## What is not yet proven
The current GitHub repository tree contains the 0006/0007 operator and evidence adapter, but the repository evidence does not demonstrate that the 0006/0007 evaluator is wired into the project's external Decision Brain / generic rule-adapter runtime as a production callable path.

## Required integration proof
A production integration artifact must show:
1. the production entry point imports/calls the 0006/0007 evaluator;
2. evaluator outputs map into the project's normalized evidence/gate contract;
3. `PASS`, `FAIL`, and `NOT_EVALUABLE` semantics are preserved without coercion;
4. Murphy direction can inform technical context but does not bypass Nison/Zone/Risk precedence;
5. no similarity result can override the Murphy hard gate;
6. 2025 remains excluded from tuning/selection;
7. an end-to-end smoke test exercises the actual production entry point.

## Freeze rule
Do not create the final freeze manifest until this integration proof exists. Replay success and unit-test success are necessary but not sufficient for Production Frozen status.

## Smallest safe next action
Create a dedicated integration adapter/test that connects the deterministic 0006/0007 evaluator output to the existing generic Decision Brain evidence contract, without changing the evaluator semantics or adding new trading thresholds.
