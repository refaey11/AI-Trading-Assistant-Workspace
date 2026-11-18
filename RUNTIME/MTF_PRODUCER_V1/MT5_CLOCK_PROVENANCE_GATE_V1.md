# MT5 Clock Provenance Gate V1

## Purpose
Prevent an MT5 bar timestamp from entering UTC-aligned MTF processing merely because its text ends in `Z`.

## Source finding
The existing MT5 Raw Capture EA obtains the bar timestamp from `MqlRates.time` and formats its components with an `...Z` suffix. In the reviewed source, there is no broker-timezone/DST conversion step or per-bar timezone policy evidence. The separate host GMT estimate and capture-time server-minus-host offset are diagnostics; they do not prove the historical timezone offset for the bar.

Therefore, the legacy field `bar_time_mt5_utc` is not accepted by this gate as proof of UTC lineage.

## Required V1 provenance envelope
- `bar_time_source_clock = BROKER_SERVER`
- `bar_time_server`: broker-server wall time without a timezone suffix
- `timezone_offset_seconds`: explicit per-bar offset, defined as server time minus UTC
- `timezone_policy_id`: versioned policy identifying how the per-bar offset was established
- `timezone_evidence_ref`: traceable evidence for the policy/offset
- `bar_time_utc`: timezone-aware UTC timestamp, arithmetically consistent with the explicit offset
- `observed_at_utc`: timezone-aware collector observation timestamp, not a substitute for broker time

The offset is per bar, not a global fixed offset. DST transitions must be represented by the applicable per-bar offset and policy evidence. The gate does not infer either.

## Fail-closed behavior
Missing, naive, unsupported, or inconsistent lineage raises a specific validation error. Such rows must be blocked from MTF alignment and the Decision Brain. No timestamp is synthesized and no timeframe duration is added to manufacture a close time.

## Scope
This gate validates declared lineage and arithmetic consistency. It does not independently certify that a broker's timezone policy is truthful; that requires an authoritative broker clock/DST source and capture evidence. It also does not prove MQL5 runtime behavior or MT5 terminal clock accuracy.

## Explicit non-goals
- No indicator formulas, weights, scaling, direction, or imputation
- No 2025 OOS use
- No change to Murphy, Nison, TIZ, Similarity, or Risk semantics
- No trading execution
