# MTF Alignment Runtime Confirmation V1

## Status
CONFIRMED from direct inspection of `MTF_ALIGNMENT_GBPUSD_V1`.

## Confirmed timeframe contract
- M5
- M15
- M30
- H1
- H4
- D1

These six timeframes are supported by the separate `MTF_ALIGNMENT_V1` artifact. This must not be conflated with the narrower `MULTI_TIMEFRAME_READER_V1` component contract.

## Important architectural distinction
- `MULTI_TIMEFRAME_READER_V1` and `MTF_ALIGNMENT_V1` are separate artifacts/components.
- A limited contract in one component does not invalidate the six-timeframe support confirmed in `MTF_ALIGNMENT_V1`.
- Future audits must inspect the relevant artifact directly before making a project-wide claim about timeframe availability.

## Confirmed feature-level evidence
Direct inspection confirmed timeframe-level market features including:
- Pivot High / Pivot Low
- Break Structure Up / Break Structure Down
- Distance to Support / Resistance
- Doji
- Hammer-like
- Shooting-star-like
- Bullish / Bearish Engulfing
- Trend Regime

The aligned output also contains aggregate context fields including:
- `mtf_trend_score`
- `mtf_bullish_count`
- `mtf_bearish_count`
- `mtf_neutral_count`
- `mtf_context`
- `higher_tf_bullish_breaks`
- `higher_tf_bearish_breaks`

## Anti-leakage rule
The MTF artifact uses closed-bar alignment logic for higher-timeframe features. Higher-timeframe information must not be attached to a lower-timeframe observation before the source higher-timeframe bar is closed.

## Data boundary
The inspected GBPUSD MTF Alignment archive is historical/aligned data, not by itself a live current-market feed.

Therefore:
- Historical MTF evidence: CONFIRMED
- Six-timeframe contract: CONFIRMED
- Anti-leakage alignment principle: CONFIRMED
- Live current-market ingestion using the same contract: NEXT INTEGRATION STEP

## 2025 protection
2025 remains Out-of-Sample and MUST NOT be used for tuning or optimization.

## Decision Brain integration boundary
The next step is not to rebuild MTF alignment. Reuse the confirmed MTF contract and map live/current market inputs into the existing Decision Brain input boundary.

Target flow:

`Live Current Market -> Existing MTF Contract (M5/M15/M30/H1/H4/D1) -> Current Market State -> Existing Decision Brain`

No new direction rule is authorized by this confirmation. The MTF layer supplies market context/evidence; it does not replace the Decision Brain or independently create LONG/SHORT decisions.

## Governance rule added
Before declaring a component missing, limited, or unsupported:
1. Search the project artifacts and repository for the relevant named component.
2. Inspect the artifact directly when available.
3. Distinguish component-level limitations from project-level capabilities.
4. Record the conclusion with provenance.
5. Do not infer missing runtime support from a different component's contract.
