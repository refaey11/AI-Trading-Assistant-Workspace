# Murphy 0008 — Final QA Edge / Provenance Audit V1

Status: CANDIDATE QA PASS — NOT PRODUCTION FROZEN

## Execution basis
Fresh executable audit against the reconstructed Rule Evaluator D1/Pivot path available in the project runtime.
Scope: GBPUSD D1, 2016–2024 only. 2025 excluded.

## Frozen validation operator used for this audit
- Support = one confirmed LOW pivot from PIVOT_SEQUENCE_V2.
- Support must be available before break observation.
- First completed D1 close strictly below Support = candidate.
- The immediately following completed D1 bar must also close strictly below the same Support to confirm.
- Retest observation begins strictly after confirmation.
- No clustering, tolerance, ATR, pips, percentage, hidden lookback, or 2025 selection.

## Results
- Confirmed LOW pivots: 344
- First-break candidates: 326
- Decisive-break confirmations: 242
- Candidates without immediate confirmation: 84
- Later range-intersection retests: 233 / 242 (96.28%)
- Later intersecting bars closing below Support (role-reversal evidence): 229 / 242 (94.63%)

## Provenance / chronology checks
- Unique support pivot identity per confirmed event: 242 / 242
- Confirmation timestamp duplicates: 78 shared timestamps across distinct support levels; these are NOT duplicate events because support identity + confirmation pair is unique.
- Duplicate support + confirmation pairs: 0
- First-break timestamp <= support availability: 0 violations
- Confirmation timestamp <= support availability: 0 violations
- Confirmation <= first-break timestamp: 0 violations
- Future-pivot rewrite of historical support: none in the evaluator path
- Retest at or before confirmation: 0 by construction
- 2025 confirmations/input: 0

## Edge cases
- 84 first-break candidates do not receive the required immediate next-bar confirmation; they remain NOT_CONFIRMED and are not promoted.
- 9 confirmed events have no later range-intersection retest before the end of the 2016–2024 dataset.
- 4 confirmed events have a later range-intersection retest but no later intersecting bar that closes strictly below Support; they therefore lack role-reversal evidence.
- These are valid evidence states, not failures or inferred positives.

## Interpretation
The executable state machine is deterministic on the inspected data and passes the chronology/provenance checks above. The event-frequency diagnostics are not trading-performance metrics.

## Governance boundary
The uploaded 0008 handoff remains the controlling source-of-truth for governance and states that PF-B1/PF-H1 and the 0008 evaluator were originally PROPOSAL / NOT FROZEN. Therefore this audit records candidate QA evidence only. It does not silently override the source-of-truth governance status or declare production freeze.

## Required next gate
An explicit project governance decision must promote the validated operational contracts to the project's production status, followed by the formal freeze manifest. Until that happens, 0008 remains a validated candidate/evidence state, not a production-frozen rule.
