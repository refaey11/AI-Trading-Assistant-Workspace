# Murphy 0030 Reference Policy Harness V1

Status: EXECUTED / NON-PRODUCTION REFERENCE
Date: 2026-08-15

## Scope
This harness tests determinism, prefix replay, future-suffix invariance, calibration isolation, and the proposed directional High/Low construction priority. It is NOT the production P&F engine and does not establish final Murphy source fidelity.

## Canonical input
`D1.csv`, 2,544 chronological GBPUSD D1 rows, 2016-01-03 through 2024-12-31.

## Exact candidate box diagnostics recomputed from the file
- 2021–2023: 0.5880466174775311%
- 2022–2024: 0.5839896629971284%

These values correct earlier rounded/inconsistent diagnostic values. They remain candidate diagnostics, not frozen production parameters.

## Results
- T1 Determinism: PASS
- T2 Prefix replay: PASS
- T3 Future-suffix invariance: PASS
- T4 Fold isolation: PASS when the exact recomputed fold values above are used
- T5 Directional High/Low priority: PASS at the policy-state level
- T6 Adapter isolation: NOT TESTED against the external engine

## Important limitation
The harness deliberately uses a minimal reference state machine. It must NOT be used as proof that the external `pnf-chart-system` implementation is Murphy-compatible. Production acceptance still requires the real engine/adapter implementation to be executed with the approved policy.

## Decision
The proposed High/Low policy has passed the reference-policy replay gates. The external engine integration and 0030 evaluator remain PRE-FREEZE.
