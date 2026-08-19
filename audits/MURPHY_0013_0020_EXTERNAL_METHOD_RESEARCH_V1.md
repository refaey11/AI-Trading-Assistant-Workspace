# Murphy 0013–0020 — External Method Research V1

## Purpose
Evaluate external open-source/technical methods for the four shared primitives blocking Rules 0013–0020. External material is corroboration only; Murphy source semantics and existing project contracts remain authoritative.

## Sources reviewed
- TradingPatternScanner — identifies horizontal S/R, ascending/descending triangles, wedges, channels and uses pattern-specific detection. External reference: GitHub `white07S/TradingPatternScanner`.
- stolgo — deterministic price-action vocabulary for support/resistance, swing/pivot levels, crosses_above/crosses_below, consolidation and breakout; explicitly documents no-lookahead context handling. External reference: GitHub `stockalgo/stolgo`.
- pytrendline — pivot-based trendline construction, minimum points, allowable error and breakout handling. External reference: GitHub `ednunezg/pytrendline`.
- Algorithmic-Support-and-Resistance — reversal-point/zigzag based S/R grouping. External reference: GitHub `BatuhanUsluel/Algorithmic-Support-and-Resistance`.
- chart_patterns — algorithmic detection of triangles, flags and pennants. External reference: GitHub `zeta-zetra/chart_patterns`.
- MQL5 structural breakout research — uses swing structure and confirmed crossing rather than mere wick intrusion; three-swing validation is presented as a structural safeguard.

## Compatibility findings
### PF-H1
External projects commonly represent S/R from confirmed pivots or reversal points. This supports reusing the project's Pivot Sequence V2 rather than inventing a new detector. External sources do NOT authorize a Murphy-specific numeric tolerance.

### PF-G1
External pattern engines commonly construct upper/lower trendlines from pivots and classify converging geometry. This supports the existing TRENDLINE_GEOMETRY_V1 direction, but no external tolerance should be imported into the Murphy contract.

### PF-B1
External systems commonly require a completed-bar close/cross of the boundary and often add a separate significance/confirmation filter. This supports the project's availability/no-lookahead design. It does NOT authorize importing ATR, percentage, volume, or two-bar thresholds into Murphy.

### PF-F1
External flag detectors generally relate the flag to a prior directional pole and then evaluate the consolidation/flag geometry. This supports the project's reuse of existing flagpole/pivot components. It does NOT define Murphy's exact meaning of “sharp” and therefore cannot supply that missing contract by itself.

## Decision
External research materially reduces implementation uncertainty but does not provide a source-authorized replacement for the four missing production contracts. Therefore:

1. Reuse existing project Pivot Sequence V2 and TRENDLINE_GEOMETRY_V1.
2. Do not import external thresholds.
3. Define the shared primitives as deterministic wrappers around existing project components, with `NOT_EVALUABLE` when required evidence is unavailable/ambiguous.
4. Run deterministic tests and 2016–2024 QA only after the wrappers are source-compatible.
5. Keep 2025 OOS and unavailable for tuning.

## Important boundary
This document is a research/compatibility artifact. It is NOT a production freeze record and does not change any Murphy rule status by itself.
