# Murphy 0006–0007 Confirmation Layer Compatibility Audit V2

Date: 2026-08-13
Status: COMPATIBLE / OPERATIONAL GATE PARTIALLY OPEN

## Confirmed source semantics

MURPHY_0006:
- reaction LOW family
- UP trendline
- two anchors
- third test/touch
- successful reaction/rebound
- line holds without meaningful break
- bullish context

MURPHY_0007:
- reaction HIGH family
- DOWN trendline
- two anchors
- third test/touch
- successful reaction/rebound
- line holds without meaningful break
- bearish context

The exact mapping artifact also describes the qualitative operator as `third touch followed by reaction away from line`.

## Existing components to reuse

- PIVOT_SEQUENCE_V2
- TRENDLINE_GEOMETRY_V1
- existing Evidence Adapter
- existing Murphy Confirmation Evidence Layer
- existing Confirmation Dataset Builder

No replacement Geometry or Pivot component is authorized.

## Availability / no-lookahead

PIVOT_SEQUENCE_V2 has an explicit two-confirming-bar availability rule. TRENDLINE_GEOMETRY_V1 line availability is based on the later availability of the two defining pivots. These contracts are compatible with the Confirmation Layer and provide the chronology foundation.

## Break/no-break audit

No existing approved 0006/0007-specific deterministic break/no-break contract was recovered in GitHub search. Geometry V1 explicitly excludes breakout detection. Murphy source provides qualitative meaningful-break semantics, but the project does not bind the general 3% or 2-consecutive-day examples to these rules.

Therefore raw post-touch line-interaction observations may be recorded, but production `no_break_valid` cannot be promoted to PASS/FAIL without an approved deterministic operator.

## Touch/reaction audit

The project proves the qualitative requirement: third touch followed by reaction away from the line. It does not provide an approved numeric predicate for what counts as a successful touch or the minimum reaction magnitude/lookback.

Therefore the existing Confirmation Layer may produce candidate evidence, but must not label a candidate as confirmed merely because a pivot of the opposite type exists.

## Historical artifact correction

The File Library artifact named `MURPHY_0006_0007_REAL_DATA_CANDIDATE_EVIDENCE_2016_2024_V2.csv` is stale/mislabeled: retrieved rows include 2025 and 2026 timestamps. It is rejected for historical QA, scoring, tuning, and freeze decisions.

The previously recorded corrected population is:
- 0006 = 166
- 0007 = 181
- total = 347
- in-window reaction candidates = 346

Its intended SHA-256 is:
`7739a55aba0a61b26ac25849135d147f153a637a55db08801701b41134e85303`

The canonical corrected CSV must be regenerated and rechecked before official historical QA.

## Compatibility matrix

| Requirement | Result |
|---|---|
| LOW/HIGH line family | PASS |
| UP/DOWN direction | PASS |
| two anchors | PASS |
| line availability | PASS |
| pivot no-lookahead | PASS |
| third-touch concept | QUALITATIVELY SUPPORTED |
| reaction-away concept | QUALITATIVELY SUPPORTED |
| deterministic touch operator | OPEN |
| deterministic reaction operator | OPEN |
| 0006/0007 no-break operator | OPEN |
| production confirmation timestamp | BLOCKED |
| 2025 exclusion | PASS |

## Gate decision

MURPHY_0006/0007 remain `NOT_YET_EVALUABLE` for production.

The next implementation is NOT a new Geometry system. It is only the smallest candidate-evidence adapter over the existing Pivot/Geometry contracts, followed by deterministic tests. No candidate evidence may be promoted to production PASS/FAIL until the missing operators are source-locked.
