# Murphy 0006/0007 — Deep File Library Search V1

Date: 2026-08-13
Status: SEARCH RECORDED / OPERATOR GAP STILL OPEN

## Sources searched
- Current project status / handoff files
- Full Murphy Chapter 4 references available in File Library
- Workspace-related uploaded artifacts
- Rule Adapter contract
- Existing GBPUSD evaluator workspace artifacts
- Historical candidate evidence artifacts

## Findings
1. Project architecture explicitly requires:
   PIVOT_SEQUENCE_V2 -> TRENDLINE_GEOMETRY_V1 -> MURPHY_CONFIRMATION_LAYER -> 0006/0007 EVALUATOR.
2. Existing Pivot and Geometry components must be reused; they must not be rebuilt.
3. Confirmation Layer expected outputs are:
   third_touch_timestamp, third_touch_price, third_touch_detected, reaction_detected, no_break_valid, confirmation_timestamp, confirmation_available_timestamp, rule_id, PASS/FAIL/NOT_EVALUABLE.
4. Current source semantics are closed at qualitative level:
   - 0006: reaction lows -> UP trendline -> two anchors -> third test/touch -> successful reaction/rebound -> line holds without meaningful break -> bullish.
   - 0007: reaction highs -> DOWN trendline -> two anchors -> third test/touch -> successful reaction/rebound -> line holds without meaningful break -> bearish.
5. Murphy discusses general price/time filtering for meaningful trendline breaks, but the project artifacts explicitly prohibit automatically binding the general 3% / 2-day examples to 0006/0007 without an explicit project contract.
6. No authoritative deterministic touch tolerance, reaction threshold, lookback, or 0006/0007-specific no-break operator was found in the searched project materials.
7. The existing evaluator expects upstream facts rather than deriving all three facts itself; therefore the open problem remains the upstream evidence-generation layer.
8. Historical Memory is evidence-only and cannot define Murphy semantics or tune operators.
9. The candidate evidence artifact named 2016-2024 V2 contains out-of-window 2026 rows and must not be treated as the historical source. The corrected 2016-2024 population remains the authoritative QA population for the current checkpoint.

## Important source distinction
The File Library confirms the semantic meaning of third touch / reaction / line hold, but it does not supply a deterministic 0006/0007 operator that can be promoted to production without inventing a missing threshold or filter.

## Current blocker
The exact project-approved upstream predicates for:
- third_touch
- reaction_bounce
- no_break
remain unresolved.

## Next authorized action
Compare the exact TRENDLINE_GEOMETRY_V1 output schema and all existing evaluator/contract fields against the required upstream facts. If an equivalent field/contract already exists, create only a minimal adapter. Otherwise record the exact missing contract and keep production evaluation NOT_EVALUABLE.

## Constraints
- No invented ATR/%/pip tolerance.
- No invented lookback/timeframe.
- No automatic 3%/2-day binding.
- No lookahead.
- No 2025 tuning.
- No replacement Pivot/Geometry implementation.
