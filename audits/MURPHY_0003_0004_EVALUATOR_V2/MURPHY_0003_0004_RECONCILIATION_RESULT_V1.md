# Murphy 0003–0004 Reconciliation Result V1

## Run

Workflow: `Murphy 0003-0004 Reconciliation #1`
Commit: `750f121d8772a3d63f7e024eb9b93ed7868e84cf`
Result: SUCCESS

## Root cause found

The existing project contains a semantic mismatch:

1. `MURPHY_0001_TO_0005_EXACT_MAPPING_V1.csv` specifies:
   - MURPHY_0003 = successive reaction peaks higher AND successive reaction troughs higher.
   - MURPHY_0004 = successive reaction peaks lower AND successive reaction troughs lower.
   - Both are marked `REQUIRES_DERIVED_FEATURE`.
2. `MURPHY_EVALUATORS_V1/MURPHY_0003_0004_EVALUATOR_CONTRACT_V1.json` and its Python implementation evaluate only the LOW/trough sequence.
3. Existing unit tests cover trough-only behavior and therefore do not detect the missing peak condition.

Therefore the earlier V1 evaluator is **not semantically equivalent to the exact mapping**.

## Canonical input

`PIVOT_SEQUENCE_V2_OUTPUT/PIVOT_SEQUENCE_CONTRACT_V2.json` defines confirmed pivot events, their prices, chronological ordering, and availability after two confirming bars. The V2 QA artifact reports `no_2025=True` for the available yearly pivot files.

## Reconciliation method used for this audit

For each confirmed LOW evaluation event within 2016–2024:

- compare current LOW against the immediately prior confirmed LOW available in the sequence;
- obtain the latest two confirmed HIGH pivots available by the same evaluation availability timestamp;
- compare current HIGH against prior HIGH;
- exact 0003 requires both comparisons to be higher;
- exact 0004 requires both comparisons to be lower.

This method is an **audit alignment**, not yet a production contract freeze. No thresholds or pivot definitions were changed.

## Exact counts from canonical Pivot Sequence V2

| Timeframe | Evaluated events | 0003 exact PASS | 0004 exact PASS |
|---|---:|---:|---:|
| D1 | 341 | 101 | 118 |
| H1 | 7,728 | 2,257 | 2,056 |
| H4 | 1,922 | 583 | 592 |
| M15 | 29,388 | 8,373 | 8,362 |
| M30 | 14,928 | 4,304 | 4,156 |
| M5 | 84,266 | 24,447 | 23,940 |

## Important conclusion

The previous historical counts recorded for the V1 trough-only evaluator must **not** be reused as exact 0003/0004 validation results.

The new exact counts above are audit results derived from the canonical V2 pivot sequence under the alignment described above. They should not be marked production-final until the alignment contract is explicitly accepted by the existing architecture and the evaluator is updated accordingly.

## 2025 policy

No 2025 data is used in the counts above. The discovery scan did find the literal year `2025` in several generic contract/QA files; that is metadata/content references, not inclusion of 2025 rows in the evaluation set. The Pivot Sequence V2 QA marks the historical yearly artifacts used here as `no_2025=True`.

## Status

**MURPHY_0003–0004: NOT FROZEN / RECONCILIATION REQUIRED**

Next gate: formalize the availability-time alignment contract, update the evaluator and tests to enforce both peak and trough conditions, then rerun 2016–2024 historical evaluation. Do not proceed to 0006–0007 until this gate is closed.
