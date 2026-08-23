# Fresh Nison 2025 Evidence Coverage Scope — 2026-08-23

This report is intentionally a reporting-only OOS boundary. It does not change Nison semantics, thresholds, direction, TIZ semantics, or Risk semantics.

The existing governed Nison production job already acquires the authoritative 2025 GBPUSD H1 source and existing Market State Reader context, then emits 44 rule rows per 2025 timestamp. The production manifest already verifies 6,225 2025 H1 rows and 273,900 expected Nison evidence rows.

The fresh coverage reporter records, from the produced evidence CSV:
- total available evidence rows
- availability rate
- rules with any available evidence
- rules with full timestamp coverage
- rules with no available evidence
- per-rule PASS / FAIL / NOT_EVALUABLE counts

2025 remains OOS evaluation-only and no tuning or threshold selection is permitted.
