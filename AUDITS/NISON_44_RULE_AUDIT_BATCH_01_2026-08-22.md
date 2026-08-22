# Nison 44-Rule Audit — Batch 01
Date: 2026-08-22
Scope: CANDLE_RULE_0001–CANDLE_RULE_0015

## Source-of-truth findings
- The integrated registry contains 44 Nison candlestick rules.
- All 44 registry entries currently carry testing.status = UNTESTED.
- The operational candle engine spec currently lists 9 deterministic pattern labels and explicitly warns that these are not canonical Steve Nison textual criteria.

## Batch results
| Rule | Pattern | Current implementation | Registry test state | Audit status |
|---|---|---|---|---|
| 0001 | Bullish Engulfing | Exact detector present | UNTESTED | IMPLEMENTATION PRESENT / SOURCE-LOCK + QA PENDING |
| 0002 | Bearish Engulfing | Exact detector present | UNTESTED | IMPLEMENTATION PRESENT / SOURCE-LOCK + QA PENDING |
| 0003 | Dark Cloud Cover | No exact detector | UNTESTED | IMPLEMENTATION GAP |
| 0004 | Piercing Pattern | No exact detector | UNTESTED | IMPLEMENTATION GAP |
| 0005 | On Neck | No exact detector | UNTESTED | IMPLEMENTATION GAP |
| 0006 | In Neck | No exact detector | UNTESTED | IMPLEMENTATION GAP |
| 0007 | Thrusting | No exact detector | UNTESTED | IMPLEMENTATION GAP |
| 0008 | Morning Star | Only Morning Star-like operational label | UNTESTED | SOURCE-LOCK / EXACT DETECTOR GAP |
| 0009 | Evening Star | Only Evening Star-like operational label | UNTESTED | SOURCE-LOCK / EXACT DETECTOR GAP |
| 0010 | Morning Doji Star | No exact detector | UNTESTED | IMPLEMENTATION GAP |
| 0011 | Evening Doji Star | No exact detector | UNTESTED | IMPLEMENTATION GAP |
| 0012 | Abandoned Baby | No exact detector | UNTESTED | IMPLEMENTATION GAP |
| 0013 | Harami | Bullish/Bearish Harami labels exist, but canonical rule is broader | UNTESTED | SOURCE-LOCK + QA PENDING |
| 0014 | Harami Cross | No exact detector | UNTESTED | IMPLEMENTATION GAP |
| 0015 | Tweezers Top | No exact detector | UNTESTED | IMPLEMENTATION GAP |

## Promotion rule
No rule in this batch is promoted to Production Frozen or Runtime solely from the existing prototype. A rule needs source-mapped contract, deterministic evaluator, tests, adapter routing, and no-lookahead/provenance verification.

## Next action
Continue batch audit against CANDLE_RULE_0016 onward, then return to 0001/0002 for exact source mapping and QA rather than bypassing the canonical freeze gates.
