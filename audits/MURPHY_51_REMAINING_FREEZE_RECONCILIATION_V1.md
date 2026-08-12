# Murphy 51 Remaining Freeze Reconciliation V1

Date: 2026-08-12

## Scope
One-pass reconciliation of the remaining Murphy rules after the known evaluator-backed candidates. This is a freeze-control artifact, not a claim that every rule is production frozen.

## Source-grounded rule states

| Rules | Current state | Freeze blocker / action |
|---|---|---|
| 0001 | PARTIAL | definite reversal operator not frozen |
| 0002 | VERIFIED NOT_EVALUABLE | exact entry/exit timing operator absent |
| 0003–0004 | V2 exists / NOT FROZEN | historical provenance remains unresolved |
| 0005 | NOT_EVALUABLE | source row/operator not currently retrievable |
| 0006–0007 | MAPPING COMPATIBLE / NOT YET EVALUABLE | source-lock + third successful reaction contract absent |
| 0008–0009 | PARTIAL | decisive-break operator not closed |
| 0010 | NOT_EVALUABLE | filter selection contract not closed |
| 0011 | PARTIAL | operator/evaluator gap |
| 0012 | NOT_EVALUABLE | operator/evaluator gap |
| 0013 | NOT_EVALUABLE | pattern/operator evaluator gap |
| 0014 | REQUIRES_DERIVED_FEATURE | derived feature missing |
| 0015 | REQUIRES_DERIVED_FEATURE | derived feature missing |
| 0016 | NOT_YET_EVALUABLE / derived feature | derived feature missing |
| 0017 | REQUIRES_DERIVED_FEATURE | derived feature missing |
| 0018 | REQUIRES_DERIVED_FEATURE | derived feature missing |
| 0019 | REQUIRES_DERIVED_FEATURE | derived feature missing |
| 0020 | NOT_YET_EVALUABLE | operator/evaluator gap |
| 0021–0023 | FREEZE CANDIDATE | evaluator/tests/historical artifacts exist; official freeze manifest gate remains |
| 0024 | PARTIAL | missing closure evidence |
| 0025 | NOT_YET_EVALUABLE | operator/evaluator gap |
| 0026 | NOT_YET_EVALUABLE | operator/evaluator gap |
| 0027 | BLOCKED / NOT_EVALUABLE | exact trend-vs-range regime operator missing |
| 0028–0029 | FREEZE CANDIDATE | evaluator/tests exist; official freeze manifest gate remains |
| 0030 | NOT_EVALUABLE | operator/evaluator gap |
| 0031 | NOT_EVALUABLE | operator/evaluator gap |
| 0032 | NOT_EVALUABLE | operator/evaluator gap |
| 0033 | PARTIAL | missing closure evidence |
| 0034 | NOT_EVALUABLE | operator/evaluator gap |
| 0035 | NOT_EVALUABLE | operator/evaluator gap |
| 0036 | NOT_EVALUABLE | operator/evaluator gap |
| 0037 | PARTIAL | missing closure evidence |
| 0038 | NOT_EVALUABLE | operator/evaluator gap |
| 0039 | PARTIAL | missing closure evidence |
| 0040 | NOT_EVALUABLE | operator/evaluator gap |
| 0041 | NOT_YET_EVALUABLE | operator/evaluator gap |
| 0042 | PARTIAL | missing closure evidence |
| 0043 | PARTIAL | missing closure evidence |
| 0044 | PARTIAL | missing closure evidence |
| 0045 | PARTIAL | missing closure evidence |
| 0046 | NOT_EVALUABLE / PARTIAL | source/operator/evidence incomplete |
| 0047 | NOT_EVALUABLE | operator/evaluator gap |
| 0048 | NOT_EVALUABLE | operator/evaluator gap |
| 0049 | NOT_EVALUABLE | operator/evaluator gap |
| 0050 | NOT_EVALUABLE / PARTIAL | combined evidence contract incomplete |
| 0051 | PARTIAL | missing closure evidence |

## Verified candidate evidence

0021–0023 have an implemented/unit-tested evaluator, preserved PASS test cases, historical evaluation artifacts for 2020–2024, Dynamic MTF support, and `2025_used=false`.

0028–0029 have an implemented evaluator and preserved PASS cases for correct divergence, wrong divergence, and missing evidence, with availability/no-lookahead handling and `2025_used=false`.

These are candidates for the official freeze manifest, not automatically frozen.

## Explicit controls

- 0003–0004 are not altered to force old historical counts.
- 0006–0007 do not receive invented touch/reaction thresholds.
- 0027 does not receive an invented trend/range operator.
- 0050 does not receive an invented combined-evidence contract.
- No new evaluator is built where the project already has a compatible component.
- 2025 is OOS only and is not used for tuning, selection, or fitting.
- Decision Brain V1/V1.1, Dynamic MTF, Pivot Sequence V2, and Trendline Geometry V1 are preserved.

## Final one-pass result

All 51 Murphy rule IDs now have an explicit controlled closure state in this manifest. The Murphy set is **not yet 51/51 FROZEN** because the Source of Truth does not support that claim. The next action is to close the small set of source/evaluator gates where evidence exists, then produce the official freeze manifest only when each required gate passes.
