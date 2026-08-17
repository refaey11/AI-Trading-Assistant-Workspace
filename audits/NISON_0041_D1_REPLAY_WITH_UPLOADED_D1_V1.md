# Nison 0041 — D1 Replay / Candidate Confirmation Scan V1

Date: 2026-08-17
Dataset: uploaded D1(2).csv
Period: 2016-01-03 through 2024-12-31
Rows: 2,544
2025 rows: 0

## Data integrity
- Timestamp order: PASS
- Duplicate timestamps: PASS (0)
- D1 source timeframe: PASS
- 2025 excluded: PASS

## Upstream structural context
The canonical project already has the Murphy 0006/0007 confirmation layer and a 2016–2024 provisional result of 8 + 7 = 15 structural confirmations. Nison 0041 uses the existing trend-line context and adds candlestick confirmation; it does not replace or generate the structural direction.

## Candidate scan
The 15 provisional Murphy trend-line interaction events were checked against the uploaded D1 candle on the third-touch date.

Engineering candidate pattern families were limited to the existing project candlestick vocabulary:
- bullish: Hammer / Morning Star family / Bullish Engulfing
- bearish: Shooting Star family / Evening Star family / Bearish Engulfing

A touch-date candle showed at least one directionally compatible simple candlestick candidate on 7/15 structural events:
- 0006: 4/8
- 0007: 3/7

Observed simple candidates included:
- 0006: Hammer candidates on 2017-11-28, 2021-02-04, 2021-12-15; Bullish Engulfing candidates on 2018-07-13 and 2021-02-04.
- 0007: Shooting-Star candidates on 2021-10-11 and 2022-02-10; Bearish Engulfing candidate on 2022-09-13.

## Canonical status boundary
These 7/15 are CANDIDATE evidence, NOT canonical PASS. The currently available CANDLESTICK_SPEC_V1 explicitly warns that its deterministic pattern definitions are engineering-inspired and require mapping to exact Nison textual criteria before canonical treatment.

Therefore:
- structural context: available
- uploaded D1 replay: PASS
- candidate candlestick evidence: 7/15
- canonical Nison 0041 PASS: NOT_EVALUABLE pending pattern-contract binding
- no-lookahead at the uploaded candle scan: PASS (pattern uses current/previous candles only)
- 2025 tuning/selection: none

## Next gate
Bind the six confirmation pattern families to their existing canonical Nison pattern contracts (without inventing thresholds), then rerun this exact 15-event scan. Do not tune thresholds from 2016–2024 and do not use 2025.
