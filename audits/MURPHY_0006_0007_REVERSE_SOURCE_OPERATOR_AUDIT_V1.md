# Murphy 0006–0007 Reverse Source Operator Audit V1

Date: 2026-08-12
Status: OPERATOR STILL NOT SOURCE-LOCKED

## Scope

Targeted review of the uploaded Murphy Chapter 4 text plus the current project state/handoff artifacts, specifically searching for a deterministic definition of:
- successful touch
- third touch
- reaction/rebound
- line hold / no-break
- confirmation timing

## Source-supported findings

Murphy Chapter 4 supports the qualitative chain:
- trendline uses reaction lows/highs;
- two points establish a tentative line;
- a third successful touch/reaction confirms the trendline;
- the line must hold / remain valid rather than being meaningfully broken.

The project status records the current 0006/0007 semantics as:
- 0006 = LOW family + UP trendline + third test/touch + successful reaction/rebound + line holds + BULLISH.
- 0007 = HIGH family + DOWN trendline + third test/touch + successful reaction/rebound + line holds + BEARISH.

## Break-specific source evidence

Chapter 4 also discusses general trendline-break handling:
- intraday penetration can be false;
- closing beyond the trendline is more important than an intraday penetration;
- price/time filters can be used to confirm a meaningful break;
- examples include a 3% price penetration and a 2-consecutive-day close filter.

These filters are general break filters. No reviewed project artifact establishes an automatic 0006/0007-specific binding of 3% or 2-day logic.

## Reverse-search result

The targeted search did NOT locate a source/project artifact that defines a deterministic touch tolerance, e.g.:
- fixed pip distance;
- fixed percentage distance;
- ATR multiple;
- fixed number of bars for touch;
- fixed reaction magnitude;
- fixed reaction duration.

It also did not locate a project-approved 0006/0007-specific no-break predicate beyond the qualitative line-holds semantics and the separate general Murphy break-filter discussion.

## Consequence

The available sources support candidate evidence generation but do not authorize a deterministic PASS/FAIL operator for `successful third touch + reaction`.

Therefore:
- bar/line intersection may be recorded only as a candidate touch event;
- a third same-type pivot alone is not equivalent to a successful touch;
- subsequent price movement can be recorded as candidate reaction evidence but cannot be converted into PASS without an approved reaction predicate;
- no-break can remain qualitative / NOT_EVALUABLE unless an approved project contract binds a break filter.

## Reuse decision

Reuse existing:
- PIVOT_SEQUENCE_V2
- TRENDLINE_GEOMETRY_V1
- D1/Historical OHLC evidence infrastructure
- existing evaluator/test framework

Do not modify Geometry V1 or invent a touch/reaction threshold to close the gate.

## Current gate

0006 = MAPPING COMPATIBLE / OPERATOR OPEN
0007 = MAPPING COMPATIBLE / OPERATOR OPEN

Next implementation is authorized only for a source-safe evidence/candidate layer. Production evaluator PASS/FAIL remains blocked until the exact operator is source-locked.

2025 remains OOS and is excluded from any implementation selection or tuning.
