# Murphy PF-F1 Flagpole Relation — Fail-Closed Compatibility Contract V1

Status: COMPATIBILITY CONTRACT — NOT PRODUCTION FROZEN

## Scope
PF-F1 supplies the preceding directional-move relation required by Murphy 0016 Flag and 0017 Pennant.

## Source-backed semantics
Murphy describes the flag/pennant as being preceded by an almost straight / sharp directional flagpole. The project source reconciliation explicitly keeps "sharp" source-descriptive until a deterministic project definition is approved.

## Deterministic evidence allowed now
The primitive may represent evidence that:
- a price path precedes the formation;
- the path has a direction UP or DOWN;
- the pole ends before the formation starts;
- the required upstream records have valid availability/provenance.

## Sharpness gate
The primitive MUST NOT classify a move as "sharp" using an invented:
- percentage threshold;
- ATR multiplier;
- pip threshold;
- slope threshold;
- bar-count threshold;
- backtest-optimized threshold.

If the rule requires a deterministic sharpness decision and no approved project definition exists, PF-F1 MUST return `NOT_EVALUABLE` for the sharpness-dependent gate.

## Provenance / no-lookahead
All price-path inputs and any pivots used to define the pole must be available no later than the decision timestamp. Future-dependent or missing provenance is `NOT_EVALUABLE`.

## Rule use
- 0016: PF-F1 is required in addition to counter-trend channel geometry and PF-B1.
- 0017: PF-F1 is required in addition to triangle geometry and PF-B1.

## Freeze restriction
This contract does not production-freeze PF-F1 or the complete Flag/Pennant rules. Full freeze requires the project's compatibility, no-lookahead, deterministic tests, 2016–2024 historical QA, provenance, and freeze-manifest gates.

2025 remains OOS and must not be used for tuning or operator selection.
