# Murphy Final Compatibility Audit — 2026-08-22

## Audit result
The earlier `35/35 Runtime` checkpoint is **retracted as a runtime claim**. The canonical Murphy runtime matrix currently supports:

- **22 / 35 Runtime VERIFIED**
- **13 / 35 Frozen / Runtime NOT PROVEN**

This correction is intentional: Frozen/Closed status must not be converted into Runtime Implemented without executable routing/entry-point integration and relevant tests.

## Verified Runtime (22)
0003, 0004, 0018, 0019, 0021, 0022, 0023, 0028, 0029, 0034, 0035, 0036, 0037, 0038, 0039, 0040, 0041, 0042, 0043, 0044, 0045, 0050.

## Frozen / Runtime NOT PROVEN (13)
0006, 0007, 0008, 0025, 0026, 0030, 0031, 0032, 0033, 0047, 0048, 0049, 0051.

## Direct audit finding
`MURPHY_EVALUATORS_V1/murphy_runtime_entrypoint_v1.py` currently dispatches 0006, 0007, 0018, 0019, 0025, 0026, 0030, 0031, 0032, 0033, 0047, 0048, 0049, and 0051, while returning `NOT_EVALUABLE` for any other rule not in the 0018/0019 special case. Therefore the entry point itself does **not** prove all 35 rules are unified-runtime routed.

## Existing evidence retained
- 0047 historical reconciliation remains valid: authoritative count 25; stale `24` metadata corrected.
- 0048 remains 186/186 historical reconciliation against `TRIN_MA10 > 1.20`.
- 0049 remains 122/122 historical reconciliation against `TRIN < 0.70`.
- 0051 deterministic contract tests remain 3/3 PASS for the standalone evaluator, but unified repository runtime verification remains pending under the conservative matrix.
- 0008 remains blocked by the approved operational definition for `decisively broken`; generic Murphy examples must not become the rule threshold without explicit source binding.

## Source limitation
The batch execution audit states that the reconstructed evaluator workspace exposes evaluator filenames, but underlying ZIP payload reads fail with `Bad magic number for file header`. Presence in the inventory is therefore not enough to mark runtime behavior PASS.

## Decision
Do not reopen frozen rule semantics. Recover readable existing evaluator payloads and execute a single 35-rule contract/routing audit. Promote rules only when executable routing and tests are directly evidenced.

2025 remains OOS and must not be used for tuning or selection.
