# Murphy 0006–0007 Confirmation Layer Compatibility Audit V2

Date: 2026-08-12
Status: PARTIALLY COMPATIBLE / EVALUATOR STILL BLOCKED

## Scope

Audit the existing Murphy 0006/0007 Confirmation Layer against the full GBPUSD Rule Evaluator V2 workspace, existing contracts, Historical Memory role, and the Murphy exact mapping artifacts. No threshold invention, no tuning, and no use of 2025 for implementation selection.

## New evidence recovered from the full GBPUSD Rule Evaluator V2 workspace

### 1. Exact rule mapping already contains the source-backed qualitative operator

`MURPHY_0006_TO_0010_EXACT_MAPPING_V1.csv` records:

- MURPHY_0006: Connect successive reaction lows with an upward-sloping line.
- MURPHY_0006: Two points create a tentative line.
- MURPHY_0006: A third successful touch and reaction confirms the trendline.
- MURPHY_0007: Connect successive reaction highs with a downward-sloping line.
- MURPHY_0007: Two points create a tentative line.
- MURPHY_0007: A third successful touch and reaction confirms the trendline.

The mapping artifact further describes the intended operator qualitatively as:
`third touch followed by reaction away from line`.

The same rows remain explicitly `NOT_YET_EVALUABLE` because "successful touch and reaction" still lacks an approved deterministic operational definition.

### 2. Trendline Geometry V1 is fully built and validated

Existing `TRENDLINE_GEOMETRY_V1_OUTPUT` contains the trendline outputs and QA artifacts.

Recovered build contract:
- input = PIVOT_SEQUENCE_V2
- consecutive same-type pivots only
- exact slope from price change / elapsed seconds
- line availability = later availability of defining pivots
- pattern classification excluded
- breakout detection excluded
- no thresholds added
- no 2025 used
- no-lookahead enforced for line availability

Required output fields include line_id, line_type, anchor timestamps/prices, slope, direction, availability timestamp, and anchor availability timestamps.

### 3. PIVOT_SEQUENCE_V2 provides an availability contract

Recovered `PIVOT_SEQUENCE_V2_OUTPUT/PIVOT_SEQUENCE_CONTRACT_V2.json` states:
- status = BUILT_DERIVED_FEATURE
- source = existing Market Structure artifacts
- pivot_high / pivot_low are event flags
- confirmation rule = 2 confirming bars
- availability timestamp = pivot event row + 2 bars in the same source timeframe
- pivot evidence is unavailable before its two-bar confirmation timestamp
- no 2025 used

This resolves an earlier uncertainty: the current V2 pivot lineage does contain an explicit availability/no-lookahead rule.

### 4. Historical Memory remains evidence-only

`HISTORICAL_CONTEXT_MEMORY_V1/CONTRACT.json` states:
- purpose = historical context memory for Market Reader
- not_a_strategy = true
- outcomes_attached = false

`HISTORICAL_OUTCOME_MEMORY_V1` contains descriptive forward-return statistics, not trade rules. These artifacts cannot define Murphy touch/reaction semantics or choose direction.

## Compatibility matrix

| Requirement | Existing evidence | Result |
|---|---|---|
| LOW/HIGH line family | exact mapping + Geometry V1 | COMPATIBLE |
| UP/DOWN direction | exact mapping + Geometry slope sign | COMPATIBLE |
| 2 anchors | Geometry V1 | COMPATIBLE |
| line availability | Geometry V1 + Pivot Sequence V2 | COMPATIBLE |
| pivot no-lookahead | Pivot Sequence V2 | COMPATIBLE |
| third touch concept | exact mapping + Murphy source | QUALITATIVELY SUPPORTED |
| reaction after third touch | exact mapping says reaction away from line | QUALITATIVELY SUPPORTED |
| deterministic touch operator | no approved project operator | BLOCKED |
| deterministic reaction operator | no approved project operator | BLOCKED |
| deterministic no-break binding for 0006/0007 | Geometry excludes breakout; no rule-specific binding found | BLOCKED |
| confirmation timestamp | depends on deterministic touch/reaction/no-break | BLOCKED |
| 2025 exclusion | contracts/QA controls | COMPATIBLE |

## Important distinction

The full workspace now proves that the project already had a qualitative operator description for 0006/0007: `third touch followed by reaction away from line`. This is stronger than the earlier generic registry wording alone.

However, the workspace still explicitly marks the rows `NOT_YET_EVALUABLE` because the words "successful touch" and "reaction away from line" are not converted into a project-approved deterministic predicate.

## Reuse decision

Reuse:
- PIVOT_SEQUENCE_V2
- TRENDLINE_GEOMETRY_V1
- existing evaluator/test infrastructure
- Historical Memory only as historical evidence/QA

Do not rebuild Geometry or Pivot Sequence.

## Prohibited inference

Do not add:
- ATR tolerance
- percentage touch tolerance
- pip tolerance
- fixed lookback
- fixed timeframe
- automatic 3% binding
- automatic 2-day binding
- inferred reaction magnitude

The Murphy 3%/2-day filters are general trendline-break material and are not proven here as a 0006/0007-specific contract.

## Gate decision

MURPHY_0006–0007 remain `NOT_YET_EVALUABLE` for production.

The exact next missing artifact is a project-approved deterministic operator specification for:
1. third touch
2. reaction away from line
3. no-break / line holds

Once that operator is source-locked, the implementation should be the smallest Confirmation Layer adapter over the existing Geometry + Pivot V2 outputs, followed by unit tests and 2016–2024 historical QA.
