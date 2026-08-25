# Decision Brain Wiring Recovery Log — 2026-08-25

## Executive status
The original final-run failure was confirmed as a runtime wiring/provenance problem, not a proven strategy-performance result.

### Current governed state
- Frozen Decision Brain scope: **78 rules = 44 Nison + 34 Murphy**.
- Murphy runtime routing: **34 / 34 ACTIVE_DISPATCHED**.
- Official 2025 P&L: **BLOCKED pending full OOS evidence/provenance validation**.
- 2025 remains evaluation-only; no tuning/calibration/threshold selection is allowed.

## Root causes fixed
1. Canonical Murphy runtime entrypoint was narrower than the frozen 34-rule scope.
2. Historical OOS producer used timestamp deduplication, collapsing multiple per-rule evidence records.
3. Synthetic `NISON_NONE` could enter the pre-existing one-row fan-in boundary.
4. Governance did not cleanly distinguish registration from actual runtime availability.

## Fixes completed
### Murphy 0003/0004
Recovered exact historical evaluator semantics and tests from Git provenance; wired into canonical runtime.

### Murphy 0029
Existing source-backed adapter found on main and wired into canonical runtime. Historical test provenance also verified.

### Murphy 0028
Recovered exact evaluator and contract from preserved Workspace artifact. Wired into runtime. Missing evidence remains NOT_EVALUABLE; no new threshold/timeframe semantics.

### Murphy 0050
Recovered exact structural checklist evaluator and contract from preserved Workspace artifact. Wired into runtime. It remains a pre-trade checklist only and cannot generate direction. Incomplete evidence remains NOT_EVALUABLE.

### Murphy 0034–0045
Recovered exact evaluator implementation from user-supplied `MURPHY_BATCH_0034_0045_PRODUCTION_FREEZE_V1(5).zip`.
- Source artifact SHA256: `c57429c17f1b457189e51f97a529799247b58d5f5d25940985c31fbeb67a8912`.
- Adapter artifact SHA256: `93923c74825ca9941cfc7fe309b54669fe8d79da00436c30fa42827340401a1c`.
- Original evaluator tests: **13 passed**.
- Original adapter QA tests: **5 passed**.
- Canonical recovered runtime smoke test: **12/12 rule routes PASS** with fail-closed confirmation behavior preserved separately.
- The outer batch freeze is a **rule-contract/evidence freeze, not a profitability claim**.
- The inner `BATCH_STATUS.json` still records `production_frozen=false` and `historical_qa=PENDING`; therefore mounting the evaluator is valid runtime recovery, but it does **not** authorize profitability claims.
- 2025 was not used for tuning.

### Lossless per-rule fan-in
Added `OOS_2025/governed_rule_fan_in_v1.py` and tests. The layer preserves all real rule records at a timestamp, excludes synthetic rule sentinels, and does not invent aggregation/direction.

### Governance audit hardening
Added `PROJECT_STATE/MURPHY_RUNTIME_ROUTING_REGISTRY_V1.json` and updated `OOS_2025/audit_final_78_rule_wiring_v1.py` to require 34/34 ACTIVE_DISPATCHED before official P&L can run.

## Workspace recovery
The split uploaded GBPUSD rule-evaluator workspace was reconstructed locally by concatenating its three top-level parts and the four internal `.bcut` chunks for Part 03. Integrity test: **No errors detected in compressed data**. Archive contents: **241 files**.

## Validation completed in this recovery
- Murphy 0003/0004 preserved test module: PASS.
- Lossless governed fan-in test suite: **5/5 PASS**.
- Murphy 0028 standalone source-backed validation: PASS / FAIL / NOT_EVALUABLE behavior confirmed.
- Murphy 0050 standalone source-backed validation: complete checklist PASS; partial evidence NOT_EVALUABLE; direction always NONE.
- Murphy 0034–0045 original evaluator suite: **13 passed**.
- Murphy 0034–0045 original adapter suite: **5 passed**.
- Murphy 0034–0045 canonical runtime smoke validation: **12/12 routes PASS**.
- Core GitHub integration/governance checks on the recovery line are passing, including Decision Brain integration, final E2E readiness, rule allowlist, Three-Book evaluator, risk/execution, TIZ, memory, and Nison runtime groups.
- 2025/OOS-related CircleCI jobs remain blocked/failing until full governed evidence coverage is satisfied. These are not interpreted as profitability results.

## Key latest GitHub commits
- `5bcdb609c8ff5fd3eda1402668657644a0e8c860` — recovered exact Murphy 0034–0045 evaluator source.
- `1772251103fca80011943ecb67cad06094186a1a` — recovered exact Murphy 0034–0045 adapter contract.
- `4d2fabcf76359d11d11a164c379911bbdf879ac9` — mounted 0034–0045 into canonical Murphy runtime entrypoint.
- `ab221d9cfca25c59a7e829e51f78f4f33057c8a1` — promoted all 34 Murphy rules to ACTIVE_DISPATCHED in the routing registry.
- `5e7109763ef43cb4364e8d420b992e5feb84bfe7` — added canonical 0034–0045 runtime tests.

## Governance invariants
- Never change the frozen 78-rule allowlist for the sake of passing the OOS.
- Never invent missing Murphy outputs.
- Never synthesize Nison rule IDs.
- Murphy alone can generate technical direction.
- Nison confirms/contradicts only.
- TIZ gates process/psychology only.
- Similarity/historical memory is evidence only.
- Risk is a hard gate.
- Missing or unavailable evidence remains NOT_EVALUABLE.
- Historical QA gaps do not justify 2025 tuning or profitability claims.

## Current engineering boundary
The **34/34 Murphy runtime mounting blocker is resolved** using the exact user-supplied production-freeze evaluator artifact. The next blocker is no longer missing Murphy runtime code; it is **full end-to-end 78-rule OOS provenance/evidence validation** and verification that the final Decision Brain consumes all available rule evidence without lossy reduction.

## Next engineering target
Run a governed 2025 **diagnostic coverage/provenance pass only** (not P&L tuning) to verify that all 34 Murphy and 44 Nison rule evidence sets reach the Final Brain fan-in correctly. Only after that gate passes can official 2025 execution/P&L be reconsidered.
