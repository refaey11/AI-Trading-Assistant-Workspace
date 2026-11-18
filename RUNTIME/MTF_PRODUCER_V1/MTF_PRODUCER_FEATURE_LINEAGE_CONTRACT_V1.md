# MTF Producer-to-Feature Lineage Contract V1

Status: Contract specification and reference validator only. Not yet wired into Stage C or Live Decision Runtime.

## Purpose
A SHA-256-shaped string is not proof that a feature was calculated from the referenced bars. This contract recomputes hashes over canonical payload bytes and binds each derived feature row to exact raw-bar payload hashes.

## Canonical hashing
- UTF-8 JSON, sorted object keys, compact separators.
- Unicode preserved; non-finite numbers and non-JSON values rejected.
- Lowercase hexadecimal SHA-256.
- Raw-bar payload and feature payload hashes are both recomputed. Hash shape alone is never accepted.

## Raw-bar record
Each raw record has an identity envelope (symbol, timeframe, bar_time_utc, source, producer), a complete payload containing the same identity fields and raw OHLC/volume/spread values, and payload_hash. Envelope and payload identity must match. bar_time_utc must be timezone-aware. This contract does not turn V1.3 raw epoch values into UTC; the clock provenance gate remains independently mandatory.

## Feature record
Each feature record has the same identity envelope, a payload containing feature name/value and identity fields, a recomputed payload_hash, feature_id, transform_id, transform_version, computed_at_utc, and a non-empty input_refs list. Each input reference contains raw_payload_hash, symbol, timeframe, and bar_time_utc.

Every reference must resolve to exactly one supplied raw record. Raw hashes are recomputed. Source, producer, symbol, and timeframe must match; reference timestamp must match the raw record. Missing, altered, duplicate, cross-symbol, and cross-timeframe inputs fail closed.

## Causality
- Every raw bar timestamp is at or before decision_as_of.
- Feature computation is at or before decision_as_of.
- Feature computation cannot precede its latest input bar.
- All timestamps must be timezone-aware.

## Explicit non-goals
This validator does not calculate MTF features, verify formula correctness, prove the producer executable ran, authenticate broker identity or timezone evidence, infer UTC/DST/offsets/close times, authorize Stage C/live decisions/orders, or change book/risk/direction semantics or the 2025 OOS boundary.

## Integration still required
1. Audit the actual Stage C/MTF producer and output schema.
2. Make the producer emit complete raw payload references and transform identity.
3. Invoke this validator at producer-to-feature and trusted runtime boundaries.
4. Bind all six timeframe feature rows to exact timeframe raw inputs without hardcoding role assignments.
5. Add replay, stale-data, missing-input, duplicate, cross-source, and tamper tests.
6. Keep production timezone policy allowlist empty until authoritative evidence is reviewed.
7. Run GitHub Actions; separately compile and test MQL5 in MT5 Demo.

Until integration and independent review pass, this contract does not unblock MTF-backed live decisions.
