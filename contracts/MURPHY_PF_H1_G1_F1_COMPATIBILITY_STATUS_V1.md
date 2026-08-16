# Murphy PF-H1 / PF-G1 / PF-F1 Compatibility Status V1

Status: COMPATIBILITY STATUS — NOT PRODUCTION FROZEN
Date: 2026-08-16

## H1
Exact horizontal evidence only: a canonical geometry boundary explicitly reporting `slope == 0` may satisfy the exact-horizontal prerequisite. Near-horizontal geometry has no approved tolerance and MUST remain `NOT_EVALUABLE`. Boundary provenance and availability remain mandatory.

## G1
Convergence/parallelism must come from canonical geometry relationship evidence. Slope-sign combinations alone MUST NOT be treated as proof of convergence or parallelism. Missing relationship evidence or unapproved approximate tolerance MUST return `NOT_EVALUABLE`.

## F1
The preceding directional-move relation can be represented deterministically when direction, chronology, and provenance are available. The source-descriptive word "sharp" has no approved deterministic project threshold in the current contract set; any sharpness-dependent decision MUST remain `NOT_EVALUABLE` until an approved definition exists.

## Reuse rule
These primitives must reuse canonical PIVOT_SEQUENCE_V2 / TRENDLINE_GEOMETRY_V1 outputs. Do not create replacement pivot or geometry engines. Do not add percentage, ATR, pip, slope, angle, clustering, or bar-count tolerances unless an approved project contract explicitly supplies them.

## Production gate
This status document does not freeze H1/G1/F1. Production readiness requires deterministic tests, no-lookahead/provenance QA, 2016–2024 historical QA, and freeze-manifest approval. 2025 remains OOS and MUST NOT be used for tuning or operator selection.
