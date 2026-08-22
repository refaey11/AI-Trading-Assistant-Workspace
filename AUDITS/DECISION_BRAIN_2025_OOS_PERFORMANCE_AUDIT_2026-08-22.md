# Decision Brain — 2025 OOS Performance Audit

Date: 2026-08-22
Status: BLOCKED / NOT RUN

## Preflight result
The 2025 OOS lock is active and the current runtime rule boundary is frozen to the latest corrected **78-rule allowlist** (34 Murphy + 44 Nison). `MURPHY_0008` remains blocked/not evaluable. The repository still contains an older provenance-completeness artifact that reports a 79-rule canonical scope; that historical artifact is superseded for current runtime gating by the later 78-rule freeze/CI commits and must not be used to expand the runtime scope.

The repository does contain existing Murphy and Nison runtime evaluator implementations, so the individual rule-source layer is present. However, the current frozen Decision Brain path still does not expose an authoritative, frozen **trade-event stream** that maps those existing rule outputs through the Decision Brain -> Knowledge Alignment -> TIZ process gate -> Risk hard gate -> execution/evaluation contract for 2025.

A 2025 GBPUSD M1 dataset is present in Dropbox as `HISTDATA_COM_MT_GBPUSD_M12025.zip` (3.44 MB; Dropbox content hash `bac280e9537c0eed20f51297a64e8c05f12a54775e5a32ad417d05cd71e0bbed`). A derived GBPUSD H4/H1 MTF file reaching 2025-12-31 is also available locally, but that derived feature file is not sufficient by itself to reconstruct all 78 rule inputs or a frozen execution stream.

## Why performance was not run
`TRUE_BACKTEST_V2` remains a separate V2/V3 trading-engine backtest with its own signal/SL/TP configuration and costs not yet applied. The existing OOS contract explicitly rejects attributing such legacy/alternate results to the frozen Decision Brain path.

Therefore no 2025 Profit Factor, Expectancy, Win Rate, Drawdown, or total-R result has been claimed for the frozen Decision Brain. Any such number produced before the missing frozen execution/evaluation path exists would be invalid attribution.

## Integrity rules now in force
- 2025 is evaluation-only.
- No 2025 tuning, calibration, threshold selection, or implementation selection.
- No future data.
- Similarity and Historical Memory are evidence-only.
- TIZ cannot generate or reverse direction.
- Risk remains a hard gate.
- Only the latest frozen 78-rule allowlist may enter the rule-adapter runtime.

## Exact next gate
Build/verify the existing-source **frozen Rule Adapter -> Decision Schema -> Risk/Process evaluation stream** without changing any frozen book rule, threshold, or 2025 data. Then run the first 2025 OOS performance evaluation from that stream and record raw immutable outputs before calculating metrics.

## Not accepted as OOS proof
- TRUE_BACKTEST_V2 aggregate results
- old V2/V3 threshold searches
- any result with costs not applied
- any result whose signal logic differs from the frozen Decision Brain path
