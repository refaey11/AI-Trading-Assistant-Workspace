# MTF Runtime Gate Validation — 2026-08-29

## Purpose
Validate the actual runtime boundary between the recovered six-timeframe MTF source and the existing Decision Brain without changing Brain semantics or creating a new strategy.

## Source provenance already established
The project already identifies `MTF_ALIGNMENT_GBPUSD_V1` as the six-timeframe source family:
`M5 -> M15 -> M30 -> H1 -> H4 -> D1`.
The source exposes the Decision Brain field family including `mtf_trend_score` and the six `*_trend_regime` fields. The historical source-closure record explicitly states that field-name compatibility is supported, while end-to-end runtime execution remains to be demonstrated.

## Local runtime test
A pre-2025 2016 GBPUSD E2E event was executed through the existing Full Brain assembler using the currently available event artifact.

Event timestamp:
`2016-01-08T06:00:00+00:00`

Observed event market-state fields:
`atr`, `location`, `structure`, `trend`, `volatility`, `volume`

The event did NOT contain:
- `mtf_trend_score`
- `M5_trend_regime`
- `M15_trend_regime`
- `M30_trend_regime`
- `H1_trend_regime`
- `H4_trend_regime`
- `D1_trend_regime`

The existing recovered Decision Brain implementation currently uses zero defaults for these missing fields. The local test therefore produced a `NO_TRADE` with `MURPHY_BRAIN_DIRECTION_CONFLICT`, but that result is NOT valid evidence of a full six-timeframe Gate 3C run because the required MTF inputs were absent and implicitly defaulted.

## Safety correction validated locally
A strict non-invasive input guard was tested locally. It rejects the event with:
`MISSING_SOURCE_BACKED_MTF_INPUT:mtf_trend_score,M5_trend_regime,M15_trend_regime,M30_trend_regime,H1_trend_regime,H4_trend_regime,D1_trend_regime`

This is the correct behavior for the integration boundary: missing source-backed MTF inputs must block the Gate rather than silently become zeros.

## Decision
- Do NOT modify Decision Brain semantics.
- Do NOT invent numerical MTF encodings.
- Do NOT treat the legacy 2016 smoke result as Gate 3C PASS.
- Do NOT run the unified 2016-2024 backtest yet.
- Use the already-identified `MTF_ALIGNMENT_GBPUSD_V1` source to populate the exact fields, then rerun the same event through the existing Full Brain bridge.

## Gate status
`MTF source provenance`: PASS / CLOSED
`Six timeframe set`: PASS / CONFIRMED
`Brain field-family compatibility`: SUPPORTED
`Strict missing-input behavior`: PASS (local validation)
`Real MTF -> Brain runtime execution`: PENDING
`Gate 3C`: PENDING

## Next single action
Obtain one actual pre-2025 row from the recovered `MTF_ALIGNMENT_GBPUSD_V1` source containing the seven required Brain fields, join it to the 2016 event on the same timestamp/as-of, and execute the unchanged Full Brain + Risk + Trade Plan path.

## Governance
No 2025 tuning. No new strategy semantics. Murphy remains primary direction/context. Nison remains confirmation/contradiction. TIZ remains process-only and optional when unavailable. Historical/Similarity memory remains evidence-only. Risk remains a hard gate.
