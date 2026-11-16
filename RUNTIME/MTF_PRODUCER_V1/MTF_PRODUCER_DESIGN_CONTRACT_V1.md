# MTF Producer V1 — Compatibility and Implementation Contract

Date: 2026-11-16
Status: DESIGN / IMPLEMENTATION GATE — NOT A DIRECTIONAL PRODUCER

## 1. Purpose

Build a separately versioned producer for source-backed M5, M15, M30, H1, H4 and D1 market observations, compatible with the existing Decision Brain input contract. The producer must not replace, retrain, or rewrite the Decision Brain, Murphy, Nison, Trading in the Zone, Similarity Engine, canonical Risk Engine, or the existing strict MTF join adapter.

This document authorizes engineering of the data acquisition, candle finalization, provenance, validation and adapter layers. It does not authorize inventing or selecting trend formulas.

## 2. Protected boundaries

- Murphy remains the technical-context authority. Any trend-regime mapping must be traceable to an already-approved Murphy rule/definition or separately approved semantic specification.
- Nison remains confirmation only.
- Trading in the Zone remains a process/psychology gate only.
- Similarity remains historical evidence only and cannot generate direction.
- Decision Brain remains unchanged.
- Risk remains a hard gate; no SL/TP or position sizing is generated here.
- 2025 remains locked OOS and must not be read for tuning, formula selection, threshold selection, or implementation selection.
- No live orders; runtime remains signal-only. No merge to main.

## 3. Timeframes and event model

Required candle intervals: M5, M15, M30, H1, H4, D1.

The canonical event clock is an explicitly timezone-aware UTC instant. Every source candle must carry:
- broker/server timestamp exactly as supplied by the MT5 terminal;
- configured broker-server timezone identifier and configuration version;
- normalized UTC candle-open and candle-close instants;
- symbol, timeframe, OHLCV, spread/tick-volume fields where supplied;
- source terminal/account-server identity (secrets excluded);
- retrieval time, producer version, schema version and raw-payload hash;
- candle-finalization status and the rule used to determine that it is closed.

Never infer timezone from machine locale, Egypt local time, file boundaries, DST patterns, or naive historical timestamps. Never silently apply utc=True to naive values. If the broker timezone/DST contract is unknown, block normalization and mark the event NOT_EVALUABLE.

## 4. Candle alignment and point-in-time rules

- A timeframe value is available only after that timeframe's candle is confirmed closed by the source.
- Lower-timeframe decision events may only consume the most recent fully closed higher-timeframe candle whose normalized close time is less than or equal to the decision as-of instant.
- Use backward as-of joins only; future candles are forbidden.
- Preserve source candle IDs/open-close times for each joined timeframe.
- Missing, duplicate, stale, partial, malformed or ambiguous candles are unavailable evidence. Never fill with zero, forward-fill across missing source periods, or synthesize candles.
- Warm-up requirements must come from an authoritative formula/indicator definition. Until recovered, insufficient history means NOT_EVALUABLE.

## 5. Decision Brain field contract

The downstream field names are fixed and are not permission to invent their meanings:
- M5_trend_regime
- M15_trend_regime
- M30_trend_regime
- H1_trend_regime
- H4_trend_regime
- D1_trend_regime
- mtf_trend_score

The historical artifact shows regime values -1/0/1 and aggregate score values -6..+6, but observed values do not prove semantic definitions. V1 must not assign these values or calculate the aggregate until an approved source definition is recovered and mapped to exact Murphy evidence. No scaling, imputation, proxy, EMA substitution, or newly chosen lookback/threshold is allowed.

The existing strict adapter at RUNTIME/DECISION_RUNTIME_V1/mtf_brain_input_join_v1.py is the integration point. Reuse it; do not create a second join implementation.

## 6. Producer architecture (separate modules)

A. MT5 acquisition adapter
- Read real terminal OHLCV for all six intervals and requested symbols.
- Capture raw source metadata and immutable payload hashes.
- Do not create a directional output.

B. Time normalization and candle finalizer
- Require explicit broker timezone/DST configuration and version.
- Convert aware source times to UTC; reject ambiguous/nonexistent local times unless the broker contract resolves them.
- Mark candles closed only from source/terminal evidence or a documented deterministic boundary contract.

C. Six-timeframe alignment adapter
- Align only closed candles with point-in-time backward semantics.
- Emit explicit per-timeframe availability and provenance.
- No defaults or inferred values.

D. Murphy semantic mapper (currently gated)
- Implement only after exact approved Murphy definitions, source IDs, parameters and warm-up behavior are located and compatibility-audited.
- Each produced regime must retain rule IDs, source candle IDs, formula version and calculation inputs.
- If the approved rule mapping cannot be proven, emit NOT_EVALUABLE, not a guessed regime.

E. Brain contract serializer
- Serialize only validated fields into the existing canonical schema.
- Emit schema/version metadata and a source envelope accepted by the existing live runtime.

## 7. Validation plan

1. Contract tests for timezone, DST, candle closure, duplicates, missing bars, stale data and future leakage.
2. Deterministic alignment tests across all six timeframes using synthetic fixtures explicitly labelled TEST_ONLY; fixtures must never be treated as market evidence or used to tune a formula.
3. Source parity tests against the canonical 2016–2024 MTF archive only after its timestamp provenance and producer semantics are independently established.
4. Historical validation must exclude 2025 entirely. Do not open/read 2025 files.
5. Live feed smoke test on MT5 Demo data, with no order permissions and no broker execution.
6. Verify all symbols/pairs use the same documented data contract; do not hard-code GBPUSD or gold.
7. Keep all output signal-only until separate demo execution gates are approved.

## 8. Known blockers from the 2026-11-16 source audit

- Canonical MTF archive contains 671,601 rows for 2016–2024, but timestamps are naive and timezone provenance is unresolved.
- 2,512 blanks exist across higher-timeframe regime inputs; they must remain unavailable until the original warm-up policy is proven.
- No six-timeframe producer source code was found in the canonical MTF archive or inspected top-level full-project archive.
- The older H1/H4 research-only reader is not an authority for the six-timeframe contract.
- Murphy historical source also contains naive timestamps; its timestamp provenance must be resolved before cross-source parity tests.

## 9. Acceptance criteria

The producer cannot be marked PASS until:
- broker timezone/DST and candle-close semantics are documented and tested;
- every timeframe's raw source lineage is reproducible;
- all Brain output semantics are backed by approved Murphy definitions;
- no missing/future/partial data can silently become a numeric Brain value;
- point-in-time alignment tests pass;
- 2016–2024 parity/validation is reproducible without touching 2025;
- all existing protected components remain unchanged;
- MT5 Demo acquisition runs with order execution disabled.

Until all criteria pass, producer status is BLOCKED / NOT_EVALUABLE and the Decision Brain must abstain rather than consume guessed MTF values.
