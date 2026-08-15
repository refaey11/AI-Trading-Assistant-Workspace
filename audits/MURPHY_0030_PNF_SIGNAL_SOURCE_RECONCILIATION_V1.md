# MURPHY_0030 — P&F Signal Source Reconciliation V1

Date: 2026-08-15
Status: SOURCE RECONCILIATION — NOT PRODUCTION FROZEN

## Finding

The audited Murphy Chapter 11 material supports the following Point & Figure semantics relevant to MURPHY_0030:

- Three-point/three-box reversal charts use 45-degree trendlines.
- The Basic Bullish Support Line is a primary upward P&F trendline.
- Murphy's Chapter 11 figure set includes a downside breakout below a Bullish Support Line as an S-7 sell signal.
- Murphy states that the complex P&F patterns/signals combine a simple buy/sell signal with the relevant trendline or pattern clearance where applicable.

## Critical distinction

The Master KB identity for MURPHY_0030 is `P&F bullish support`, with X/O columns and Bullish Support Trendline as the structural reference. The current rule record does not specify a separate numeric confirmation threshold, fixed timeframe, or box size.

Therefore we must NOT silently convert:
- a generic P&F buy signal into the definition of 0030;
- the S-7 downside-break signal into a 0030 bullish-entry trigger;
- a box size or timeframe from an external tutorial into Murphy source semantics.

## Operational consequence

A source-faithful first-layer evidence operator can safely expose:

`bullish_support_line_status = ABOVE | AT_LINE | BELOW | NOT_EVALUABLE`

with availability tied to completed P&F construction inputs.

However, `ABOVE` is structural bullish-context evidence, not by itself a production trade entry signal. If the rule contract requires a specific P&F confirmation signal, that signal must be explicitly approved as a project operationalization before evaluator freeze.

## Governance

- No invented box-size value.
- No invented fixed timeframe.
- No 2025 tuning.
- No backtest-based signal selection.
- Missing construction/confirmation evidence => NOT_EVALUABLE.
- Reuse the shared P&F feature for 0030–0032.

## Source references

Primary source: John J. Murphy, Technical Analysis of the Financial Markets, Chapter 11 — Point and Figure Charting.
External corroboration was used only to understand conventional P&F terminology; it does not override Murphy or the Master KB.
