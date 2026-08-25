# Decision Brain Wiring Recovery Log — 2026-08-25

## Objective
Restore the governed Decision Brain runtime wiring without changing frozen rule semantics, without using 2025 for tuning, and without inventing missing rule outputs.

## Confirmed root causes
1. The frozen Decision Brain allowlist is 78 rules: 44 Nison + 34 Murphy. The allowlist is deny-by-default and must not be changed.
2. The Murphy runtime entry point was narrower than the frozen Murphy allowlist. This caused a governance/runtime mismatch.
3. The 2025 historical event producer deduplicated Murphy and Nison rows by timestamp, collapsing multiple per-rule records into a single row.
4. The final 2025 candidate stream consequently represented only MURPHY_0021, MURPHY_0022, and MURPHY_0023, while the Nison stream was collapsed separately and could emit synthetic NISON_NONE.
5. The official wiring audit therefore correctly blocked the 2025 P&L interpretation. The 0-trade output is a wiring/governance result, not strategy performance.

## Recovery performed in this checkpoint
### Restored from historical Git provenance
- Murphy 0003/0004 exact evaluator V2 restored from commit `6c85b5687b5ac42c1e0a6cf6fa506b4212760ada`.
- The preserved 0003/0004 deterministic tests restored from commit `e7f57b801f9f8b986c36fcb74b6772b2bfe7d805`.
- Restored evaluator is now at `MURPHY_EVALUATORS_V1/murphy_0003_0004_runtime_v2.py`.
- Restored tests are at `MURPHY_EVALUATORS_V1/test_murphy_0003_0004_runtime_v2.py`.
- Canonical Murphy runtime entry point now dispatches MURPHY_0003 and MURPHY_0004.

### Validation
- Local deterministic validation: PASS.
- Test module result: 1 passed.
- The historical source tests cover 7 behavioral cases plus the missing-input NOT_EVALUABLE checks, i.e. 8 assertions in total.

## Recovered-but-not-promoted runtime artifacts
### Murphy 0034–0045
Historical Git records show a recovered evaluator package and adapter QA package for rules 0034–0045. The historical checkpoint records 13 evaluator tests PASS and 5 adapter tests PASS, but explicitly says the package was a shared evaluator candidate and historical QA had not yet been run. A fail-closed runtime bridge was also recorded in historical Git. Therefore this checkpoint does not promote 0034–0045 to production runtime on the basis of test execution alone.

### Murphy 0028
Historical Git records mark 0028 as production frozen and explicitly instruct that its frozen evaluator/divergence artifacts must be preserved. The current main branch still requires artifact reconciliation before runtime promotion; no new 0028 semantics are created here.

### Murphy 0050
The canonical evidence-reconciliation registry records 0050 as frozen with 4/4 deterministic tests PASS, but the current main runtime entry point does not dispatch it. It remains a recovery/wiring gap until its exact evaluator artifact is reconciled into the unified runtime path.

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

## Next engineering boundary
The remaining required fix is the historical event fan-in: preserve one evidence record per available rule per timestamp and carry the complete per-rule provenance forward without silently overwriting rows. Downstream decision semantics must remain unchanged unless an existing frozen contract explicitly defines a multi-rule aggregation.

## Governing evidence
- `governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json`
- `governance/RULE_ADAPTER_PROVENANCE_MAPPING_V1.json`
- `PROJECT_STATE/FINAL_78_RULE_WIRING_AUDIT_2026-08-25.md`
- `PROJECT_STATE/CURRENT_MURPHY_24_RUNTIME_STATUS_2026-08-22.md`
- `OOS_2025/full_decision_brain_historical_event_producer_v1.py`
- `OOS_2025/full_decision_brain_assembler_v1.py`
- `evaluation/three_book_decision_evaluator_v1.py`
