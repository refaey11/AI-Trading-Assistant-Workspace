# Murphy 0006–0007 Book Operator Clarification V2
Date: 2026-08-12

## Source reviewed
Uploaded full Chapter 4: `الفصل الرابع مورفي (1).txt`

## Source-backed operator semantics
Chapter 4 gives the following operational sequence for trendlines:

### Uptrend line / 0006
- An uptrend line is drawn upward/right along reaction lows.
- At least two suitable lows are required to draw the line.
- The third test/touch is the confirming test of trendline validity.
- The successful third test is described as price rebounding away from the line without breaking it.
- After confirmation, if the trend continues in its original direction, the line is considered valid/useful.

### Downtrend line / 0007
- A downtrend line is drawn downward/right along reaction highs.
- Two points form the temporary line.
- A third test confirms validity under the analogous rule.
- The successful test requires the line to hold rather than be broken.

## Break interpretation in the same chapter
The chapter explicitly distinguishes an intraday penetration from a meaningful trendline break and states that a close behind the trendline is more important than a mere intraday break. It then presents price/time filters (including examples such as a 3% price rule and a 2-consecutive-day closing rule) as ways analysts may filter breakouts.

## Important boundary
The chapter therefore DOES provide source evidence for the qualitative `no_break` condition required by 0006/0007. This corrects the earlier overstatement that the source did not define no-break at all.

However, the chapter does NOT assign one specific numeric breakout filter to Murphy rules 0006/0007. The 3%/2-day examples are discussed as general trendline-break filters and are not automatically the touch/reaction threshold for these two rules.

## Current evaluator implication
The source-defined third-test operator can be expressed without inventing a new numeric touch tolerance:

1. valid trendline exists from the existing geometry layer;
2. third test/touch occurs;
3. third test is successful and price rebounds away from the line;
4. no meaningful break has occurred according to the project's approved trendline-break contract;
5. event is only usable at the confirmation availability timestamp.

The remaining implementation question is therefore narrower than before:
**which existing project contract/field defines the actual trendline-break filter and the event availability for the third test?**

Do NOT add a new tolerance/ATR threshold/percentage/2-day rule for 0006/0007 unless an existing project contract explicitly binds that filter to these rules.

## Status
**0006–0007 source semantics: RESOLVED**
**No-break semantics: RESOLVED QUALITATIVELY BY SOURCE**
**Exact project-bound operational break field: COMPATIBILITY PENDING**
**Production Freeze: NOT YET**

## Controls
- Reuse existing Trendline Geometry V1.
- Reuse existing breakout/filter contract if it is already the project-standard operator.
- No new threshold or timeframe invented.
- 2025 remains OOS and untouched.
