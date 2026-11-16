# MTF Producer V1 — Stage A Field Compatibility Matrix

**Date:** 2026-11-16  
**Parent:** PR #122 / `feature/mtf-producer-v1-design`  
**Status:** READ-ONLY AUDIT — all seven derived fields remain blocked pending authoritative semantics.

## Executive result

The canonical MTF archive establishes the names and observed serialized domains of the seven Brain inputs, but does not establish their formulas, timestamp timezone, broker-clock/DST behavior, or missing-value semantics. Therefore none of the seven derived fields is authorized for reimplementation yet.

The correct next build unit is the raw MT5 bar-capture layer. It can be implemented independently without inventing the derived MTF features. Historical parity remains blocked until historical timestamp provenance is recovered.

## Field-by-field matrix

| Brain field | Archive evidence | Observed domain / missingness | Formula / semantics | Decision |
| --- | --- | --- | --- | --- |
| `M5_trend_regime` | Canonical archive column exists | Audit reports observed regime encoding -1/0/1; no M5 blanks counted in the seven-field missingness table | Not recovered | BLOCKED |
| `M15_trend_regime` | Canonical archive column exists | -1/0/1 observed; 26 blanks | Not recovered; blanks may be warm-up but not proven | BLOCKED |
| `M30_trend_regime` | Canonical archive column exists | -1/0/1 observed; 53 blanks | Not recovered; blanks may be warm-up but not proven | BLOCKED |
| `H1_trend_regime` | Canonical archive column exists | -1/0/1 observed; 107 blanks | Not recovered; blanks may be warm-up but not proven | BLOCKED |
| `H4_trend_regime` | Canonical archive column exists | -1/0/1 observed; 371 blanks | Not recovered; blanks may be warm-up but not proven | BLOCKED |
| `D1_trend_regime` | Canonical archive column exists | -1/0/1 observed; 1,955 blanks | Not recovered; blanks may be warm-up but not proven | BLOCKED |
| `mtf_trend_score` | Canonical archive column exists | Observed range -6..+6; no field-specific blank count reported | Aggregation weights, component inclusion, conflict handling, and neutral semantics not recovered | BLOCKED |

**Important:** Observed values are descriptive facts only. They do not authorize a formula, threshold, weight, or directional interpretation. The aggregate score must not be reverse-engineered from correlation or fitted to historical outcomes.

## Timestamp and bar-availability contract

| Item | Current evidence | Required proof | Current decision |
| --- | --- | --- | --- |
| Historical archive timestamp | All serialized timestamps are naive | Original exporter/source timezone and clock semantics | BLOCKED |
| Broker/server timezone | Not declared | Broker server timezone history and DST transitions | BLOCKED |
| Timestamp meaning | README says higher-TF bars join after close; exact timestamp convention unproven | Whether timestamp labels bar open or close, plus availability timestamp | BLOCKED |
| Live MT5 time | Not yet captured by a versioned producer | Capture server time and UTC conversion with explicit broker policy | BLOCKED |
| Closed higher-TF bar | Architecture declares close-only alignment | Deterministic close-boundary tests for all six periods | BLOCKED |
| Missing bars / warm-up | Annual-start blanks observed | Per-field lookback requirements and explicit unavailable semantics | BLOCKED |
| Volume | Runtime expects explicit volume availability | Tick vs real volume provenance and missing/zero distinction | BLOCKED |

No naive timestamp may be relabeled as UTC. Do not apply `utc=True` to naive historical data. The live capture may normalize a timestamp only after the MT5 server-time conversion policy is explicit and tested.

## Existing architecture to preserve

- Required Brain fields remain exactly the seven names above.
- Reuse `RUNTIME/DECISION_RUNTIME_V1/mtf_brain_input_join_v1.py`; it performs backward as-of joining, allows exact matches, and rejects naive timestamps, duplicate timestamps, missing fields, and future-only input.
- The join adapter is not a feature producer and must remain non-directional.
- Do not substitute Similarity Engine 57D normalized features.
- Do not use the legacy research-only H1/H4 reader as a six-timeframe producer.
- Do not modify Murphy, Nison, TIZ, Decision Brain, Similarity Engine, or Risk Engine semantics.

## Safe first implementation: raw MT5 capture only

A separately versioned capture component may be implemented before derived feature semantics are recovered, provided it only records raw source bars and provenance.

Required raw record fields:

- `symbol`, `timeframe`, `bar_time_server`, `bar_time_utc`, `bar_close_time_utc`, `retrieved_at_utc`
- `open`, `high`, `low`, `close`
- `tick_volume`, `real_volume`, `spread_points`
- `volume_type`, `is_closed`, `source_id`, `broker_server_id`
- `timezone_policy_id`, `capture_version`, `payload_hash`

The capture must preserve raw server timestamps as received, record the explicit conversion policy, and reject conversion when the broker timezone/DST policy is unknown. It must never synthesize a bar or fill missing OHLCV values. It must mark a bar usable only after its close is confirmed.

Required capture tests:

1. all six timeframe identifiers map to the correct MT5 periods;
2. bar-close boundary and unfinished-bar exclusion;
3. server-time to UTC conversion with explicit timezone policy;
4. DST transition and ambiguous/nonexistent local times;
5. duplicate bar idempotency and conflicting duplicate rejection;
6. missing bars, stale feed, and out-of-order arrival;
7. tick-volume and real-volume remain distinct;
8. restart/replay produces deterministic records and hashes;
9. no future bar is available to an earlier query timestamp.

## Gate decision

- **Stage A (field semantics): BLOCKED** — no authoritative formulas recovered.
- **Stage A (historical timestamp provenance): BLOCKED** — source clock unresolved.
- **Stage B (raw MT5 capture): READY FOR IMPLEMENTATION** — provided it is raw-only and broker timezone conversion fails closed until configured.
- **Stage C (derived features): NOT AUTHORIZED** — wait for formula/source contract.
- **Stage D (historical parity): BLOCKED** — no naive timestamp guessing; use only 2016–2024 after provenance is proven.
- **2025:** untouched and locked OOS.
- **Trading execution:** disabled; no live or demo orders in this stage.

## Immediate next action

Implement the raw-only MT5 capture interface and deterministic tests on a separate branch. In parallel, continue searching the source archive/documentation for the original six-timeframe producer and historical timezone provenance. Do not emit the seven Brain fields until their semantics are authoritative.
