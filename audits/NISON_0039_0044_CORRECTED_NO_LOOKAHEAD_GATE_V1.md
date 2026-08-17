# Nison 0039–0044 Corrected No-Lookahead Gate V1

Status: CORRECTED TEST GATE / NOT FROZEN

## Finding
The prior adapter result claimed timestamp ordering prevented lookahead. That claim is withdrawn for validation purposes because sorting evidence before checking chronology can conceal an upstream ordering defect.

## Corrected invariant
The adapter MUST validate the causal order of the evidence as received from upstream. It MUST NOT sort events before validation.

Required sequences:
- 0041: trendline event -> later confirmation event.
- 0042: level-test event -> later confirmation event.
- 0043: breakout/return-inside-range -> later confirmation event.
- 0044: level break -> successful retest -> later confirmation event.

If an upstream event arrives with a timestamp earlier than the immediately preceding causal event, validation fails closed.

## Revalidation status
- Previous 7/7 result: withdrawn as a sufficient no-lookahead proof.
- Adapter source mapping remains valid.
- Historical QA remains blocked.
- Production freeze remains blocked.

## Governance
No thresholds, lookbacks, tolerances, or scoring are introduced by this correction. 2025 remains OOS and excluded from tuning/selection.
