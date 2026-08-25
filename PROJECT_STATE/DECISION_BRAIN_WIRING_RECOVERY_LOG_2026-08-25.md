# Decision Brain Wiring Recovery Log — 2026-08-25

## Objective
Restore the governed Decision Brain runtime wiring without changing frozen rule semantics, without using 2025 for tuning, and without inventing missing rule outputs.

## Confirmed root causes
1. Frozen Decision Brain allowlist = 78 rules: 44 Nison + 34 Murphy; deny-by-default.
2. Murphy runtime entrypoint was narrower than the frozen Murphy allowlist.
3. Historical OOS producer deduplicated Murphy/Nison rows by timestamp, collapsing multiple per-rule records.
4. The final 2025 candidate stream therefore represented only Murphy 0021/0022/0023; Nison could emit synthetic `NISON_NONE` after collapse.
5. The official final wiring audit therefore correctly blocked official 2025 P&L. The 0-trade output was a wiring/governance result, not strategy performance.

## Phase 2 completed
- Restored/wired Murphy 0003/0004 from historical Git provenance.
- Wired existing Murphy 0029 adapter into the canonical runtime entrypoint.
- Added lossless per-rule fan-in compatibility layer.
- Updated OOS producer to preserve per-rule counts/IDs/provenance while keeping frozen downstream decision semantics unchanged.
- Added Murphy runtime routing/availability registry.
- Hardened final 78-rule audit to distinguish registration from actual ACTIVE_DISPATCHED availability.

## Phase 3 — Workspace recovery and additional Murphy routing
### Workspace reconstruction
The split GBPUSD rule-evaluator workspace was reconstructed locally from uploaded parts:
- `GBPUSD_RULE_EVALUATOR_V2_WORKSPACE_PART_01_OF_03.zip.part`
- `GBPUSD_RULE_EVALUATOR_V2_WORKSPACE_PART_02_OF_03.zip.part`
- `GBPUSD_RULE_EVALUATOR_V2_WORKSPACE_PART_03_OF_03.zip_part1.bcut` through `_part4.bcut`

The reconstructed archive contains **241 files** and was verified with `unzip -t`: `No errors detected in compressed data`.

### Murphy 0028
Recovered exact evaluator and contract from the preserved Workspace artifact:
- `MURPHY_EVALUATORS_V1/murphy_0027_0029_evaluator.py`
- `MURPHY_EVALUATORS_V1/MURPHY_0027_0029_EVALUATOR_CONTRACT_V1.json`

The source contract says 0028 is implemented and passes only on confirmed BEARISH divergence at HIGH pivot; 0029 is implemented on confirmed BULLISH divergence at LOW pivot. 0027 remains blocked until the exact trend-vs-ranging operator is defined. No threshold or timeframe was invented.

0028 is now dispatched in the canonical runtime entrypoint and marked `ACTIVE_DISPATCHED` in the routing registry.

### Murphy 0050
Recovered exact structural evaluator and contract:
- `MURPHY_EVALUATORS_V1/murphy_0050_evaluator.py`
- `MURPHY_EVALUATORS_V1/MURPHY_0050_EVALUATOR_CONTRACT_V1.json`

0050 is explicitly a pre-trade multi-factor checklist. It cannot generate BUY/SELL, cannot guess missing evidence, and cannot mark partial evidence as PASS. Its preserved current state is `NOT_EVALUABLE`, with missing sector/breadth, weekly/monthly mapping, combined retracement/gaps, combined pattern evidence, and incomplete MA evidence listed as blockers. `2025_used=false`.

0050 is now dispatched in the canonical runtime entrypoint and marked `ACTIVE_DISPATCHED` in the routing registry. This means the evaluator is mounted; it does not mean the checklist is PASS.

### Validation
Standalone source-backed validation completed:
- Murphy 0028: PASS / FAIL / NOT_EVALUABLE behavior verified.
- Murphy 0050: all-PASS checklist returns PASS; missing evidence returns NOT_EVALUABLE; direction remains NONE.

## Current canonical Murphy routing state
- **22 ACTIVE_DISPATCHED**
- **12 RECOVERED_NOT_MOUNTED**: 0034–0045
- **34 total allowlisted Murphy rules**

Official 2025 P&L remains blocked until 34/34 ACTIVE_DISPATCHED and all governing fan-in/coverage gates pass.

## Important status of 0034–0045
Historical Git recovery shows a shared evaluator candidate and fail-closed bridge with 13 evaluator tests PASS and 5 adapter QA tests PASS, but the preserved status explicitly says `SHARED_EVALUATOR_CANDIDATE`, `production_frozen=false`, and `historical_qa=NOT_YET_RUN`. The current recovered Workspace archive contains mapping/audit tables for 0034–0045 but does not contain the actual `murphy_batch_evaluators.py` implementation module. Therefore these 12 rules remain NOT MOUNTED and are not invented.

## Invariants preserved
- 2025 = OOS evaluation-only; no tuning/calibration.
- Murphy remains the only directional book.
- Nison = confirmation/contradiction only.
- TIZ = process/psychology gate only.
- Similarity/historical memory = evidence only.
- Risk = hard gate.
- Unknown/missing evidence = NOT_EVALUABLE / fail closed.
- No synthetic rule IDs.
- No new indicator thresholds or timeframe assumptions.

## Latest GitHub commits in this recovery
- `6e95a7aa89ed54cd3feccbc646330a2d7ad94692` — restore exact 0028 evaluator.
- `465abaae8149bb245a5190b0e9012a2eeef1693c` — restore exact 0050 evaluator.
- `d7091c47d1e099b83ff8232fc749fe2d410c661b` — wire 0028/0050 into runtime entrypoint.
- `d0f8b58ef7eefb469a8b095a2b6812d3cb636fe6` — update routing registry to 22 ACTIVE_DISPATCHED.
- `4f0e9da37fa51de4c8a1e0bc015f573902c49921` — preserve 0027–0029 evaluator contract.
- `ed8670ea95754c9822fee4f619785b2380b70609` — preserve 0050 evaluator contract.

## Next engineering boundary
Recover the exact missing 0034–0045 evaluator implementation from the available historical Git/Dropbox/workspace artifacts, mount only the source-backed implementation, run the approved in-sample QA, then move the 12 rules to ACTIVE_DISPATCHED only after their contract and runtime dependencies are present.
