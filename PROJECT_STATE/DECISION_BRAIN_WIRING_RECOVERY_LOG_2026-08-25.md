# Decision Brain Wiring Recovery Log — 2026-08-25

## Objective
Restore the governed Decision Brain runtime wiring without changing frozen rule semantics, without using 2025 for tuning, and without inventing missing rule outputs.

## Confirmed root causes
1. The frozen Decision Brain allowlist is 78 rules: 44 Nison + 34 Murphy. The allowlist is deny-by-default and must not be changed.
2. The Murphy runtime entry point was narrower than the frozen Murphy allowlist. This caused a governance/runtime mismatch.
3. The 2025 historical event producer deduplicated Murphy and Nison rows by timestamp, collapsing multiple per-rule records into a single row.
4. The final 2025 candidate stream consequently represented only MURPHY_0021, MURPHY_0022, and MURPHY_0023, while the Nison stream was collapsed separately and could emit synthetic NISON_NONE.
5. The official wiring audit therefore correctly blocked the 2025 P&L interpretation. The 0-trade output is a wiring/governance result, not strategy performance.

## Recovery performed
### Restored / wired from historical Git provenance
- Murphy 0003/0004 exact evaluator V2 restored from commit `6c85b5687b5ac42c1e0a6cf6fa506b4212760ada`.
- Preserved 0003/0004 deterministic tests restored from commit `e7f57b801f9f8b986c36fcb74b6772b2bfe7d805`.
- Murphy 0029 exact runtime adapter was already present on main and has now been wired into the canonical entrypoint. Historical adapter commit: `85b8c6bfad5566288af33e4eff2e0136aeeef4b6`; historical tests: `1508fc6a8999168f50c105ca2fee689d3843cedc`.

### Canonical routing state after this recovery
There are **20 ACTIVE_DISPATCHED Murphy rules** in the current runtime entrypoint.
The remaining **14 allowlisted Murphy rules are not mounted**:
- `MURPHY_0028` — FROZEN_NOT_MOUNTED
- `MURPHY_0034` through `MURPHY_0045` — RECOVERED_NOT_MOUNTED
- `MURPHY_0050` — FROZEN_NOT_MOUNTED

This corrects the earlier overstatement that there were 15 missing rules after 0003/0004 recovery. The exact remaining gap is 14.

A dedicated routing registry now separates routing registration from runtime availability:
`PROJECT_STATE/MURPHY_RUNTIME_ROUTING_REGISTRY_V1.json`.

### 0034–0045 recovery boundary
Historical Git records show a recovered evaluator package and adapter QA package for rules 0034–0045. The historical checkpoint records 13 evaluator tests PASS and 5 adapter tests PASS, but the package remained `SHARED_EVALUATOR_CANDIDATE` with historical QA not yet run. A fail-closed runtime bridge was also recorded. Therefore this project state does not promote 0034–0045 to active runtime until the actual evaluator package is mounted and reconciled.

### 0028 boundary
Historical Git records mark 0028 as production frozen and explicitly prohibit semantic changes without compatibility audit/re-freeze. The exact current-main evaluator artifact still requires reconciliation before active routing.

### 0050 boundary
The canonical reconciliation registry records 0050 as frozen with 4/4 deterministic tests PASS, but the current main runtime entrypoint does not dispatch it. It remains a wiring gap until its exact evaluator artifact is reconciled.

## Lossless fan-in repair
A new compatibility-only fan-in layer was added at:
`OOS_2025/governed_rule_fan_in_v1.py`

The layer:
- preserves every real Murphy/Nison rule record at a timestamp;
- does not deduplicate rule evidence;
- excludes synthetic rule sentinels such as `NISON_NONE`;
- exposes explicit evidence counts and rule IDs;
- retains the old `keep='last'` single-row behavior only as a temporary compatibility selector for the frozen downstream evaluator;
- performs no directional voting, no confidence invention, and no strategy change.

The historical OOS producer was updated to use the lossless rule grouping and to emit:
- `murphy_rule_count`
- `nison_rule_count`
- `murphy_rule_ids`
- `nison_rule_ids`
- fan-in provenance metadata

The output decision semantics remain the existing frozen single-evidence behavior until an approved multi-rule aggregation contract exists.

## Validation
- 0003/0004 restored test module: PASS (1 module; 8 behavioral assertions covered by the preserved test source).
- Lossless governed fan-in test suite: **5 passed** locally.
- Murphy 0029 historical test source documents PASS/FAIL/NOT_EVALUABLE behavior and historical population reconciliation: PASS in the preserved Git source.

## Governance / audit hardening
`OOS_2025/audit_final_78_rule_wiring_v1.py` was updated to distinguish:
- entrypoint registration;
- routing-registry state;
- actual ACTIVE_DISPATCHED runtime availability.

The audit remains fail-closed and now requires all 34 allowlisted Murphy rules to be ACTIVE_DISPATCHED before official P&L can run.

## Invariants preserved
- 2025 remains OOS evaluation-only.
- No 2025 tuning, threshold selection, calibration, or semantic changes.
- Murphy remains the only directional technical source.
- Nison remains confirmation/contradiction only.
- Trading in the Zone remains a process/psychology gate only.
- Similarity/historical memory remains evidence only and cannot generate direction.
- Risk remains a hard execution gate.
- Unknown or unavailable rules remain NOT_EVALUABLE / fail-closed.
- No synthetic rule IDs are introduced.

## Current blocker
The project is **still NOT READY for official 2025 P&L** because 14 allowlisted Murphy rules are not yet actively mounted and the final multi-rule fan-in has not yet been promoted to a directional aggregation contract.

## Next engineering boundary
1. Recover/reconcile the exact runtime artifacts for 0028, 0034–0045, and 0050 from historical Git/Dropbox without changing semantics.
2. Mount and test them in the unified runtime entrypoint.
3. Run the governed per-rule evidence replay over the approved in-sample window only.
4. Verify the 34-rule fan-in/provenance gate.
5. Only after all gates pass may the existing 2025 OOS execution path be reconsidered; no tuning is permitted.

## Governing evidence
- `governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json`
- `governance/RULE_ADAPTER_PROVENANCE_MAPPING_V1.json`
- `PROJECT_STATE/MURPHY_RUNTIME_ROUTING_REGISTRY_V1.json`
- `PROJECT_STATE/FINAL_78_RULE_WIRING_AUDIT_2026-08-25.md`
- `PROJECT_STATE/CURRENT_MURPHY_24_RUNTIME_STATUS_2026-08-22.md`
- `OOS_2025/governed_rule_fan_in_v1.py`
- `OOS_2025/full_decision_brain_historical_event_producer_v1.py`
- `OOS_2025/full_decision_brain_assembler_v1.py`
- `evaluation/three_book_decision_evaluator_v1.py`
