# Murphy 0006–0007 Compatibility Audit V1

Date: 2026-08-12
Status: PARTIALLY COMPATIBLE / OPERATIONALIZATION BLOCKED

## Scope
Compatibility audit only. No threshold invention, no tuning, no evaluator implementation from guessed semantics, and no use of 2025 for tuning/selection.

## Authoritative rule semantics

- MURPHY_0006: reaction LOW family -> upward trendline -> two anchors -> third test/touch -> successful reaction/rebound -> line holds without meaningful break -> BULLISH.
- MURPHY_0007: reaction HIGH family -> downward trendline -> two anchors -> third test/touch -> successful reaction/rebound -> line holds without meaningful break -> BEARISH.

The qualitative source semantics are now resolved. The remaining blocker is deterministic operationalization of touch, reaction, and no-break.

## Existing upstream components inspected

### PIVOT_SEQUENCE_V2
Available and is the required source of confirmed pivots. Pivot availability is preserved and must be respected for chronology/no-lookahead.

### TRENDLINE_GEOMETRY_V1
Existing built derived feature. It MUST be reused; it must not be rebuilt.

Recovered contract:
- input: PIVOT_SEQUENCE_V2
- line generation: consecutive pivots of the same type only
- slope: exact price change / elapsed seconds
- line availability: later confirmation timestamp of the two defining pivots
- breakout detection: explicitly excluded
- pattern classification: excluded
- no added thresholds
- line cannot be available before both defining pivots are confirmed

Recovered output fields:
`line_id, line_type, point_1_timestamp, point_1_price, point_2_timestamp, point_2_price, slope_price_per_second, direction, availability_timestamp, point_1_availability, point_2_availability, source_file`

Recovered QA artifact confirms slope, availability, chronology, type, and no-2025 checks are passing for the stored trendline files.

## Compatibility matrix

| Requirement | Existing evidence | Result |
|---|---|---|
| 2-point LOW/HIGH line anchors | TRENDLINE_GEOMETRY_V1 | COMPATIBLE |
| UP/DOWN direction | exact slope sign in Geometry | COMPATIBLE |
| line_id | Geometry output | COMPATIBLE |
| anchor timestamps/prices | Geometry output | COMPATIBLE |
| line availability | later pivot availability | COMPATIBLE |
| confirmed pivot lineage | PIVOT_SEQUENCE_V2 | COMPATIBLE |
| third-touch detection | no approved operator found | BLOCKED |
| successful reaction detection | no approved operator found | BLOCKED |
| no-break / line-holds semantics | Geometry explicitly excludes breakout detection; no approved 0006/0007 contract found | BLOCKED |
| confirmation timestamp | depends on reaction/no-break operator | BLOCKED |
| 2025 exclusion | Geometry QA has no-2025 control; no tuning allowed | COMPATIBLE |

## Critical finding

The previous source-status blocker is narrower than originally recorded: TRENDLINE_GEOMETRY_V1 is not missing. It is present as a built derived feature with validated chronology/availability fields.

However, TRENDLINE_GEOMETRY_V1 intentionally does not implement breakout detection and does not define a touch tolerance, minimum-touch threshold, reaction threshold, or no-break rule. Therefore it cannot by itself produce a deterministic PASS for 0006/0007.

## Prohibited inference

Do NOT introduce:
- 3% break rules
- 2-day break rules
- ATR tolerance
- percentage/pip tolerance
- fixed lookback
- fixed timeframe
- inferred reaction magnitude

unless an authoritative project/source contract is recovered that explicitly binds such an operator to 0006/0007.

## Gate decision

MURPHY_0006–0007 are **not yet evaluable for production**.

The existing Geometry layer is compatible and should be reused. The smallest missing layer is a Murphy Confirmation Layer / adapter that can consume Geometry + completed-bar/pivot evidence, but it must remain NOT_EVALUABLE until the project-approved deterministic definitions of successful touch, reaction, and no-break are recovered.

## Next action

Search the full project/workspace for an existing approved touch/reaction/break contract. If none exists, do not invent one. Record the unresolved operator explicitly and keep 0006/0007 blocked rather than forcing an evaluator.
