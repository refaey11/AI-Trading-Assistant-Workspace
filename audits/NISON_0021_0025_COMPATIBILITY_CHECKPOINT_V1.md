# Nison 0021–0025 Compatibility Checkpoint V1

Status: AUDIT CHECKPOINT — NOT FROZEN

## Scope
Rules 0021–0025 from the existing Nison 44-rule registry/checkpoint. This record is source-bounded and does not create canonical semantics where the currently transferred source evidence is incomplete.

## Governance
- Nison remains confirmation/evidence only.
- No invented thresholds, lookbacks, tolerances, scoring, or direction generation.
- 2025 remains OOS and is excluded from tuning/selection/calibration/optimization.
- Generic Murphy or generic candlestick primitives cannot be silently treated as Nison semantics.
- No production freeze is granted by this checkpoint.

## Rule decisions

| Rule | Name | Compatibility decision | Blocking gate |
|---|---|---|---|
| 0021 | Three Mountains | NOT_EVALUABLE | Source-locked multi-swing topology plus confirmation/invalidation semantics are not yet operationally closed. |
| 0022 | Three Rivers | NOT_EVALUABLE | Source-locked topology plus confirmation/invalidation semantics are not yet operationally closed. |
| 0023 | Three Buddha Tops | NOT_EVALUABLE | Authoritative structural decomposition is required; do not equate it to generic head-and-shoulders. |
| 0024 | Three Buddha Bottoms | NOT_EVALUABLE | Authoritative structural decomposition is required; do not equate it to generic inverse head-and-shoulders. |
| 0025 | Dumpling Top | NOT_EVALUABLE | Source-locked rounding/volume/context semantics are not operationally closed; no invented curvature threshold. |

## Source-transfer constraint
The current Nison source manifest explicitly records the canonical assembled source archive and its provenance, but also states that binary source transfer to the GitHub branch was still awaiting completion. Therefore this checkpoint does **not** claim that exact source passages for 0021–0025 were newly extracted in this step.

## Next gate
1. Complete binary/extracted source transfer into the branch.
2. Locate exact Nison passages for 0021–0025.
3. Decompose each rule into hard canonical, qualitative measurable, qualitative unmeasurable, and evidence-only clauses.
4. Map only compatible existing primitives through explicit adapters.
5. Add deterministic tests and availability/no-lookahead tests only after the operational contract is source-locked.
6. Historical QA may begin only after evaluator closure; 2025 remains excluded.

## Verdict
**0021–0025: audited as NOT_EVALUABLE; no evaluator, historical QA, or freeze is claimed.**
