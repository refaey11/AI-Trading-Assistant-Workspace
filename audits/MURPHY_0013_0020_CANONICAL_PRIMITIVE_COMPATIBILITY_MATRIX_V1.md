# Murphy 0013-0020 — Canonical Primitive Compatibility Matrix V1

Status: GOVERNANCE / COMPATIBILITY AUDIT — NOT PRODUCTION FROZEN
Date: 2026-08-16

## Purpose
Bind Rules 0013-0020 to existing canonical Pivot/Geometry infrastructure without rebuilding it, and record the current closure state of shared primitives.

## Canonical upstreams
- PIVOT_SEQUENCE_V2: reuse required.
- TRENDLINE_GEOMETRY_V1: reuse required.
- VOLUME_CONFIRMATION_V2: reuse only where source-compatible.

## Shared primitive closure
| Primitive | Canonical upstream reuse | Deterministic production contract | Current decision |
|---|---|---|---|
| PF-H1 | Pivot-derived levels / existing S-R identity | No approved horizontal tolerance/level-cluster contract proven | NOT_EVALUABLE for approximate horizontal cases |
| PF-G1 | TRENDLINE_GEOMETRY_V1 | No approved numeric convergence/parallelism tolerance proven | Exact geometry may be represented; approximate cases remain NOT_EVALUABLE |
| PF-B1 | Existing breakout infrastructure if approved | No approved shared decisive-break policy proven for 0013-0020 | NOT_EVALUABLE unless an explicit policy is supplied |
| PF-F1 | Canonical price/pivot path | "Sharp" remains descriptive; no deterministic threshold approved | NOT_EVALUABLE until governed |

## Rule mapping
- 0013: PF-01 + PF-02 + descending upper + ascending lower + PF-G1 + PF-B1.
- 0014: PF-01 + PF-02 + PF-H1 + ascending lower + PF-B1.
- 0015: PF-01 + PF-02 + PF-H1 + descending upper + PF-B1.
- 0016: PF-F1 + channel/parallel relation + PF-B1 (+ compatible volume context).
- 0017: PF-F1 + 0013 triangle geometry + PF-B1 (+ compatible volume context).
- 0018: PF-02 + downward boundaries + PF-G1 + PF-B1.
- 0019: PF-02 + upward boundaries + PF-G1 + PF-B1.
- 0020: PF-01 + PF-H1 range + horizontal/parallel boundaries + PF-B1.

## Governance conclusions
1. Existing Pivot and Geometry components are upstream dependencies, not permission to invent missing rule operators.
2. Murphy source semantics are closed enough to define structural intent, but the project-specific deterministic contracts for horizontal classification, convergence/parallelism, breakout confirmation, and flagpole sharpness are not proven frozen by the accessible evidence.
3. Therefore the structural evaluator may be used only as a non-production, fail-closed layer.
4. Any missing required primitive must yield NOT_EVALUABLE rather than an inferred PASS/FAIL.
5. 2025 remains OOS and is excluded from tuning/operator selection.

## Freeze gate
No 0013-0020 rule may be marked production frozen until:
source provenance -> explicit primitive contracts -> evaluator -> deterministic tests -> 2016-2024 historical QA -> availability/no-lookahead -> provenance/freeze manifest.

## Important status conflict
A later continuity backup records 0008 as production frozen while earlier PF-B1 artifacts explicitly record PF-B1 as not frozen. That conflict is preserved and must not be silently used to declare PF-B1 closed for 0013-0020.
