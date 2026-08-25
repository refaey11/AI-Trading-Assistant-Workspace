# Decision Brain Wiring Recovery Log — 2026-08-25

## Executive status
The original final-run failure was confirmed as a runtime wiring/provenance problem, not a proven strategy-performance result.

### Current governed state
- Frozen Decision Brain scope: **78 rules = 44 Nison + 34 Murphy**.
- Murphy runtime routing: **22 / 34 ACTIVE_DISPATCHED**.
- Remaining unmounted Murphy rules: **0034–0045 (12 rules)**.
- Official 2025 P&L: **BLOCKED**.
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

### Lossless per-rule fan-in
Added `OOS_2025/governed_rule_fan_in_v1.py` and tests. The layer preserves all real rule records at a timestamp, excludes synthetic rule sentinels, and does not invent aggregation/direction. The OOS producer now preserves rule counts, IDs, and provenance while the downstream frozen evaluator retains its legacy single-evidence compatibility behavior until an approved multi-rule aggregation contract exists.

### Governance audit hardening
Added `PROJECT_STATE/MURPHY_RUNTIME_ROUTING_REGISTRY_V1.json` and updated `OOS_2025/audit_final_78_rule_wiring_v1.py` to require 34/34 ACTIVE_DISPATCHED before official P&L can run.

## Workspace recovery
The split uploaded GBPUSD rule-evaluator workspace was reconstructed locally by concatenating its three top-level parts and the four internal `.bcut` chunks for Part 03. Integrity test: **No errors detected in compressed data**. Archive contents: **241 files**.

Recovered directly from this Workspace:
- `MURPHY_EVALUATORS_V1/murphy_0027_0029_evaluator.py`
- `MURPHY_EVALUATORS_V1/MURPHY_0027_0029_EVALUATOR_CONTRACT_V1.json`
- `MURPHY_EVALUATORS_V1/murphy_0050_evaluator.py`
- `MURPHY_EVALUATORS_V1/MURPHY_0050_EVALUATOR_CONTRACT_V1.json`
- Mapping/audit tables for 0034–0045

## 0034–0045 — unresolved recovery boundary
Historical Git evidence confirms that a dedicated `MURPHY_0034_0045` evaluator package was executed successfully:
- evaluator suite: **13 passed**;
- adapter suite: **5 passed**;
- fail-closed runtime bridge exists in historical Git.

However:
- the current main repository does not contain the underlying `murphy_batch_evaluators.py` implementation package;
- the reconstructed 241-file Workspace archive does not contain it either;
- exhaustive local ZIP search for `MURPHY_BATCH_0034_0045`, `wave2`, and related implementation symbols found no second copy;
- Dropbox search for `MURPHY_BATCH_0034_0045`, `wave2`, and direct 0034–0045 evaluator names also returned no matching text artifact;
- the historical checkpoint explicitly describes the package as `SHARED_EVALUATOR_CANDIDATE`, `production_frozen=false`, `historical_qa=NOT_YET_RUN`.

Therefore **0034–0045 are intentionally not mounted**. Their mapping/audit tables are evidence about intended source conditions, not permission to invent executable logic.

## Validation completed in this recovery
- Murphy 0003/0004 preserved test module: PASS.
- Lossless governed fan-in test suite: **5/5 PASS**.
- Murphy 0028 standalone source-backed validation: PASS / FAIL / NOT_EVALUABLE behavior confirmed.
- Murphy 0050 standalone source-backed validation: complete checklist PASS; partial evidence NOT_EVALUABLE; direction always NONE.
- Core GitHub integration/governance checks on the latest recovery line are passing, including Decision Brain integration, final E2E readiness, rule allowlist, Three-Book evaluator, risk/execution, TIZ, memory, and Nison runtime groups.
- 2025/OOS-related CircleCI jobs currently fail because the governed 34-rule coverage/evidence gates are not yet satisfied. These failures are consistent with the deliberate fail-closed blocker and are not interpreted as profitability results.

## Key GitHub commits
- `b0d453cc8c5ecdbe7ace9703965eb430084f4f6b` — restore 0003/0004 evaluator.
- `7979b2d1b63e887f3447ebee6eec5c915648dd8a` — restore 0003/0004 tests.
- `93f953d3e19461ae62fa8329744a8848458cda12` — wire 0003/0004.
- `a2a529886da3e327879fe8b8253a1077ec654395` — wire 0029.
- `4d051081cb01a967024a211da662bf6ea6519353` — add lossless fan-in.
- `e67a25d9cd65853db5d5e43828a4a4d9d4c95f57` — fan-in tests.
- `5530d77d5023fd0402a1263ef07f05f3d7526270` — update OOS producer.
- `3a242a72293d7966377df93c520dc08309c72fbe` — routing registry.
- `33d4fb32f6a6f5006a4d4cc3dc56fcf1275cedda` — fail-closed audit hardening.
- `6e95a7aa89ed54cd3feccbc646330a2d7ad94692` — restore 0028.
- `465abaae8149bb245a5190b0e9012a2eeef1693c` — restore 0050.
- `d7091c47d1e099b83ff8232fc749fe2d410c661b` — wire 0028/0050.
- `d0f8b58ef7eefb469a8b095a2b6812d3cb636fe6` — mark 22 ACTIVE_DISPATCHED.
- `4f0e9da37fa51de4c8a1e0bc015f573902c49921` — preserve 0028/0029 contract.
- `ed8670ea95754c9822fee4f619785b2380b70609` — preserve 0050 contract.
- `6828efaea95ddf099607df4784752d36b28017e0` — add runtime tests for 0028/0050.
- `f403788064b2ee44d8a7bf8315dc47563fd96689` — phase 3 recovery log.

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

## Professional stop condition for this stage
The wiring defect is materially fixed and documented. The project is **not yet ready for official 2025 P&L** because the exact source-backed implementation package for 0034–0045 is still unavailable in the connected GitHub/Dropbox/workspace artifacts. Promoting those 12 rules without the package would violate the project's own compatibility/frozen-source rules.

## Next recovery target
Recover the exact 0034–0045 implementation package from an accessible historical production-freeze artifact or Git/Dropbox source copy, then verify its dependencies and tests before mounting. No strategy changes or OOS tuning should occur while doing so.
