# Murphy 39 Factory — Next Execution Plan V1

Purpose: execute the 39-rule batch using existing shared accelerators without inventing semantics.

## Batch policy
- Frozen 12 remain excluded.
- No auto-freeze.
- 2025 remains OOS and is never used for tuning, selection, calibration, or operator choice.
- Existing canonical source records remain authoritative.
- NOT_EVALUABLE is preferred over fabricated evidence.

## Execution lanes
1. AUDIT_READY rules: run their declared shared accelerator / next gate in batch.
2. NOT_EVALUABLE rules: collect the exact missing source/compatibility evidence; do not fabricate operators.
3. Shared accelerators are reused; rule semantics remain rule-specific.
4. Any accelerator failure is recorded once and mapped to all affected rules.
5. Historical QA starts only after semantic/operator closure for each rule.

## Current first-pass groups
- PNF: 0030, 0031, 0032
- Pivot Sequence V2: 0005, 0011, 0012, 0014, 0015
- Shared Evidence / Geometry: 0001, 0009, 0010, 0013, 0016, 0017, 0018, 0019, 0020, 0034, 0035, 0036, 0038, 0050
- Existing indicator modules: 0024, 0037, 0040, 0041
- Risk Engine: 0042, 0043, 0044, 0045
- Breadth data: 0046, 0047, 0048, 0049
- Decision/process gates: 0039, 0051
- Nison integration: 0033

## Stop conditions
Stop and record BLOCKED/NOT_EVALUABLE when source semantics, operator compatibility, availability/no-lookahead, or deterministic behavior is not established. Never substitute optimization or guessed thresholds.
