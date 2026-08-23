# Murphy 2025 Fresh Coverage Compatibility Audit V1

Date: 2026-08-23
Status: AUDIT_COMPLETE / PRODUCER_NOT_COMPLETE
Purpose: determine the smallest safe path to fresh Murphy 2025 coverage without rebuilding Murphy knowledge or using 2025 for tuning.

## Baseline
- Frozen allowlist: 34 Murphy + 44 Nison; Murphy 0008 excluded.
- Current 2025 coverage report is OOS_COVERAGE_ONLY.
- Murphy entries in that report are a frozen reporting snapshot, not a fresh 2025 producer run.
- Therefore no Murphy profitability claim is authorized from the current report.

## Key compatibility findings
### MURPHY_0021 — first clean fresh-production candidate
Existing evaluator semantics are already explicit: price direction = close vs previous_close; confirmation uses the existing volume_direction; no new threshold is introduced. Fresh 2025 execution can therefore be pursued through the existing evaluator/bridge once the governed 2025 source path is supplied. This is an integration task, not a new rule-definition task.

### MURPHY_0003 / MURPHY_0004 — existing evaluator, upstream pivot evidence still needed
The existing evaluator consumes current_reaction_trough and prior_reaction_trough. The project already has a pivot-sequence contract whose rules say to use pivots produced by the existing Market Structure layer, preserve source timestamp/value, require confirmed pivots, and never redefine pivot semantics. The existing pivot contract explicitly excludes 2025 from tuning/selection. Fresh 2025 coverage therefore requires running the existing pivot-sequence production path on the 2025 source; it does not justify inventing a new pivot detector.

### MURPHY_0022 / MURPHY_0023 — hard upstream data gap
The evaluator requires futures open-interest direction in addition to price and volume. The GBPUSD H1 source path used for the current OOS production does not provide an authoritative futures-OI field. These rules remain NOT_EVALUABLE unless an approved OI source/contract already exists; no proxy or synthetic OI is permitted.

### MURPHY_0028 / MURPHY_0029 — 2025 divergence evidence not currently frozen
The project contains an oscillator-divergence module using existing RSI_14 and confirmed pivot sequences, with no added thresholds and a later-pivot confirmation timestamp. Its stored contract is explicitly marked 2020-2024 and `2025_used: false`. Therefore the 2025 divergence module must be explicitly produced/frozen before these rules can be promoted to fresh 2025 evidence. Reusing 2020-2024 output as 2025 evidence is prohibited.

### MURPHY_0050 — checklist is intentionally fail-closed
The evaluator is already implemented as a pre-trade checklist and cannot generate direction. Its contract lists unresolved upstream requirements including sector/breadth, explicit weekly/monthly review mapping, combined retracement/gap evidence, combined reversal/continuation evidence, and confirmed moving-average evidence. The project evidence matrix marks multiple items unavailable or only partial. Therefore 0050 stays NOT_EVALUABLE until those exact upstream contracts exist; we must not add indicators merely to make 0050 pass.

### MURPHY_0030-0033 — runtime exists, but 2025 evidence remains OOS-bound
The runtime audit confirms executable adapters and smoke verification for these rules, while historical QA remains 2016-2024 and 2025 remains excluded from tuning/selection. Fresh 2025 use must therefore come from an explicitly governed source path, not historical replay.

### MURPHY_0013-0020 and other contract-gated rules
Existing project records contain candidate/frozen-boundary work that was not uniformly production-frozen. These rules must not be promoted to fresh 2025 evidence merely because an evaluator or historical artifact exists.

## Measurement-quality issue discovered
The current Murphy frozen snapshot uses `available_rows` values that are not semantically identical to Nison availability metrics in the same combined coverage JSON (for example, MURPHY_0021 reports 6,216 available rows while also reporting 36 NOT_EVALUABLE rows). Therefore the combined `27 rules with any available evidence / 1 full available rate` figures should not be interpreted as a perfectly normalized cross-family evaluability metric. Before the next combined coverage report, the reporting contract should separate:
- rows_emitted
- evaluable_rows
- pass_rows
- fail_rows
- not_evaluable_rows
- source_available_rows

No historical baseline is being rewritten; this is a forward measurement correction.

## Decision
Do not rebuild Murphy.
Do not tune 2025.
Do not invent missing upstream facts.
Do not call the current report a Final 78-rule OOS result.

## Next execution order
1. Fresh-produce MURPHY_0021 through the existing evaluator/bridge on the governed 2025 source.
2. Produce 2025 pivot evidence using the existing pivot-sequence contract, then audit 0003/0004 compatibility.
3. Audit whether an already-approved 2025 RSI-divergence production path exists; otherwise keep 0028/0029 blocked.
4. Keep 0022/0023 and 0050 blocked unless their exact upstream contracts are found in the existing project.
5. Run a normalized fresh Murphy coverage report, checkpoint it, then combine with Nison only if coverage semantics are consistent.
