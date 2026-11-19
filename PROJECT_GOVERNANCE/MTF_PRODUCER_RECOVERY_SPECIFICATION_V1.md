# MTF Producer Recovery Specification V1

**Status:** SPECIFICATION ONLY — NOT AN IMPLEMENTATION  
**Date:** 2026-11-19  
**Base evidence:** PR #137 historical source-search audit and the 2026-08-21/2026-08-29 MTF evidence records  
**Governance:** 2025 remains protected OOS. No source/runtime changes, no inferred formulas, no live execution.

## 1. Purpose

Define the minimum evidence required to recover or faithfully reproduce the original six-timeframe MTF feature producer consumed by the Decision Brain. This document does not authorize implementation, formula selection, data fitting, calibration, or runtime activation.

The existing MTF Alignment artifact is evidenced as a serialized six-timeframe input dataset. Its existence and as-of alignment evidence do not establish the exact algorithms that produced its numeric feature values.

## 2. Architecture boundaries

Keep these distinct:

1. **Full MTF Reader architecture:** W1, D1, H4, H1, M30, M15, M5, with top-down context and explicit timeframe roles.
2. **Six-timeframe alignment/feature layer:** M5, M15, M30, H1, H4, D1.
3. **Decision Brain numeric input contract:** consumes source-backed fields; it must not invent encodings or silently impute missing values.
4. **Dynamic MTF binding:** selects/assigns timeframe roles according to its recovered contract; it is not itself proof of the feature calculations.
5. **Similarity/Memory:** historical evidence only; never the sole decision maker.

Murphy supplies technical context/market structure. Nison supplies candlestick confirmation only. Trading in the Zone is a psychology/process gate only and cannot generate direction. Risk remains a hard gate.

## 3. Seven canonical fields under recovery

The following seven fields remain **UNRESOLVED / NOT_EVALUABLE** for numeric producer semantics until the evidence requirements in this specification are met:

- `M5_trend_regime`
- `M15_trend_regime`
- `M30_trend_regime`
- `H1_trend_regime`
- `H4_trend_regime`
- `D1_trend_regime`
- `mtf_trend_score`

Observed serialized values (including categorical values such as -1/0/+1 and score ranges) are observations only. They do not establish the formula, thresholds, lookback, aggregation, warm-up, or missing-data behavior.

The broader archived schema also exposes structure/pivot/BOS, distance, candlestick/context, and aggregate count fields. Their presence in a CSV schema is not proof that their producer semantics are recovered.

## 4. Evidence required before producer implementation

### 4.1 Authoritative source and version
- Recover the original executable producer source, or a formally approved complete algorithm specification.
- Record repository/path, immutable commit or artifact revision, source hash, producer version, dependencies, and execution environment.
- Establish that the recovered producer generated the exact archived dataset family being used as the reference.
- Do not substitute reader adapters, as-of joiners, schema normalizers, Similarity feature builders, XAUUSD-only pivot prototypes, or downstream consumers for the original producer.

### 4.2 Raw input contract
For every timeframe, specify:
- symbol identity and canonical symbol mapping;
- raw OHLCV field names, numeric precision, and volume type/availability semantics;
- candle open/close timestamp convention and timezone provenance;
- source broker/feed and immutable input snapshot identity;
- handling of gaps, duplicates, out-of-order bars, and incomplete candles.

### 4.3 Per-field calculation semantics
For each of the seven fields, provide:
- exact formula or deterministic algorithm;
- all parameters, thresholds, lookbacks, tie-breaking rules, and boundary conditions;
- required warm-up length and first valid output rule;
- null/NaN/missing-input behavior;
- whether the value is categorical, ordinal, or continuous, and its documented domain;
- deterministic behavior across repeated runs.

For `mtf_trend_score`, explicitly document its aggregation inputs, weighting, normalization, handling of unavailable timeframes, and whether it is computed from the six regime fields or from another independent evidence set. Do not infer that it is a sum, average, or vote count from observed ranges.

### 4.4 Time and causality
- Define whether each feature is calculated only from completed source candles.
- Define exact as-of join semantics for each target M5 observation.
- Prove that higher-timeframe features become available only after the source candle close.
- Preserve timestamp offsets and broker-server clock provenance; normalize to UTC only under an evidenced mapping.
- No naive timestamps, guessed timezone offsets, or DST inference.
- Tests must include boundary timestamps around HTF close, missing bars, duplicate bars, and future-bar injection.

### 4.5 Golden fixtures and reproducibility
- Obtain a small, immutable set of original raw inputs and corresponding original producer outputs from the same producer version.
- Include normal, boundary, warm-up, missing-data, gap, and contradictory-timeframe cases.
- Store fixture hashes and provenance.
- Require exact categorical matches and documented numeric tolerances for continuous outputs.
- A fixture created by a new implementation is not an authoritative golden fixture.
- Reproduce archived outputs on permitted development data without tuning to protected OOS data.

### 4.6 Missingness and warm-up
- Explain the observed early-file blanks per timeframe and field.
- Distinguish warm-up, source gaps, unavailable inputs, and producer errors.
- Never replace missing MTF values with zero, neutral, or a fabricated direction.
- Until semantics are established, affected rows must remain NOT_EVALUABLE and fail closed.

## 5. Validation gates

| Gate | Required proof | Failure result |
|---|---|---|
| P0 — Source identity | Immutable original source or approved complete algorithm spec | BLOCKED |
| P1 — Input provenance | Raw OHLCV, symbol, time and volume lineage | BLOCKED |
| P2 — Formula semantics | All seven field algorithms and missing/warm-up rules | NOT_EVALUABLE |
| P3 — Golden parity | Reproducible parity against original fixtures | BLOCKED |
| P4 — Causality | Completed-bar/as-of/no-future-leak tests | BLOCKED |
| P5 — Integration compatibility | Exact field mapping into existing Brain contract, no defaults | BLOCKED |
| P6 — Governed E2E | Timestamped canonical event through existing Brain, TIZ boundary and Risk path | NOT PASSED |

A schema check, alignment pass, reader pass, adapter pass, or successful unit test of an adapter cannot independently close P0–P6.

## 6. Explicit exclusions

- No new trend-regime formula or score formula is proposed here.
- No numeric encoding is inferred from observed output values.
- No zero-imputation or neutral fallback is permitted.
- No ATR-in-MTF assumption is permitted without source evidence.
- No change to Decision Brain direction logic is authorized.
- No BUY/SELL generation, order placement, or live trading is authorized.
- No 2025 data may be used for training, tuning, calibration, thresholds, feature selection, or iterative fitting.
- Do not rebuild the already-audited candle aggregation or existing MTF architecture from scratch.

## 7. Current evidence interpretation

The historical evidence establishes that:
- an MTF Alignment GBPUSD artifact family exists with M5/M15/M30/H1/H4/D1 schema and serialized trend/structure/context fields;
- source metadata describes higher-timeframe joins after source candle close;
- the complete MTF Reader architecture separately includes W1;
- Dynamic MTF binding and selection contract artifacts were recovered in the reconstructed workspace evidence;
- runtime alignment evidence and numeric producer semantics are separate gates.

The GitHub-only source search recorded in PR #137 did not recover the original executable numeric producer or authoritative formula semantics. References in old audit records to a recovered dataset or a closed alignment gate must not be reinterpreted as proof of recovered producer code.

## 8. Approval required to proceed

Implementation may begin only after an authorized source/algorithm and its provenance are identified, compatibility-audited against the existing Brain contract, and golden fixtures are available. Any implementation proposal must be isolated on a feature branch and remain Draft until explicit user approval. No changes to `main` or merges are part of this specification.
