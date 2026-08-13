# Murphy 0006–0007 Confirmation Source Binding V1

Date: 2026-08-13
Status: PARTIAL SOURCE BINDING / NO PRODUCTION PROMOTION

## Direct source record
The original project records recovered from the uploaded archives state:
- MURPHY_0006 = Confirmed uptrend line; successive reaction lows; upward slope; two points tentative; third successful touch and reaction; confirmation field empty; status incomplete.
- MURPHY_0007 = Confirmed downtrend line; successive reaction highs; downward slope; two points tentative; third successful touch and reaction; confirmation field empty; status incomplete.

## Murphy Chapter 4 integrated source
The Chapter 4 integrated knowledge artifact states:
- Up trendline connects successive reaction lows.
- Down trendline connects successive reaction highs.
- Two points form a tentative line.
- A confirmed trendline requires a third successful touch and reaction without breaking.
- Trendline importance increases with successful test frequency.
- Trendlines should enclose the entire daily price range (High to Low).
- Intraday penetration is distinguished from a closing break.
- General price/time break filters are discussed: 3% closing penetration for major trends / 1% for short-term, and a 2-consecutive-daily-close time filter.

## Source-safe binding that can be stated now
The following are source-backed semantics, not yet production operators:
1. Third-touch candidate must occur after the two-anchor line is available.
2. Candidate must belong to the correct reaction family (LOW for 0006, HIGH for 0007).
3. The daily range intersection field already present in the candidate evidence is directly aligned with the source statement that the trendline should enclose the entire daily price range.
4. A subsequent directionally consistent opposite-family reaction candidate can be retained as reaction evidence.

## What is still NOT source-locked
The source does not explicitly specify, for 0006/0007:
- whether a third touch must be a confirmed pivot versus any bar interaction;
- whether the line intersection itself is sufficient to call a touch;
- a numeric tolerance around the line;
- a minimum reaction magnitude/distance;
- which break filter (3% or 2-day) must be selected for these rules.

Therefore the existing candidate fields may be used as evidence, but must not be promoted to deterministic PASS/FAIL without an explicit project contract for these choices.

## Critical conclusion
We can now close more of the semantic-to-feature mapping, but NOT the final production confirmation operator.

The smallest safe implementation remains:
- preserve the existing Evidence Adapter;
- preserve existing Geometry and Pivot components;
- expose source-aligned candidate evidence;
- keep `third_touch`, `reaction_bounce`, and `no_break_valid` as NOT_EVALUABLE at production level until the missing operator choices are source-locked.

## No invented parameters
Do not invent ATR, pip, percentage, lookback, timeframe, reaction threshold, or automatic 3%/2-day binding.
2025 remains OOS.
