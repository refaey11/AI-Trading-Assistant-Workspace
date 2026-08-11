# Murphy 0027–0029 Test & QA V1

Date: 2026-08-12

## Evidence basis

The preserved project artifacts identify an existing 0027–0029 evaluator/test package. The project handoff states:
- 0027 evaluator intentionally returns NOT_EVALUABLE until the exact trend-vs-ranging regime operator is approved;
- 0028/0029 divergence evaluator/test cases exist;
- the evaluator refuses to invent an ADX threshold or fixed timeframe.

The current GitHub repository search did not expose the underlying evaluator/test files directly, so this QA record does not claim fresh execution of those tests in the current environment.

## Rule-level status

### 0027
Status: **BLOCKED / NOT_EVALUABLE by design**

Reason: exact trend-vs-ranging regime operator is not source-locked. No ADX threshold or fixed timeframe may be invented.

### 0028
Status: **TEST ARTIFACT EXISTS / FRESH EXECUTION NOT VERIFIED HERE**

The preserved project state reports divergence test cases. A fresh run cannot be claimed without retrieving the underlying test package.

### 0029
Status: **TEST ARTIFACT EXISTS / FRESH EXECUTION NOT VERIFIED HERE**

Same limitation as 0028.

## QA decision

Do not mark 0027–0029 Frozen based solely on the preserved status.

- 0027 remains NOT_EVALUABLE until the regime operator is source-locked.
- 0028/0029 remain implementation/test-present but require direct test artifact retrieval and execution before a fresh PASS can be declared.

## Controls

- No invented ADX threshold.
- No invented fixed timeframe.
- No 2025 tuning.
- Reuse existing evaluator/test artifacts; do not rebuild them.

## Next action

Retrieve the actual evaluator/test files from the Workspace/File Library and execute/inspect them directly. Then update this QA record with concrete PASS/FAIL outputs. Continue forward meanwhile.
