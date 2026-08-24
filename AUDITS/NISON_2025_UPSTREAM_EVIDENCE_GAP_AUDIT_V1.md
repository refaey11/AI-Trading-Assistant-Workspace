# NISON 2025 UPSTREAM EVIDENCE GAP AUDIT V1

## Scope
Audit of the 2025 out-of-sample Nison runtime evidence stream. 2025 remains evaluation-only; no tuning or threshold selection is permitted.

## Runtime result
- Input rows for 2025: 6,225
- Nison rules: 44
- Evidence rows: 273,900
- PASS: 0
- FAIL: 83,298 (30.41%)
- NOT_EVALUABLE: 190,602 (69.59%)
- Full-coverage rules: 0
- Zero-coverage rules: 18

## Root cause
The Nison runtime is executing fail-closed. The current Market State producer supplies trend and location but does not supply all source-backed upstream categorical facts required by several Nison rules. Missing evidence must not be invented.

## Market State fields available
- timestamp
- OHLC
- volume and indicators
- trend
- structure_event
- volume_ratio / volume_state
- volatility_state
- support/resistance distances
- location
- bull_engulf / bear_engulf / hammer / shooting_star
- market_interpretation

## Missing upstream evidence families
- volume_high
- formation_confirmed
- formation_complete
- final_bullish_strong
- final_bearish_strong
- evidence_available
- role
- previous_session
- current_session
- direction
- source-backed qualitative candlestick facts
- source-backed confirmation structures

## Rule-group findings
### NISON_0021–NISON_0029
All 6,225 rows NOT_EVALUABLE. Reason: requires source-backed upstream formation fact. Required evidence is not present in the current Market State contract.

### NISON_0030
All rows NOT_EVALUABLE. Reasons split between requiring an existing uptrend and requiring pattern completion. Runtime needs formation_complete and final_bullish_strong in addition to contextual evidence.

### NISON_0031
All rows NOT_EVALUABLE. Primary reason: requires five-candle continuation structure. The inspected source adapter only enriches and forwards the latest three candles, creating a wiring/history-window mismatch that must be audited and fixed without changing rule semantics.

### NISON_0032–NISON_0037
Coverage varies, but required qualitative source-backed relations and categorical facts are incomplete. Do not convert qualitative source language into invented numeric thresholds.

### NISON_0038
All rows NOT_EVALUABLE. Requires previous/current session OHLC and direction; those fields are absent from the current Market State producer.

### NISON_0039–NISON_0044
All rows NOT_EVALUABLE. These require methodology/context evidence, including evidence_available, role and confirmation structures. They must not be converted into standalone directional detectors.

## Existing-project evidence discovered
The repository contains:
- Nison source adapter and runtime evaluators
- context/trend translation tests
- compatibility tests for source adapters
- runtime smoke tests for 0021–0044
- governance allowlist covering NISON_0001..NISON_0044
- provenance mapping that marks the Nison contracts as source-contract frozen

Some required fields appear in adapter/runtime test fixtures, but the audit did not establish an authoritative production producer for all missing fields. Test fixtures are not sufficient to manufacture production evidence.

## Decision
1. Preserve fail-closed behavior.
2. Do not invent thresholds or source facts.
3. Audit existing authoritative producers before building anything new.
4. Reuse and connect an existing producer when compatible.
5. Fix the NISON_0031 history-window wiring issue after compatibility verification.
6. Keep rules NOT_EVALUABLE where authoritative upstream evidence is genuinely absent.
7. Do not use 2025 OOS data for tuning or threshold selection.

## Next execution checkpoint
Perform a producer-by-producer compatibility audit for the missing evidence families, beginning with formation evidence, five-candle history support, session OHLC/direction, and methodology/context evidence. Record each producer as FOUND / COMPATIBLE, FOUND / INCOMPATIBLE, or NOT FOUND before integration.
