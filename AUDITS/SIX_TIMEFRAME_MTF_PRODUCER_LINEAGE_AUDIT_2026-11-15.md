# Six-Timeframe MTF Producer Lineage Audit — 2026-11-15

## Executive finding

The project has a real six-timeframe GBPUSD alignment archive and prior 2020-2024 timestamp-alignment evidence. However, the exact producer that generated the current six-timeframe `MTF_ALIGNMENT_GBPUSD_V1.zip` values (including `M5_trend_regime` ... `D1_trend_regime` and `mtf_trend_score`) has not been recovered. Therefore, the archive is a source-backed data artifact, but its full feature-generation semantics and earliest availability times are not yet producer-verified.

This is narrower than saying "there is no MTF data": the six-TF artifact and its historical alignment checks exist. The missing item is the authoritative generator/feature contract and per-row availability lineage for the exact Gate3C-consumed artifact.

## Evidence recovered

1. Dropbox contains `/MTF_ALIGNMENT_GBPUSD_V1.zip`, alongside same-family EURUSD, USDJPY, USDCAD, and XAUUSD archives.
2. GitHub commit `333795a0a135317619af69fd11f191db595e86a7` shows the governed development workflow downloading `/MTF_ALIGNMENT_GBPUSD_V1.zip`, extracting its CSV files, and passing the extracted directory to `BACKTEST/DEV_BACKTEST_RUNNER_V1.py --mtf-dir`.
3. Earlier audit commits `c269b0f0b5fb4acb5c735bbdc99d0bb917c3187e` and `f5e0e59b46f2b79a0e28405713955cb7f18720d1` document six source timeframes M5/M15/M30/H1/H4/D1, 2020-2024 counts, monotonic/duplicate checks, and backward/as-of mapping with no future timestamp mappings in that tested dataset window. A related audit `9467887ef96b20aedfa7755bf16ad2f76ffb8af0` says those source datasets exposed `bar_close_timestamp`. These are alignment audit results, not proof of the producer code for the Gate3C archive.
4. The separate `AI_Trading_Assistant_MULTI_TIMEFRAME_READER_V1` is explicitly RESEARCH_ONLY and implements H4 context + H1 local structure. Its spec says M15 is not fabricated from H1. It is not the Gate3C six-timeframe archive and must not be substituted for it.
5. `MTF_57D_DEEP_LINEAGE_FINDINGS_2026-08-29.md` explicitly reports that the exact raw/pre-standardized 57D producer and preprocessing lineage were not recovered. It warns not to feed standardized Similarity V2 matrices directly into Brain V1.
6. `compatibility/dynamic_mtf_binding_adapter_v1.py` validates explicit role assignments only; it does not produce the six timeframe trend regimes or score. `dynamic_mtf_runtime_resolver_v1.py` resolves roles from pre-derived evidence flags and likewise does not generate those raw timeframe features.
7. Historical commit `5a7fb724fec9a2536ea9465a7557f000af06a316` added a development-runner adapter that maps supplied trend labels to numeric values and calculates `mtf_trend_score` as the mean of available timeframe values. This is a runner-level transformation, not proof that it is the canonical producer/semantic contract for the Gate3C archive. It must not be silently treated as the Brain V1 source contract.

## What is and is not proven

| Question | Finding |
|---|---|
| Does a six-timeframe GBPUSD archive exist? | YES |
| Are there prior 2020-2024 as-of/no-future alignment checks for the six source timeframe series? | YES, as documented by prior audit evidence |
| Is the exact Gate3C archive producer code recovered? | NO |
| Are the trend-regime encodings and `mtf_trend_score` generation contract proven for that archive? | NO |
| Does the separate H1/H4 MTF Reader implement the six-TF archive? | NO |
| Does the Dynamic MTF role resolver generate trend features? | NO |
| Is earliest availability at Gate3C event time proven for all six TF fields? | NO |

## Safe decision

- Keep the six-timeframe source archive intact; do not replace it with the H1/H4 research-only reader.
- Do not invent or normalize directional numeric mappings, averaging, thresholds, or default-zero values as a substitute for the missing producer contract.
- Do not feed the Similarity V2 standardized 57D index directly into Brain V1.
- Preserve each timeframe's own source timestamp and `bar_close_timestamp` when present; prove the exact join and availability boundary used by the Gate3C archive producer.
- Until the exact producer/contract is recovered, six-TF fields whose derivation or availability cannot be proven must be marked NOT_EVALUABLE at the evidence boundary, not silently synthesized.
- 2025 remains frozen OOS and excluded from recovery, calibration, and tuning.

## Next concrete action

Search the original workspace/backup archives for the producer that generated `MTF_ALIGNMENT_GBPUSD_V1.zip`, and recover its source code, config, feature dictionary, and input lineage. If that source cannot be recovered, document the archive as externally supplied with unverified feature-generation semantics and retain a strict NOT_EVALUABLE gate for those fields. No runtime behavior is changed by this audit.
