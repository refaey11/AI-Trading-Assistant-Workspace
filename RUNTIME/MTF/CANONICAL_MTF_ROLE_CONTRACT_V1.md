# Canonical MTF Role Contract V1

Status: evidence-backed integration contract
Date: 2026-08-29

## Purpose

Preserve the existing Multi-Timeframe architecture without confusing the six-TF feature/alignment vector with the full MTF reader architecture.

## Full MTF reader timeframes

The existing MTF Reader Specification V2 defines seven real-data timeframes:

- M5 — execution confirmation
- M15 — short-term structure and confirmation
- M30 — local structure and pullback
- H1 — primary intraday structure
- H4 — higher-timeframe context
- D1 — major context
- W1 — macro context

Reading order:
Weekly/Daily context → 4H trend and major structure → 1H current structure → 30M pullback/continuation → 15M setup development → 5M confirmation.

## Six-TF feature/alignment layer

The audited six-TF fields are:

M5, M15, M30, H1, H4, D1

The associated source-backed fields are:

- mtf_trend_score
- M5_trend_regime
- M15_trend_regime
- M30_trend_regime
- H1_trend_regime
- H4_trend_regime
- D1_trend_regime

These six-TF fields are a feature/alignment layer only. They must not be treated as the complete definition of the full MTF reader; W1 remains part of the full reader architecture as macro context.

## Decision Brain input contract

The existing Decision Brain V1 specification requires more than the seven six-TF fields above. Its market-structure inputs are the six trend-regime fields. Its MTF-context inputs additionally include:

- mtf_trend_score
- mtf_bullish_count
- mtf_bearish_count
- mtf_neutral_count
- mtf_context_code

Its volatility module requires:

- M5_volatility_regime
- M15_volatility_regime
- M30_volatility_regime
- H1_volatility_regime
- H4_volatility_regime
- D1_volatility_regime

Volume is conditional and is active only when `volume_available=true`; unavailable volume must not be converted to zero.

Therefore, Gate 3C must validate the complete source-backed Brain input set actually required by the existing Brain path, not only the seven six-TF alignment fields.

## Non-negotiable data policy

- Use genuine OHLCV for each required timeframe.
- Do not fabricate M5/M15/M30 from H1.
- Preserve UTC/as-of causality.
- Do not generate BUY/SELL inside the MTF layer.
- Do not create guessed numeric encodings or zero-fill missing Brain inputs.
- Missing source-backed MTF inputs must fail closed rather than silently becoming 0.0.
- Historical memory remains descriptive evidence and cannot override current market structure.

## Integration boundary

MTF supplies role assignments and timeframe-specific market evidence. The existing Decision Brain remains responsible for synthesis/assessment. Murphy remains technical context/market structure; Nison remains confirmation; Trading in the Zone remains process-only; historical/similarity memory remains evidence only.

## Gate 3C requirement

Gate 3C is not PASS from schema/source provenance alone. PASS requires a real timestamped canonical event that carries the complete source-backed MTF/Brain input set into the existing Full Brain runtime with no missing/defaulted fields, followed by the existing risk/trade-plan path.

## Evidence sources

Canonical MTF architecture source in the existing Dropbox workspace:
AI_Trading_Assistant_FULL_PROJECT_V1/AI_Trading_Assistant_MTF_ARCHITECTURE_V2/MTF_READER_SPEC_V2.json

Decision Brain source contract:
/DECISION_BRAIN_V1_SPEC.json

Six-TF alignment source:
/MTF_ALIGNMENT_GBPUSD_V1.zip

This contract records wiring semantics only; it does not create or replace either source.
