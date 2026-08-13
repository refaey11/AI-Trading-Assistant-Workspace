# Murphy 0006–0007 Compatibility Audit V2

Date: 2026-08-13
Status: COMPATIBLE ARCHITECTURE / UPSTREAM OPERATOR GAPS OPEN

## Important correction to the earlier V1 framing

The project already contains a reusable Murphy 0006/0007 trendline confirmation evaluator in the Workspace lineage. The evaluator consumes upstream facts rather than deriving them:
- third_touch
- reaction_bounce
- no_break
- confirmation_available_timestamp

Therefore the missing production work is NOT a replacement evaluator. The missing work is the upstream deterministic evidence contract that supplies those facts.

## Compatibility chain

PIVOT_SEQUENCE_V2
→ TRENDLINE_GEOMETRY_V1
→ upstream third_touch / reaction_bounce / no_break evidence
→ existing Murphy 0006/0007 evaluator
→ PASS / FAIL / NOT_EVALUABLE

### PIVOT_SEQUENCE_V2
Compatible and reusable.
- two confirming bars;
- availability at pivot event row + 2 bars;
- no lookahead;
- 2025 excluded.

### TRENDLINE_GEOMETRY_V1
Compatible and reusable.
- consecutive same-type pivot anchors;
- exact slope;
- direction and line availability;
- does not implement breakout detection or confirmation.

### Existing candidate evidence
`MURPHY_0006_0007_REAL_DATA_CANDIDATE_EVIDENCE_2016_2024_V4.csv`
- 166 rows for 0006;
- 181 rows for 0007;
- 347 total;
- 23-column schema;
- 2016–2024 only;
- mapping checks pass;
- unique candidate keys;
- candidate status only;
- no-break remains observation-only;
- exact zero-distance contacts = 0.

Candidate QA is PASS, but it is explicitly not production confirmation.

## Existing evaluator compatibility

The evaluator contract expects the following upstream facts:
- `third_touch`
- `reaction_bounce`
- `no_break`
- `confirmation_available_timestamp`

The existing evaluator should be reused. Do not create a second evaluator that duplicates its rule-level decision logic.

## Upstream operator audit

### Third touch — OPEN
Geometry provides anchors, direction, line price, and availability. Candidate evidence provides candidate pivots and line interaction observations. However, no source/project-locked tolerance or deterministic successful-touch predicate was recovered.

Do not use exact collinearity as a touch definition. The geometry audit found exact collinear triples only as diagnostics and explicitly prohibits promoting that diagnostic to the operator.

### Reaction bounce — OPEN
Candidate evidence includes a subsequent reaction candidate and a directional-consistency observation. This is useful source-compatible evidence, but the production definition of a successful reaction/rebound has not been contractually locked with a deterministic operator.

Do not invent reaction magnitude, ATR, pip, percentage, lookback, or timeframe thresholds.

### No-break — OPEN
GitHub/source searches did not recover an approved 0006/0007-specific executable break predicate. `break_structure_up/down` is only a provenance/reference concept for adjacent rules, not a valid 0006/0007 operator.

Murphy Chapter 4 provides qualitative no-break semantics and general price/time filter examples, but the project has not explicitly bound 3% or 2-consecutive-day filtering to 0006/0007. Do not silently bind them.

## Historical Memory compatibility

Historical Memory / Similarity remains evidence-only. It cannot define Murphy semantics, select the missing operator, or tune thresholds. It may be used later for historical QA after the deterministic rule contract is closed.

## Decision

Architecture is compatible. Existing components are reusable. Candidate QA is complete. The remaining production blocker is precisely the upstream operator contract:

1. deterministic third-touch predicate;
2. deterministic reaction/rebound predicate;
3. deterministic no-break predicate.

Until those are source/project-locked, the existing evaluator must remain `NOT_YET_EVALUABLE` for production.

## Authorized next action

Inspect the exact existing evaluator contract and the full Trendline Geometry V1 field/schema artifacts side-by-side. If an authoritative equivalent field already exists for any upstream fact, create only the smallest adapter and tests. If no authoritative equivalent exists, record the missing contract and do not invent it.

## Constraints

- Do not rebuild Pivot V2.
- Do not rebuild Geometry V1.
- Do not replace the existing evaluator.
- Do not promote candidate evidence to PASS/FAIL.
- Do not invent thresholds/tolerances/lookbacks/timeframes.
- Do not bind 3% or 2-day automatically.
- Do not use 2025 for tuning or implementation selection.
