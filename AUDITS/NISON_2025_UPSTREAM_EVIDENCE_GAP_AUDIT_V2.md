# Nison 2025 Upstream Evidence Gap Audit V2

Date: 2026-08-24
Scope: GBPUSD 2025 OOS Nison runtime

## Current verified state

- Fresh Nison production run completed successfully on 6,225 2025 H1 rows.
- 44 Nison rule IDs emitted across 273,900 evidence rows.
- Output: 83,298 FAIL; 190,602 NOT_EVALUABLE; 30.41% evaluable overall.
- Market State context has 24 columns and supplies source-derived trend/location and market-state fields, but it does not provide the upstream categorical formation/window/session/methodology fields required by several frozen Nison runtime modules.
- 2025 remains evaluation-only. No tuning or threshold selection from 2025 is permitted.

## Compatibility findings

### NISON_0021..0029
The runtime intentionally fails closed unless `formation_confirmed` is already supplied as a source-backed upstream fact. There is no authoritative 2025 formation producer identified in the current workspace search. Do not infer formation facts from outcomes or invent geometry/tolerances.

### NISON_0030
Requires Uptrend plus `formation_complete`, `final_bullish_strong`, and explicit confirmation. The current Market State does not supply the categorical facts. Remain NOT_EVALUABLE until an authoritative producer is identified.

### NISON_0031
A concrete adapter wiring defect was identified: the frozen runtime requires five candles, while the OOS adapter was exposing only the last three. This is a pure history-availability correction and does not add pattern semantics, thresholds, or 2025 tuning.

Implementation completed in `OOS_2025/nison_2025_source_adapter_v1.py`: payload history widened from 3 to 5 completed candles.

A regression test was added to `tests/compatibility/test_nison_2025_source_adapter_v1.py` to lock the five-candle contract.

### NISON_0032..0037
These rules require source-backed categorical facts such as close-at/near-high, near/similar body size, Window state, open-price relationships, and trend-resumption/continuation facts. The current Market State and adapter do not supply these fields. No authoritative producer for those exact fields was identified in the current search. Keep NOT_EVALUABLE unless a source-locked producer is found.

### NISON_0038
Requires previous/current session OHLC and explicit bullish/bearish direction. Current Market State does not expose session objects in the Nison context shape. No source-backed session producer was identified in the current search. Keep NOT_EVALUABLE.

### NISON_0039..0044
These are methodology/context modules, not ordinary candlestick detectors. Their runtime requires `evidence_available`, role=`confirmation` or `context`, and explicit confirmation. They must be supplied through the governed methodology/context evidence boundary rather than forced into Market State candlestick fields.

## Governance

- Nison remains confirmation/context only; it cannot create standalone trade direction.
- Murphy remains the directional/technical context authority.
- Trading in the Zone remains process/psychology gate only.
- Similarity/historical memory remains evidence only.
- Missing evidence must remain NOT_EVALUABLE; no fabricated proxy is allowed.

## Implementation status

1. Upstream evidence gap audit completed.
2. Concrete NISON_0031 history-window compatibility correction applied.
3. Regression test for five-candle availability added.
4. No authoritative producer found yet for the remaining missing formation/window/session/methodology facts in the current workspace search.
5. Historical QA must be rerun for the affected adapter before any fresh 2025 OOS evaluation after this integration change.

## Next gate

Perform the historical 2016-2024 QA on the modified Nison source adapter and the Nison runtime suite. Only after that passes should a new 2025 production run be considered. Do not use 2025 to tune or define any missing qualitative rule semantics.
