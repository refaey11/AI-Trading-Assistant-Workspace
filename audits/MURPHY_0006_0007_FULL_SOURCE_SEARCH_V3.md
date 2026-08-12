# Murphy 0006–0007 Full Source Search V3

Date: 2026-08-13
Status: SEARCH COMPLETED / NO NEW DETERMINISTIC OPERATOR FOUND

## Scope
Full cross-source search requested for Murphy 0006/0007 across:
1. uploaded Workspace / File Library artifacts;
2. uploaded Murphy book/source material;
3. GitHub development/provenance mirror;
4. existing project audits/contracts and candidate evidence.

## Workspace / File Library findings

Confirmed:
- Rule Registry contains MURPHY_0006 and MURPHY_0007 with wording: `A third successful touch and reaction confirms the trendline.`
- Current project status records the working mapping 0006 = LOW + UP -> BULLISH and 0007 = HIGH + DOWN -> BEARISH, but earlier source-lock audits explicitly mark the original database record as unrecovered.
- Existing PIVOT_SEQUENCE_V2 and TRENDLINE_GEOMETRY_V1 are canonical and must be reused.
- The V4 candidate evidence dataset is candidate-only and must not be treated as production confirmation.

Search terms included rule_id, primary_source, original_rule, rule_name, setup, conditions, decision, trendline, touch, reaction, confirmed uptrend/downtrend, successful touch, reaction away, meaningful break, breakout, 3%, 2-day, no-break.

No independent original Master Rule Database record with the complete requested fields was recovered.

## Murphy book/source findings

The uploaded Murphy source establishes the qualitative concepts already recorded in the project:
- trendlines are constructed from reaction highs/lows;
- two points establish a tentative trendline;
- additional tests increase significance;
- a third test/reaction supports confirmation;
- meaningful trendline breaks must be distinguished from mere intraday penetration;
- price/time filtering is discussed generally for meaningful breaks.

The source does NOT provide a project-specific numeric 0006/0007 touch tolerance, reaction magnitude/duration, or an explicit binding of the general 3% / 2-consecutive-day examples to these two rule IDs.

Therefore the book supports qualitative semantics, not a complete deterministic project operator.

## GitHub findings

GitHub commit history was searched for 0006/0007 and related source/operator/break terms.
Relevant recorded commits include:
- `1e6cdc2210973c11a88bab52b0c5fe31bc701cce` — Master Rule Database search; original record not recovered.
- `9b29e5fb85fe160abad6276e399c470feee239fc` — final compatibility audit; no approved 0006/0007-specific deterministic break/no-break contract and no deterministic touch/reaction operator found.
- `8dc09a3691a0ca1d8a9317c09c8bc4480affcd4f` — reverse source audit for touch/reaction operator.
- `51b089ffa66a490099e5dd7d93d889140acdbe39` — direct Geometry/Pivot compatibility findings.
- `49efa8727c693274249455a7dcd9370936ee47a0` — source-safe evidence adapter.
- `3a983323bb148543b482a740d7e8f058d3bf7e92` — evidence adapter tests.

No GitHub source file supersedes the Workspace/Rule Registry provenance with a deterministic 0006/0007 touch/reaction/no-break contract.

## Final conclusion

No new authoritative deterministic operator was found.

Source-backed qualitative operator remains:
- 0006: LOW reaction family -> UP trendline -> third test/touch -> successful reaction/rebound -> line holds -> bullish context.
- 0007: HIGH reaction family -> DOWN trendline -> third test/touch -> successful reaction/rebound -> line holds -> bearish context.

Still NOT source-locked:
- exact touch predicate/tolerance;
- exact reaction predicate/magnitude/duration;
- exact no-break predicate for these rule IDs;
- production confirmation timestamp based on those predicates.

## Decision

Do not invent ATR, pip, percentage, lookback, timeframe, reaction magnitude, or automatic 3%/2-day binding.

The existing candidate-only evidence layer is the maximum source-safe implementation at this point. Production 0006/0007 remains `NOT_YET_EVALUABLE` until an authoritative deterministic operator contract is recovered.

2025 remains OOS and is excluded from selection/tuning.
