# Murphy 0021–0023 — Evaluator Result Boundary Test V1

Date: 2026-08-13
Scope: 0021–0023 only
Status: TEST SPECIFICATION — NOT EXECUTED

## Purpose
Validate the lossless EvaluatorResult boundary before any mapping into the canonical Rule Adapter schema.

## Cases

| Case | Input | Required output |
|---|---|---|
| PASS-UP | rule_id=0021, status=PASS, directional_confirmation=UP | exact preservation of all supplied fields |
| FAIL-DOWN | rule_id=0022, status=FAIL, directional_confirmation=DOWN | exact preservation of all supplied fields |
| NOT-EVALUABLE | rule_id=0023, status=NOT_EVALUABLE, directional_confirmation=null | status remains NOT_EVALUABLE; direction remains null/missing |
| Missing direction | any rule/status with no direction | direction remains missing; no inference |
| Source reason | any result with reason | reason preserved exactly |
| Availability timestamp | any result with confirmation_available_timestamp | timestamp preserved exactly |

## Negative invariants
The boundary must fail validation if it:

- changes `rule_id`
- changes `status`
- converts `NOT_EVALUABLE` into another status
- invents a direction
- invents strength
- invents conflict
- recalculates the evaluator result
- introduces a threshold/lookback/tolerance/proxy
- reads 2025 data

## Execution requirement
This file is a test specification only. It does not claim that the tests have run or passed. The next implementation step must execute these cases against the actual boundary implementation and record pass/fail evidence.

## Freeze rule
Boundary tests passing do not grant Production Freeze. Adapter compatibility and the 122,943-row zero-mismatch reconciliation remain mandatory.