# CURRENT STATE INDEX — 2026-08-22

## Purpose
Single entry point for the live project state. When multiple versions exist, read this index first.

## Current operational source of truth
1. This index
2. `AUDITS/MURPHY_FINAL_COMPATIBILITY_AUDIT_2026-08-22.md`
3. `AUDITS/MURPHY_35_RUNTIME_MATRIX_V2_2026-08-22.md`
4. `AUDITS/MURPHY_35_RUNTIME_INVENTORY_2026-08-22.md`
5. `AUDITS/MURPHY_RUNTIME_BATCH_EXECUTION_STATUS_V1.md`
6. Rule-specific newest final/approval record
7. Canonical/frozen source artifacts
8. Historical audits and recovery files

## Murphy active scope
**35 Frozen/Closed rules**

## Verified Runtime count
**22 / 35**

## Verified Runtime rules
0003, 0004, 0018, 0019, 0021, 0022, 0023, 0028, 0029, 0034, 0035, 0036, 0037, 0038, 0039, 0040, 0041, 0042, 0043, 0044, 0045, 0050.

## Frozen / Runtime NOT PROVEN
0006, 0007, 0008, 0025, 0026, 0030, 0031, 0032, 0033, 0047, 0048, 0049, 0051.

## Important correction
An earlier checkpoint recorded **35/35 Runtime Implemented**. The final compatibility audit retracts that runtime claim because the canonical matrix still supports only **22/35 verified Runtime**. Frozen/Closed does not imply Runtime Implemented.

## Direct entry-point finding
`MURPHY_EVALUATORS_V1/murphy_runtime_entrypoint_v1.py` currently dispatches 0006, 0007, 0018, 0019, 0025, 0026, 0030, 0031, 0032, 0033, 0047, 0048, 0049, and 0051. Other rule IDs fall through to `NOT_EVALUABLE` except the special 0018/0019 handling. The entry point therefore does not prove all 35 rules are unified-runtime routed.

## Rule-specific evidence retained
- 0047 authoritative occurrence count remains **25**; the `24` in `CLOSURE.md` is stale metadata.
- 0048 historical reconciliation remains **186/186 exact** for `trin_ma10 > 1.20`.
- 0049 historical reconciliation remains **122/122 exact** for `trin < 0.70`.
- 0051 standalone deterministic evaluator tests remain **3/3 PASS**, but unified repository Runtime is not proven under the conservative matrix.
- 0008 remains blocked pending approved operational definition for `decisively broken`; do not infer a threshold from generic Murphy examples.

## Source limitation
The batch execution audit reports that the reconstructed evaluator workspace exposes evaluator filenames but the underlying ZIP payload reads fail with `Bad magic number for file header`. Filename presence is therefore not sufficient to mark Runtime behavior PASS.

## Decision rule
Do not reopen frozen rule semantics and do not invent thresholds. Recover readable existing evaluator payloads, then run one batch contract/runtime routing audit across all 35 rules. Promote only with direct executable routing + relevant test evidence.

2025 remains OOS and must not be used for tuning or selection.

## Immediate next work
Recover the readable evaluator payloads for the 13 Runtime-unproven frozen rules, then perform the 35-rule unified routing audit. After that, freeze the corrected Murphy Runtime baseline and move to broader Decision Brain integration.
