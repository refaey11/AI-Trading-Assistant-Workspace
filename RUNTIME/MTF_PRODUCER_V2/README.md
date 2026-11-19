# MTF Structure Producer V2 — isolated prototype

Status: **prototype / not production-ready / no runtime integration**.

## Input contract
- Completed, contiguous source-timeframe OHLC bars with integer sequence indices.
- Confirmed pivot events only: unique pivot ID, HIGH/LOW, price, source bar index, availability bar index, confirmation status.
- This prototype enforces a minimum two-bar confirmation delay, matching the inspected H1 PIVOT_SEQUENCE_V2 audit. It does not prove the canonical pivot producer is verified for all six timeframes.
- All timestamps, timezone mapping, broker clock provenance, payload hashes, and freshness must be validated by a future upstream evidence-envelope gate. The prototype cannot certify those facts.

## Semantics
- HH + HL => BULLISH_STRUCTURE; LH + LL => BEARISH_STRUCTURE; all other sufficiently populated combinations => RANGE_OR_MIXED.
- Structure events are evaluated against pivots available strictly before the break bar.
- BOS is a close crossing in the direction of the already established structure state; CHOCH is a close crossing against it.
- The previous completed close must be on/inside the boundary and the current close strictly beyond it, preventing repeated events on every subsequent bar.
- Wick-only breaks do not emit events.
- No score, timeframe vote, trading direction, order, or legacy-field alias is produced.

## Known limitations
- Pivot detector is external and deliberately not implemented here.
- Event deduplication/expiry and gap policy are not yet specified.
- Clock/provenance status is always emitted as `PROVENANCE_UNVALIDATED`; caller-supplied identifiers are metadata, not proof. No row is marked production-available.
- No market data, backtest, calibration, 2025 data, MT5 terminal, or live order path is used.
- Treat this as a deterministic semantic prototype only; do not connect to Decision Brain until separate adapter and validation gates pass.
