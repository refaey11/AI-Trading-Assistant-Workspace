# Murphy 0006–0007 — Source Binding Proposal V1

Date: 2026-08-13
Status: PROPOSAL / NOT YET PRODUCTION-LOCKED

## Purpose

Convert the already-proven raw evidence for rules 0006 and 0007 into the smallest source-backed operator proposal without inventing thresholds or silently changing the rule semantics.

## Source-backed inputs

### 1. Pivot evidence
PIVOT_SEQUENCE_V2 is the active lineage. It specifies two confirming bars and makes pivot evidence available at the pivot event row + 2 bars in the same source timeframe. No lookahead is allowed.

### 2. Trendline geometry
TRENDLINE_GEOMETRY_V1 consumes PIVOT_SEQUENCE_V2, builds lines from consecutive same-type pivots, calculates exact slope, and makes the line available at the later anchor confirmation timestamp. Breakout detection and thresholds are excluded from geometry.

### 3. Original rule semantics
0006: confirmed uptrend line; reaction lows; upward slope; two tentative points; third successful touch and reaction; bullish.
0007: confirmed downtrend line; reaction highs; downward slope; two tentative points; third successful touch and reaction; bearish.

### 4. Murphy Chapter 4 break semantics
Chapter 4 states that two points form a tentative trendline and a third successful touch/reaction confirms the trendline. It also distinguishes intraday penetration from closing breaks and gives general examples of a 3% closing-price penetration filter for major trends, 1% for short-term trends, and a 2-consecutive-daily-close time filter.

These are source-backed general trendline semantics. They are NOT automatically bound to 0006/0007 until a project-level binding is explicitly approved.

## Proposed operator decomposition

### A. Third-touch candidate
For a rule-specific line:
1. candidate pivot must be the same type as the anchor pivots;
2. candidate pivot evidence must be available at its V2 confirmation timestamp;
3. candidate must occur after line availability;
4. existing line-interaction/range-intersection evidence is retained as the raw touch evidence;
5. no invented distance tolerance is introduced.

Status: CANDIDATE / source-compatible, but not yet a final SUCCESSFUL_TOUCH PASS predicate.

### B. Reaction candidate
Use the existing subsequent directional-reaction observation already present in the candidate evidence:
- uptrend rule: reaction direction must be upward/away from the line;
- downtrend rule: reaction direction must be downward/away from the line.

No new reaction magnitude, ATR, pip, lookback, or timeframe threshold is introduced.

Status: CANDIDATE / source-compatible, but not yet a final PASS predicate unless the project accepts the existing reaction operator as the formal definition.

### C. No-break policy
Do NOT choose a policy silently. Preserve the following explicit alternatives for compatibility review:

Option 1 — Murphy price filter: closing price penetration threshold, with source examples of 3% for major trends and 1% for short-term trends.
Option 2 — Murphy time filter: 2 consecutive daily closes beyond the trendline.
Option 3 — combined policy, only if an existing project contract explicitly permits combining them.

Current status: NOT_BOUND.

## Compatibility gate

The proposal is compatible with existing architecture only if:
- it consumes PIVOT_SEQUENCE_V2 rather than rebuilding pivot confirmation;
- it consumes TRENDLINE_GEOMETRY_V1 rather than rebuilding line geometry;
- it uses fields already present in MURPHY_0006_0007_REAL_DATA_CANDIDATE_EVIDENCE_2016_2024_V4.csv;
- it introduces no new unsupported threshold;
- it keeps 2025 completely OOS;
- it does not promote CANDIDATE_ONLY / OBSERVATION_ONLY evidence to production PASS/FAIL until the operator binding is approved.

## Decision required

Before implementation, explicitly select:
1. whether the existing directional reaction observation is the approved reaction operator;
2. which Murphy Chapter 4 no-break policy, if any, is bound to 0006/0007.

Until those decisions are recorded, 0006 and 0007 remain NOT_YET_EVALUABLE.

## Non-goals

- No rebuilding of Pivot V2.
- No rebuilding of Geometry V1.
- No tuning.
- No 2025 usage.
- No invented tolerance, ATR, pip, lookback, or timeframe.
