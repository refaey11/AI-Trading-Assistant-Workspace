# GBPUSD Rule Evaluator V2 Workspace Recovery — 2026-08-23

## Recovery
- Reconstructed the split workspace from all available parts/chunks.
- Reconstructed ZIP size: ~597.7 MB.
- `unzip -t` completed with no errors.
- Archive contains 241 readable entries.

## Content-level finding
The archive contains substantial source-derived rule contracts, evaluator artifacts, timeframe mappings, indicator outputs, and four isolated Murphy evaluator Python files.

No central end-to-end runner/exporter was found that clearly produces the frozen 2025 Decision-Event Stream from the 78-rule allowlist through Decision Brain -> process/risk gates -> execution/evaluation.

Observed Python evaluators in the archive are limited and do not constitute a central 78-rule/2025 Decision-Event runner.

## Governance
- No rule semantics changed.
- No TIZ semantics invented.
- No Risk replacement runtime created.
- 2025 remains OOS-only.
- No tuning/calibration/threshold selection performed.

## Current implication
The Rule Evaluator workspace is a source/evaluator artifact workspace, not a proven complete 2025 Decision-Event execution path. The current project must continue from existing governed adapters/contracts and must not fabricate a runner from missing semantics.

## Next controlled action
Continue recovery/content audit only where an existing authoritative source can be found. Otherwise, keep the missing runtime explicitly blocked and do not mislabel a newly reconstructed runner as an existing canonical runtime.
