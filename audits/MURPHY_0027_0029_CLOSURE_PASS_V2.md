# Murphy 0027–0029 Closure Pass V2

Date: 2026-08-12

## 0028–0029 closure evidence

Existing `MURPHY_0027_0029_EVALUATOR_V1` provides exact implemented logic:
- 0028 PASS only when existing confirmed divergence is BEARISH at HIGH pivot.
- 0029 PASS only when existing confirmed divergence is BULLISH at LOW pivot.
- Missing divergence evidence returns NOT_EVALUABLE.
- The evaluator consumes existing Pivot Sequence V2, RSI-14, and confirmed divergence artifacts.
- Availability is taken from the divergence artifact's availability timestamp to avoid lookahead.
- `2025_used=false`.

Recorded unit tests for 0028/0029 all pass:
- confirmed bearish divergence;
- wrong divergence;
- missing evidence;
- confirmed bullish divergence;
- wrong divergence;
- missing evidence.

Historical summary:
- 0028 confirmed events: 1,592.
- 0029 confirmed events: 1,644.

## 0027 blocker

0027 remains NOT_EVALUABLE. The exact trend-vs-ranging regime operator is not defined in the authoritative project contract. No ADX threshold, fixed timeframe, or other proxy is invented.

## Decision

- 0028 = QA PASS / FREEZE CANDIDATE.
- 0029 = QA PASS / FREEZE CANDIDATE.
- 0027 = BLOCKED / NOT_EVALUABLE.

Production FROZEN status is not claimed in this pass because the official freeze manifest still requires source-semantic acceptance across the complete gate chain.

## Controls

- Existing components are reused; no rebuild.
- Similarity is not used to create or override Murphy direction.
- 2025 remains OOS and is not used for tuning or implementation selection.
