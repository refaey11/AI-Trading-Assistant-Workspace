# MTF Evidence Status Reconciliation

**Date:** 2026-11-18  
**Parent:** PR #122 — MTF Producer V1 governed design and compatibility gates  
**Status:** RECONCILIATION ONLY — NO FEATURE IMPLEMENTATION OR RUNTIME CHANGE

## 1. Why this reconciliation is required

The repository contains earlier MTF closure records (August 2026) and the newer MTF Producer V1 audits (November 2026). Their conclusions refer to different evidence layers. They must not be collapsed into a single PASS or BLOCKED label.

This record preserves the earlier valid findings while clarifying the remaining producer and live-capture gaps.

## 2. Evidence layers and current disposition

| Evidence layer | Earlier repository evidence | What that evidence actually closes | What remains open | Current disposition |
| --- | --- | --- | --- | --- |
| Official timeframe architecture | `docs/TIMEFRAME_ARCHITECTURE_CORRECTION_2026-08-21.md`; `docs/MTF_ALIGNMENT_RUNTIME_CONFIRMED_V1.md` | Official six-timeframe family is M5, M15, M30, H1, H4, D1; distinct from the H1/H4-only legacy Reader V1 | None for the six timeframe names themselves | CLOSED |
| Historical aligned MTF artifact identity | `audits/evidence/MTF_ALIGNMENT_6_TIMEFRAME_SOURCE_CLOSURE_2026-08-21.md` | Recovered `MTF_ALIGNMENT_GBPUSD_V1` artifact family exists and contains six-TF aligned feature families and aggregate MTF fields | Exact producer source/formulas, encoding, missing-value semantics, and complete lineage for every field | SOURCE FAMILY IDENTIFIED; FEATURE SEMANTICS PARTIAL |
| Historical 2020–2024 as-of alignment test | `AUDITS/TIMEFRAME_FULL_SIX_TF_ASOF_ALIGNMENT_2020_2024_2026-08-22_FINAL.md` | The tested rows had monotonic, duplicate-free timestamps and zero future mappings for the five reported timeframe joins | This test does not prove original timestamp clock provenance, all years, all symbols, live availability, or the original feature producer | TESTED WINDOW PASS ONLY |
| Historical timestamp provenance | `RUNTIME/MTF_PRODUCER_V1/STAGE_A_FIELD_COMPATIBILITY_MATRIX.md`; `BACKTEST/MTF_PROVENANCE_BLOCKER_2026-09-02.md` | The current recovered archive/producer lineage limitations are explicitly recorded | Naive legacy timestamps' timezone/clock/DST and original timestamp convention remain unresolved; exact producer mapping remains unresolved | BLOCKED |
| Brain input field compatibility | `audits/evidence/MTF_ARCHITECTURE_V2_TO_DECISION_BRAIN_COMPATIBILITY_AUDIT_2026-08-21.md`; Stage A matrix | The seven field names align at the field-family/interface level | Formula meaning, aggregation weights, allowed encoding semantics, missingness and scaling policy | INTERFACE SUPPORTED; SEMANTICS BLOCKED |
| Live MT5 raw capture | `MT5_CAPTURE_TO_MTF_SOURCE_COMPATIBILITY_AUDIT_2026-11-18.md`; `MT5_EA_TIMESTAMP_SERIALIZATION_SOURCE_AUDIT_2026-11-18.md` | V1/V1.2 can capture raw bars for six native MT5 periods and validate core OHLCV/schema properties | Source clock contract, trusted observation/retrieval time, close/availability time, timezone policy, deterministic six-TF boundary evidence | PARTIAL |
| Dynamic MTF roles | `AUDITS/DYNAMIC_MTF_RECOVERY_ZIP_REPAIR_AND_TIME_SESSION_SEARCH_2026-08-22.md` and related adapter audits | Authoritative Dynamic MTF binding contract and examples were recovered; adapter components exist | Runtime execution against actual aligned rows, provenance/timestamp validation at upstream boundary, Time/Session Context remains separate | CONTRACT RECOVERED; RUNTIME PARTIAL |
| Live Decision Runtime integration | PR #120 and runtime source/tests | Runtime consumes a strict seven-field MTF envelope and can produce signal-ready/no-trade output without orders | A validated live producer must supply semantically correct, time-valid fields; full current-market-to-runtime evidence remains incomplete | PARTIAL / FAIL-CLOSED |

## 3. Important distinctions

### 3.1 Six-timeframe architecture is not blocked

The official six-timeframe architecture and the existence of the recovered historical aligned artifact are established. Do not rebuild the MTF architecture or describe the entire six-timeframe source family as missing.

### 3.2 Historical as-of PASS is scoped

The August 22, 2026 as-of report records zero future mappings and zero missing mappings for its tested 2020–2024 rows and five adjacent timeframe joins. Preserve that result as a scoped historical alignment test.

It is not evidence that:
- naive source timestamps have verified UTC provenance;
- the original producer formulas have been recovered;
- the live MT5 feed has equivalent timing behavior;
- every symbol/year has passed;
- the current Decision Brain has completed full end-to-end validation.

### 3.3 Source-family recovery is not formula recovery

The recovered `MTF_ALIGNMENT_GBPUSD_V1` artifacts establish the source family and field families. Observed values such as trend-regime encodings and aggregate score ranges do not reveal exact formula semantics, weights, warm-up behavior, or missing-value policy. Do not reverse-engineer these from correlations or outcomes.

### 3.4 Live capture clock audit is a separate issue

The November EA source audit concerns the semantics and provenance of timestamps emitted by the live MT5 raw-capture EA. It does not invalidate the existence of the historical MTF archive or the scoped August as-of result. It does prevent treating the current EA's serialized UTC-looking field as independently proven UTC until the exact platform contract and clock domain are documented.

### 3.5 Dynamic MTF and Time/Session are separate dependencies

The recovered Dynamic MTF binding contract must be reused and audited rather than rebuilt. Its existence does not close Time/Session Context, nor does it prove runtime execution against real aligned rows. Do not invent session boundaries or selection thresholds.

## 4. Correct next work sequence

1. Preserve the existing six-timeframe architecture and historical as-of PASS as scoped evidence.
2. Continue source-lineage/feature-semantics recovery for the seven Brain MTF fields from the canonical historical artifact and its immutable source metadata.
3. Continue the separate MT5 timestamp source-contract investigation; do not claim V1.3 clock acceptance yet.
4. Inspect the recovered Dynamic MTF contract and current adapter together, then identify only concrete compatibility gaps against the existing role contract.
5. Keep the live Decision Runtime fail-closed until a source-backed producer can provide semantically correct fields with valid availability/provenance.
6. Do not start Stage C derived feature production or Stage D parity until exact field semantics and historical time provenance are approved.

## 5. Governance

- No feature formula, score, weight, encoding, imputation, scaling, session boundary, or directional rule is introduced here.
- No existing architecture, historical data, V1/V1.2 EA, ingest contract, Decision Brain, Murphy, Nison, TIZ, Similarity Engine, or Risk Engine is modified.
- 2025 remains locked OOS and is not accessed or used.
- No trading orders are enabled.
- No merge to `main` is authorized.
- This is a documentation-only reconciliation; no automated test run is claimed.
