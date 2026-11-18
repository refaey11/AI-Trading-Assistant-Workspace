# MT5 EA Timestamp Serialization — Source-Level Audit

**Date:** 2026-11-18  
**Scope:** Read-only inspection of the V1 and Forex-Only V1.2 MQL5 exporters.  
**Branches inspected:** `feature/mt5-raw-capture-v1`, `feature/mt5-forex-only-capture-v1-2`  
**Decision:** The EA source alone does not prove that the serialized `bar_time_mt5_utc` is UTC. V1.3 UTC provenance must remain blocked pending authoritative source-contract evidence.

## 1. Source files

- `RUNTIME/MT5_RAW_CAPTURE_V1/MT5_Raw_Capture_Only_V1.mq5`
- `RUNTIME/MT5_FOREX_ONLY_CAPTURE_V1_2/MT5_Forex_Only_Raw_Capture_V1_2.mq5`

Both files contain the same timestamp formatter:

```mql5
string IsoUtc(const datetime value)
{
   MqlDateTime t;
   TimeToStruct(value, t);
   return StringFormat("%04d-%02d-%02dT%02d:%02d:%02dZ",
                       t.year, t.mon, t.day, t.hour, t.min, t.sec);
}
```

The function decomposes the supplied `datetime` and appends the literal suffix `Z`. There is no timezone conversion, UTC offset application, source validation, synchronization check, or uncertainty calculation in this function.

Both exporters call it for:
- `rates[0].time` → serialized as `bar_time_mt5_utc`;
- `TimeGMT()` → serialized as `host_gmt_estimate_utc`.

The fact that a field name or serialized string ends in `_utc` / `Z` does not itself prove UTC provenance.

## 2. What the EA does establish

The source visibly:
- calls `CopyRates(symbol, tf, 1, 1, rates)`;
- uses shift 1, described in comments as the latest fully closed bar;
- records current `TimeTradeServer()`, `TimeCurrent()`, `TimeGMT()`, and `TimeLocal()` observations separately;
- writes a contemporaneous server-minus-host-GMT diagnostic;
- writes `is_closed=true` after the shift-1 CopyRates call succeeds.

This supports the intended closed-bar selection path and separate clock-observation fields. It does not by itself establish the UTC meaning of `rates[0].time`, the accuracy of the host clock, or the actual close/first-availability instant of the bar.

## 3. Required correction to the V1.3 evidence position

Until an authoritative MT5 source contract is attached and reviewed:
- treat `bar_time_mt5_utc` as a source timestamp serialized with a UTC-looking label, not as independently proven UTC;
- do not use it for cross-source UTC ordering or no-future claims that depend on verified UTC;
- do not infer broker timezone/DST from `observed_server_minus_host_gmt_seconds`;
- do not treat `TimeGMT()` as a trusted synchronized UTC clock without synchronization and uncertainty evidence;
- do not populate `bar_close_time_utc` by adding timeframe duration;
- keep the historical 2016–2024 naive timestamp archive blocked and unchanged.

This audit does not assert that MT5's timestamp contract is wrong. It states that the reviewed EA code does not independently prove that contract. Platform documentation/source evidence and controlled terminal observations are still required.

## 4. Safe next action

Before implementing the V1.3 timestamp validator or changing any EA:
1. Attach authoritative MT5 documentation/source evidence for the exact semantics of `MqlRates.time` and the datetime clock APIs used.
2. Record the documented clock domain for each source independently.
3. Decide whether the capture machine's UTC clock can be trusted, and how synchronization/uncertainty is evidenced.
4. Keep unresolved values explicitly unavailable.
5. Only then freeze the V1.3 schema and write deterministic fixture assertions against that approved contract.

No EA, CSV, ingest adapter, existing V1/V1.2 data, feature formula, Decision Brain, or trading behavior was changed by this audit.

## 5. Gate status

- Existing V1 Python contract tests: prior GitHub Actions run passed; that does not validate clock-source truth.
- EA MQL5 compile/runtime: not re-run as part of this read-only source audit.
- `bar_time_mt5_utc` UTC provenance: **NOT PROVEN BY REVIEWED EA SOURCE**.
- Observation clock trust/uncertainty: **NOT PROVEN**.
- `bar_close_time_utc`: **UNAVAILABLE / DO NOT SYNTHESIZE**.
- V1.3 fixture implementation: **BLOCKED pending source-policy approval**.
- Stage B: **PARTIAL**.
- Stage C and Stage D: **BLOCKED**.
- 2025 OOS: **LOCKED / NOT TOUCHED**.
- Live orders: **NOT AUTHORIZED**.
