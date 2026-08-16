# Murphy Shared Primitives — Solution Pass V1

Status: ENGINEERING CANDIDATE / NOT PRODUCTION FROZEN
Date: 2026-08-16

## Purpose
Close the first shared blockers for Murphy 0013–0020 without rebuilding canonical Pivot/Geometry/Volume components and without assigning engineering thresholds to Murphy.

## Source / project findings
The project source reconciliation identifies four shared blockers: horizontal level, boundary relationship, breakout confirmation, and flagpole relation. Existing material explicitly says these are not production-frozen and that no numerical tolerances may be invented. The same records require reuse of PIVOT_SEQUENCE_V2, TRENDLINE_GEOMETRY_V1 and VOLUME_CONFIRMATION_V2.

## External engineering research
Recent public implementations commonly use confirmed pivots, fitted trendlines, mathematical future-intersection/apex tests for convergence, containment checks, and closed-bar breakout confirmation. Other implementations use ATR/percentage tolerances for robustness, but those parameters are engineering choices and therefore are NOT imported into Murphy. Sources reviewed include TradingView triangle implementations and MQL5 pattern-detection articles. These are engineering references only, not Murphy source authority.

## Solution A — PF-H1 Horizontal Level

### Candidate contract
Use the existing confirmed pivot / geometry pipeline. A boundary is `HORIZONTAL_EXACT` only when its canonical geometry slope is exactly zero under the existing geometry representation. No price-cluster tolerance is introduced.

Outputs:
- level_id
- level_price
- role SUPPORT|RESISTANCE
- availability_timestamp
- status AVAILABLE|NOT_EVALUABLE

### Why
This is the smallest deterministic interpretation of the word horizontal that introduces no arbitrary percentage/ATR/pip tolerance. It is conservative: near-horizontal levels remain NOT_EVALUABLE until a separate engineering tolerance is explicitly approved.

### Consequence
0014/0015/0020 can receive a deterministic structural horizontal-level result for exact-horizontal cases. This does not claim that Murphy requires mathematical exactness; it is an engineering conservative mode.

## Solution B — PF-G1 Boundary Relationship

### Candidate contract
For two existing TRENDLINE_GEOMETRY_V1 boundaries:

1. `CONVERGING` if their mathematical intersection exists strictly after the current evaluation timestamp and the boundaries are moving toward that intersection.
2. `PARALLEL_EXACT` if their slopes are exactly equal and the lines do not intersect.
3. `NOT_EVALUABLE` otherwise.

No convergence-angle, ATR, percentage, or slope-difference threshold is introduced.

### Why
A future mathematical intersection is a deterministic geometric fact. Public engineering implementations also use future apex/intersection as a core convergence test, although many add tunable thresholds; those thresholds are deliberately excluded here.

### Consequence
0013/0018/0019 can obtain a conservative convergence result. 0016/0020 can obtain only exact-parallel results; approximate parallelism remains NOT_EVALUABLE pending governance.

## Solution C — PF-B1 Breakout Event vs Decisive Break

Split the contract into two states instead of forcing a threshold:

1. `RAW_BOUNDARY_CROSS`
   - first completed-bar close beyond an already-available boundary.
   - deterministic and no-lookahead.
2. `DECISIVE_BREAK_CONFIRMED`
   - only emitted when an explicitly approved breakout policy is supplied.

Policy families remain:
- PRICE_FILTER
- TIME_FILTER

Murphy's general 1–3% examples and two-day example are NOT selected as the project-wide policy. If no policy is supplied, decisive confirmation remains `NOT_EVALUABLE`.

### Why
This lets the Factory build and test the structural breakout event now without pretending that a raw close beyond a line is automatically Murphy's "significant/decisive" break.

## Solution D — PF-F1 Flagpole Relation

### Candidate contract
Separate the source requirement into:
- preceding directional move exists;
- direction agrees with the continuation context;
- pole ends before formation starts;
- volume context is exposed separately through existing VOLUME_CONFIRMATION_V2 where compatible.

Do NOT encode the adjective `sharp` as a new numeric threshold in V1.

Status:
- `AVAILABLE` when the preceding directional relation can be established from existing canonical evidence;
- `NOT_EVALUABLE` for the unresolved sharpness component.

### Why
This closes the chronology and direction portion without silently converting "sharp" into ATR/percentage/length rules. Public flag detectors commonly add ATR-normalized pole thresholds, but those are engineering choices and are intentionally not imported into Murphy.

## Rule impact

### Can now progress structurally
- 0013: pivots + geometry + convergence + raw breakout event.
- 0014: pivots + geometry + exact-horizontal resistance + raw breakout event.
- 0015: pivots + geometry + exact-horizontal support + raw breakout event.
- 0018: boundaries + convergence + raw breakout event.
- 0019: boundaries + convergence + raw breakout event.
- 0020: exact-horizontal range + exact-parallel relationship + raw breakout event.

### Remains partially blocked
- 0016: unresolved sharpness and approximate-parallel channel semantics.
- 0017: unresolved sharpness; triangle geometry can reuse 0013 path.
- Any rule requiring a decisive/significant breakout rather than a raw boundary cross remains gated by PF-B1 policy approval.

## Required tests
For every primitive:
1. positive deterministic case
2. invalid geometry case
3. insufficient evidence case
4. availability/no-lookahead case
5. missing-data case

## Historical QA
After implementation:
- run 2016–2024 QA;
- reconcile provenance and event timestamps;
- perform leakage/no-lookahead audit;
- do not use 2025 for tuning or operator selection.

## Governance boundary
These are Engineering Candidate contracts. They do not rewrite Murphy source semantics and are not attributed to Murphy. Production freeze requires explicit approval, deterministic tests, historical QA, availability/leakage audit, and provenance/freeze manifest.

## Research references
- TradingView triangle implementation: future apex/intersection and containment are used as objective geometry checks; configurable tolerances are implementation-specific.
- MQL5 wedge implementation: slope comparison and future apex are used to classify converging wedges.
- MQL5 flag implementation: quantitative pole/channel/breakout filters are used by some engineering implementations; those numeric filters are intentionally not imported here.

External research is engineering context only. Project source remains authoritative for Murphy semantics.
