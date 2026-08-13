# Murphy 0006–0007 Original Record Recovery V2

Date: 2026-08-13
Status: RECORD RECOVERED / OPERATIONAL CONTRACT STILL OPEN

## Direct archive inspection
The uploaded project archives were inspected directly at ZIP-content level, not only through File Library snippets.

Archives checked:
- AI_Trading_Assistant_MASTER_KB_V1.zip
- AI_Trading_Assistant_TRADING_RULES_V2.zip
- AI_Trading_Assistant_3_BOOK_INTEGRATION_V1.zip
- GBPUSD_RULE_EVALUATOR_V2_WORKSPACE_RECONSTRUCTED_V2.zip
- additional Murphy workspace audit archives

## Recovered rule records
### MASTER_KB
`02_Trading_Rules/MASTER_CANDIDATE_RULES_V1.json`
contains MURPHY_0006 and MURPHY_0007.

### TRADING_RULES_V2
`02_Trading_Rules_V2/MASTER_TRADING_RULES_V2.json`
contains both records.

Both records are explicitly:
- `MURPHY_0006`: `INCOMPLETE_NEEDS_RULE_DEFINITION`
- `MURPHY_0007`: `INCOMPLETE_NEEDS_RULE_DEFINITION`

Both have:
- source book: Technical Analysis of the Financial Markets
- author: John J. Murphy
- chapter: 4
- section: Trendlines
- 0006 name: Confirmed uptrend line
- 0007 name: Confirmed downtrend line
- 0006 direction: BULLISH
- 0007 direction: BEARISH
- 0006: successive reaction lows + upward slope + two tentative points + third successful touch and reaction
- 0007: successive reaction highs + downward slope + two tentative points + third successful touch and reaction
- `confirmation` field is empty for both
- `missing_fields = ["confirmation"]`

### 3-BOOK INTEGRATION
`03_Rule_Registry/INTEGRATED_RULE_REGISTRY_V1.json` contains the same original_rule payload for both records, but sets:
- `primary_source = UNATTRIBUTED`
- `integration_role = needs_source_review`

This is not a source-locked production record; it is an integrated candidate registry record.

### GBPUSD evaluator workspace
`MURPHY_0006_TO_0010_EXACT_MAPPING_V1.csv` confirms:
- 0006 third-touch/reaction row = `NOT_YET_EVALUABLE`
- 0007 third-touch/reaction row = `NOT_YET_EVALUABLE`
- reason: successful touch and reaction needs an approved operational definition.

## Important correction to prior conclusion
The original rule records WERE recoverable from the uploaded archives. Therefore the earlier statement that the original records could not be found should not be repeated.

However, recovery does NOT close the operator gate. The recovered records themselves explicitly leave `confirmation` empty and mark both rules incomplete.

## Operational implication
The source-lock question is now split cleanly:
1. Rule identity / semantic mapping = recovered.
2. Exact deterministic confirmation operator = still missing.

No new threshold or operator is authorized by these records.

## Next exact action
Audit the recovered `confirmation` gap against:
- Murphy Chapter 4 source text
- existing Geometry V1 output
- existing break/no-break contracts
- any other project artifact that may supply an already-approved confirmation operator.

Do not invent a touch tolerance, reaction magnitude, lookback, ATR, percentage, pip rule, or automatic 3%/2-day binding.

2025 remains OOS.
