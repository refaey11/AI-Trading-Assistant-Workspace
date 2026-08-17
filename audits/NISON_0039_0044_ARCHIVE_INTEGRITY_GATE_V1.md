# Nison 0039–0044 Archive Integrity Gate V1

Status: BLOCKED BY SOURCE ARCHIVE COMPLETENESS

## Direct local inspection
The uploaded GBPUSD_RULE_EVALUATOR_V2 workspace is delivered as four `.bcut` chunks. Each chunk contains a 157-byte metadata prefix and a payload. The payload sizes are:
- part 1: 50,870,000 bytes
- part 2: 50,870,000 bytes
- part 3: 50,870,000 bytes
- part 4: 46,609,966 bytes
Total available payload: 199,219,966 bytes.

Reassembling those payloads does not yield a complete ZIP archive. The ZIP central directory references content beyond the available 199,219,966 bytes; extraction/testing reports a missing-data condition. Therefore the full evaluator archive is not currently available in this runtime.

## What is still directly verified
- The Nison source/rule definitions are present in the 3-book integration and Trading Rules V2 archives.
- The Nison adapter/no-lookahead test source exists on the feature branch.
- PIVOT_SEQUENCE_V2 and TRENDLINE_GEOMETRY_V1 are known project artifacts from the evaluator workspace audit.

## Consequence
Do not claim end-to-end historical readiness for Nison 0039–0044 until the complete evaluator archive (or the missing remainder/artifacts) is available.

## Required recovery
Provide the complete `GBPUSD_RULE_EVALUATOR_V2_FULL.zip` or all missing archive chunks. Once available, run one batch to:
1. verify canonical pivot/trendline artifacts;
2. locate any approved S/R, breakout/return, and retest/polarity producers;
3. run Nison 0039–0044 end-to-end causal/no-lookahead tests;
4. run 2016–2024 historical QA;
5. keep 2025 OOS and excluded from tuning/selection.

No new numerical operators are invented while the source archive is incomplete.
