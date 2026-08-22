# Murphy Final Compatibility Audit — 2026-08-22

## Corrected audit result
**34 / 35 Runtime Verified**

The earlier 35/35 checkpoint was too broad, and the older 22/35 matrix was too conservative after the latest GitHub runtime adapters/tests were added. This audit reconciles the current GitHub source, current unified entry-point routing, deterministic tests, and the canonical blocker for 0008.

## Existing verified Runtime (22)
0003, 0004, 0018, 0019, 0021, 0022, 0023, 0028, 0029, 0034, 0035, 0036, 0037, 0038, 0039, 0040, 0041, 0042, 0043, 0044, 0045, 0050.

## Newly verified in this audit (12)
- 0006 — current evaluator present; unified entry-point route present; deterministic tests cover confirmation, lookahead rejection, missing evidence, and wrong candidate handling.
- 0007 — same shared evaluator/entry-point/test coverage as 0006.
- 0025 — current evaluator present; unified route present; PASS/FAIL/NOT_EVALUABLE tests present.
- 0026 — current evaluator present; unified route present; PASS/FAIL/NOT_EVALUABLE tests present.
- 0030 — current evaluator plus source-bounded 3-box P&F core; unified route and deterministic tests present. A real status-overwrite bug was fixed during this audit.
- 0031 — same source-bounded P&F core/route/test; status-overwrite bug fixed.
- 0032 — same source-bounded P&F core/route/test; status-overwrite bug fixed.
- 0033 — current evaluator adapter plus underlying evaluator candidate; unified route and deterministic tests present.
- 0047 — current evaluator + unified route + deterministic tests; 25/25 historical labels already reconciled in the closed final artifact.
- 0048 — current evaluator + unified route + deterministic tests; 186/186 historical labels reconciled; operator `trin_ma10 > 1.20`.
- 0049 — current evaluator + unified route + deterministic tests; 122/122 historical labels reconciled; operator `trin < 0.70`.
- 0051 — current process-gate evaluator + unified route + deterministic PASS/FAIL/NOT_EVALUABLE tests.

## Blocked rule (1)
### 0008 — BLOCKED / NOT_EVALUABLE
The canonical 0006–0008 freeze artifact explicitly states that no approved operational definition exists for `decisively broken`; the fail-closed runtime is therefore authoritative. The prior GitHub 0008 runtime incorrectly promoted a generic role-reversal mapping. That code was corrected to return `NOT_EVALUABLE`, and the tests were changed to assert fail-closed behavior until an approved PF-B1 binding exists.

## Runtime entry-point evidence
`MURPHY_EVALUATORS_V1/murphy_runtime_entrypoint_v1.py` explicitly dispatches 0006, 0007, 0018, 0019, 0025, 0026, 0030, 0031, 0032, 0033, 0047, 0048, 0049, and 0051. The remaining verified rules are part of the established integrated Runtime set represented by the existing runtime inventories.

## Direct execution checks performed
- 0006/0007 shared evaluator: confirmation and fail-closed/lookahead cases reproduce the current tests.
- 0025/0026 evaluator: PASS/FAIL/NOT_EVALUABLE cases reproduce the current tests.
- 0030/0031/0032: local smoke reproduced the current test payloads; all three return PASS after the status-overwrite fix.
- 0033 underlying evaluator: confirmed contextual payload reproduces `CONFIRMED / NEUTRAL`.
- 0047: PASS/FAIL/NOT_EVALUABLE logic matches current tests.
- 0048/0049: source-bounded operators match current tests and historical reconciliation counts.
- 0051: complete/empty/unknown field cases match current tests.
- 0008: corrected runtime intentionally returns NOT_EVALUABLE.

## Historical evidence retained
- 0047 authoritative occurrence count = 25; the `24` in `CLOSURE.md` is stale metadata.
- 0048 exact historical reconciliation = 186/186 for `TRIN_MA10 > 1.20`.
- 0049 exact historical reconciliation = 122/122 for `TRIN < 0.70`.

## Verification boundary
This audit does not claim a GitHub Actions CI run. The available connector exposes workflow inspection but not manual workflow dispatch. Direct local execution plus source/test inspection are used here.

## Constraints preserved
- 2025 remains OOS and is not used for tuning or selection.
- No new Murphy thresholds were invented.
- No proxy substitution was introduced.
- Frozen rule semantics were not silently rewritten.

## Immediate next action
Freeze the corrected **34/35** Murphy Runtime baseline. Keep 0008 blocked until an approved PF-B1 decisive-break definition is source-locked, then return to broader Decision Brain integration work without reopening the 34 verified rule contracts.
