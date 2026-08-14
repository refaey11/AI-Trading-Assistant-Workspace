# Murphy 0008 PF-B1 — Real PIVOT_SEQUENCE_V2 Integration Audit V1

Status: INTEGRATION PASS / GOVERNANCE CANDIDATE — NOT PRODUCTION FROZEN
Date: 2026-08-15
Branch: audit/murphy-0008-pf-b1-v1

## Scope
Run the current PF-B1 operationalization candidate against the real canonical PIVOT_SEQUENCE_V2 output and the project's real GBPUSD H1 2016–2024 OHLC evidence available in the workspace snapshot.

## Canonical upstream evidence verified
PIVOT_SEQUENCE_V2 contract:
- status: BUILT_DERIVED_FEATURE
- source: MARKET_STRUCTURE_GBPUSD_ALL_TF_V1
- confirmation rule: 2 confirming bars
- availability: pivot event row + 2 bars in the same source timeframe
- lookahead control: pivot evidence unavailable before its two-bar confirmation timestamp
- 2025_used: false

H1 PIVOT_SEQUENCE_V2 QA:
- rows: 17,789
- price_numeric: True
- status_ok: True
- no_2025: True
- timestamps_ok: True

2016–2024 subset:
- pivot rows: 15,266
- LOW pivots: 7,731
- every row has availability_row - source_row = 2
- every row has confirmation_status = CONFIRMED_AFTER_2_BARS

## OHLC integration source
The workspace contains GBPUSD H1 2016–2024 OHLC in DMI_ADX_V1_OUTPUT/GBPUSD_H1_DMI_ADX_2016_2024.csv.
This file provides the completed H1 timestamp/open/high/low/close series used here only as market-bar evidence; it is not treated as a replacement for the canonical pivot generator.

## Candidate under test
For this integration audit only:
1. A confirmed LOW pivot becomes a support-boundary candidate at its pivot price.
2. The support is not usable before its PIVOT_SEQUENCE_V2 availability timestamp.
3. Raw downside break is observed at the first completed H1 bar after support availability whose CLOSE is below the support price.
4. A later confirmed LOW pivot below that support is used as downstream decisive-break confirmation candidate.
5. Decisive confirmation becomes available only at that lower pivot's PIVOT_SEQUENCE_V2 availability timestamp.

This is explicitly an operationalization candidate. It is not claimed to be Murphy's literal numeric rule and is not production-frozen.

## Real-data integration results
Using all H1 2016–2024 data:
- candidate support-break/confirmation events: 7,648
- unique support candidates in this population: 7,648
- unique confirming lower pivots: 2,848
- median raw-break to confirmation-availability lag: 9 hours
- maximum lag: 79 hours
- zero confirmations on the same bar as the raw break

The large difference between support candidates and unique confirming pivots shows that one later lower pivot can confirm breaks of multiple older support candidates. This is a real population/identity issue and must not be silently collapsed by the evaluator.

## Deterministic invariants
All passed:
- support availability <= raw-break timestamp
- raw-break timestamp < confirming lower-pivot timestamp
- raw-break timestamp < confirmation availability timestamp
- confirming lower-pivot price < support-boundary price
- no 2025 support candidates
- no 2025 confirmations

## Interpretation
The integration proves that the current candidate can be executed against real PIVOT_SEQUENCE_V2 availability semantics without lookahead and that its event chronology is deterministic.

It does NOT prove that:
- a single pivot-derived LOW is the project's official support identity;
- a close below that level is Murphy's official decisive-break definition;
- a downstream confirmed LOW is the approved decisive-break operator;
- the multiple-support-to-one-lower-pivot population should be deduplicated in a particular way;
- the rule is production-ready.

## Newly identified governance issue
Support identity/selection remains unresolved for a production 0008 evaluator. The real-data integration shows that multiple historical support candidates can be broken by the same later lower pivot. The evaluator therefore needs an explicit support-selection/identity policy before PASS/FAIL production classification.

This is separate from the earlier horizontal-clustering issue. It does not justify inventing a tolerance or threshold.

## Decision
INTEGRATION PASS for the candidate's chronology/availability mechanics.
PRODUCTION STATUS remains BLOCKED.

Remaining gates:
1. approve support identity/selection semantics;
2. approve decisive-break operational semantics;
3. deterministic unit tests against the approved contract;
4. 2016–2024 historical QA;
5. no-lookahead/leakage audit;
6. production freeze review.

2025 remains OOS and is excluded from operator/threshold selection.
