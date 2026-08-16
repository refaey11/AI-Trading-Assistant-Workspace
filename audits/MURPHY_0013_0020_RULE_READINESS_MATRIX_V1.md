# Murphy 0013-0020 Rule Readiness Matrix V1

Status: READINESS / NOT PRODUCTION FROZEN
Date: 2026-08-16

| Rule | Structural primitive | Additional primitive | Breakout | Current readiness |
|---|---|---|---|---|
| 0013 Symmetrical Triangle | G1 exact convergence | Pivot/chronology | B1 required | BLOCKED by B1 production policy |
| 0014 Ascending Triangle | H1 exact horizontal | positive lower boundary | B1 required | BLOCKED by B1 production policy |
| 0015 Descending Triangle | H1 exact horizontal | negative upper boundary | B1 required | BLOCKED by B1 production policy |
| 0016 Flag | F1 flagpole relation | G1/channel geometry | B1 required | BLOCKED by B1 + sharpness definition |
| 0017 Pennant | F1 flagpole relation | G1/triangle geometry | B1 required | BLOCKED by B1 + sharpness definition |
| 0018 Falling Wedge | G1 exact convergence | both boundaries negative slope | B1 required | BLOCKED by B1 production policy |
| 0019 Rising Wedge | G1 exact convergence | both boundaries positive slope | B1 required | BLOCKED by B1 production policy |
| 0020 Rectangle | H1 exact horizontals | G1 exact parallelism | B1 required | BLOCKED by B1 production policy |

## Shared status
- Canonical PIVOT_SEQUENCE_V2: reuse required.
- Canonical TRENDLINE_GEOMETRY_V1: reuse required.
- PF-H1: exact-only fail-closed compatibility contract exists; near-horizontal remains NOT_EVALUABLE.
- PF-G1: exact geometry compatibility exists; unapproved approximate tolerance remains NOT_EVALUABLE.
- PF-B1: fail-closed compatibility contract exists, but no production-frozen policy is approved for these Murphy rules.
- PF-F1: chronology/direction relation can be deterministic; "sharp" remains NOT_EVALUABLE without an approved definition.

## Interpretation
Structural evaluators may operate as evidence-producing components, but a structural result is not a complete Murphy rule confirmation while required gates remain unresolved.

## Freeze rule
No production freeze, historical QA sign-off, or performance tuning is authorized from this matrix alone. 2025 remains OOS and must not be used for tuning.
