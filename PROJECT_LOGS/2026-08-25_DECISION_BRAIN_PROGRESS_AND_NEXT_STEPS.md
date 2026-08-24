# AI Trading Assistant — Decision Brain
## Project Progress Log — 2026-08-25

### Current position
The project is in the governed 2025 OOS integration / final Decision Brain evaluation stage. The existing architecture and frozen contracts are being reused; no new trading-rule semantics are being introduced and 2025 is evaluation-only.

### What was completed in the latest work
1. Added / wired the historical Full Decision Brain producer path around the existing governed assembler.
2. The current assembler composes:
   - existing Decision Brain governance handoff;
   - existing Three-Book decision evaluator;
   - frozen OOS execution adapter;
   - existing Murphy direction/context;
   - Nison confirmation/contradiction as confirmation/context only;
   - TIZ as process/psychology gate and never as a direction generator;
   - risk as a hard execution gate;
   - historical memory as evidence only, never sole direction.
3. Added a governed full 78-rule 2025 event-stream runner and current coverage path.
4. Added/used Nison evidence aggregation by timestamp without creating standalone direction.
5. Preserved the OOS governance policy:
   - no 2025 tuning;
   - no 2025 threshold selection;
   - no fabricated missing evidence;
   - missing evidence remains NOT_EVALUABLE;
   - Similarity/Prediction is not a standalone direction source;
   - no profitability number is promoted until the official gate is satisfied.
6. The CI pipeline was triggered so the integration and OOS jobs can execute against the existing project sources.

### Current CI state observed
The core compatibility / governance checks already reported success in the latest status snapshot, including Decision Brain integration, final E2E readiness, risk execution runtime, frozen execution bridge, frozen 2025 OOS evaluator contract, three-book evaluator, Nison runtime groups, memory boundaries, rule allowlist, and TIZ optional execution adapter.

The following OOS production jobs were still pending at the time this log was written:
- nison_2025_full_production_v1
- oos_2025_78_rule_coverage_v1
- murphy_0021_2025_fresh_v1
- murphy_0022_0023_2025_pit_v1
- nison_evidence_aggregate_v1
- historical_outcome_memory_v1
- memory_integration_v1
- rule_adapter_allowlist_runtime_gate_v1

### Important boundary
There is NO official 2025 profitability result yet. The existing profitability-readiness contract explicitly requires the authoritative 2025 source, full governed 78-rule event stream, governed Decision Brain direction, preserved Nison contradiction handling, frozen risk/execution eligibility, and an explicit no-tuning OOS statement before any profitability number can be promoted.

### What we do next
1. Wait for the currently pending OOS production jobs to finish.
2. Inspect the generated CI artifacts/manifests and verify source provenance, row counts, rule coverage, joinability, and gate statuses.
3. If all required evidence streams are complete, run the governed full Decision Brain event assembly on the authoritative 2025 inputs.
4. Only after the full governed event stream passes the official readiness gate, run/promote the official 2025 profitability evaluation.
5. If any job fails, fix only the contract/wiring/data-provenance issue; do not tune 2025 to make the result pass.

### Source-of-truth policy
Existing project knowledge and frozen contracts remain authoritative. New work must integrate with those artifacts rather than rebuild them from scratch. 2025 remains OOS and must never be used for tuning.
