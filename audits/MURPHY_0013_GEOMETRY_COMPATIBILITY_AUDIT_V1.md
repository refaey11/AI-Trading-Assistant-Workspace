# MURPHY_0013 — Geometry Compatibility Audit V1

Date: 2026-08-16
Status: AUDIT COMPLETE / OPERATOR PROPOSAL PENDING APPROVAL
Branch: `audit/murphy-0013-geometry-compat-v1`

## Scope

Audit whether MURPHY_0013 (Symmetrical Triangle) can reuse existing canonical Pivot/Trendline Geometry infrastructure and whether an approved deterministic convergence operator already exists.

## Source / rule record

The authoritative Master KB rule record identifies MURPHY_0013 as a Symmetrical Triangle from Murphy Chapter 6. Required structure:
- at least four reversal points;
- descending upper trendline;
- ascending lower trendline;
- breakout direction observed rather than assumed.

The project Chapter 6 source describes the formation as two converging trendlines meeting at an Apex. The stored project source also records a typical breakout location around 2/3–3/4 of horizontal width, but this is descriptive timing context and is not converted here into a hard eligibility gate.

## Existing canonical infrastructure

The project already has `PIVOT_SEQUENCE_V2` and `TRENDLINE_GEOMETRY_V1`. The 0013–0020 derived-feature contract explicitly requires reuse of these components and prohibits rebuilding Geometry.

The Geometry layer is treated as the source of:
- confirmed reversal points;
- upper/lower boundary identity;
- boundary slope/orientation;
- boundary availability.

## Search result: convergence

No production-frozen PF-G1 convergence/parallelism implementation was found in the accessible GitHub repository.

The existing PF-G1 contract is only a proposal and explicitly states that no numerical convergence/parallelism tolerance is authorized; without an approved deterministic rule it returns `NOT_EVALUABLE`.

Therefore the current evidence is sufficient to identify the two canonical boundaries and their orientations, but **not sufficient to emit a production `CONVERGING` classification**.

## Search result: breakout

A new shared compatibility contract exists in `contracts/MURPHY_0013_0020_PF_B1_SHARED_TWO_CLOSE_COMPATIBILITY_V1.md`.

It reuses the 0008 two-close architecture without copying 0008 Support/Resistance semantics. For 0013 it permits either UP or DOWN breakout testing against the canonical upper/lower pattern boundaries, subject to explicit compatibility gates. The contract remains `COMPATIBILITY CONTRACT / NOT PRODUCTION FROZEN`, so it can be reused as the candidate PF-B1 path but cannot by itself justify a production freeze.

## Compatibility decision

### PASS — reusable upstream components
- PIVOT_SEQUENCE_V2: compatible.
- TRENDLINE_GEOMETRY_V1: compatible.
- Existing PF-B1 two-close architecture: compatible as a candidate shared breakout path, subject to rule-level approval and QA.

### BLOCKED — missing deterministic geometry operator
- PF-G1 `CONVERGING` classification is not yet an approved production operator.
- No numeric tolerance may be invented.
- No historical outcome may be used to choose the convergence operator.
- 2025 remains excluded from all tuning/selection.

## Smallest source-bounded operator proposal

A separate governance proposal may define convergence without a tolerance by using the already-existing canonical line geometry:

1. Require a valid upper boundary and lower boundary with complete provenance.
2. Require upper boundary slope `< 0` and lower boundary slope `> 0`.
3. Compute the mathematical intersection (apex) of the two canonical lines.
4. Require the intersection to occur strictly after the boundary geometry becomes jointly available and to be in the forward time direction.
5. Require the boundary ordering to remain valid at the evaluation timestamp.
6. If any required geometry/availability field is missing or the lines do not have a valid forward intersection, return `NOT_EVALUABLE` rather than inventing a tolerance.

This is an **operationalization proposal only**. It is not claimed to be verbatim Murphy wording and must receive governance approval before implementation as PF-G1.

## 0013 assembly after approval

`PIVOT_SEQUENCE_V2`
→ `TRENDLINE_GEOMETRY_V1`
→ `PF-G1 CONVERGING`
→ `PF-B1 breakout confirmation`
→ `MURPHY_0013 adapter/evaluator`

No directional signal is generated merely because the triangle is symmetrical. Breakout direction remains observed from the confirmed breakout event.

## Historical QA gate

Do not run a production historical PASS/FAIL replay yet. The correct sequence is:
1. approve/close PF-G1 operator;
2. deterministic unit tests;
3. integrate 0013 evaluator;
4. availability/no-lookahead QA;
5. fresh 2016–2024 historical QA;
6. provenance/freeze review;
7. keep 2025 OOS and excluded from tuning/selection.

## Final audit result

**MURPHY_0013 GEOMETRY COMPATIBILITY: PARTIAL / BLOCKED ON PF-G1 OPERATOR APPROVAL.**

No existing canonical component was rebuilt, no threshold was tuned, and no historical result was used to select the geometry definition.
