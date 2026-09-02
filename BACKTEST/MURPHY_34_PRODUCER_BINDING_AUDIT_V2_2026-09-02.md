# Murphy 34 Producer Binding Audit V2 — 2026-09-02

Scope: diagnostic recovery branch only; 2016-2024 development window; 2025 locked OOS.

Principle: artifact presence is not decision eligibility. A producer is only decision-eligible after exact semantic binding, provenance, timestamp availability, and strict-as-of validation pass.

| Rule | Runtime | Producer family found in recovered workspace | Current state | Directional role |
|---|---|---|---|---|
| 0003 | exact | Pivot Sequence V1 + historical evaluator artifact | OBSERVED / NOT ELIGIBLE | structural bullish |
| 0004 | exact | Pivot Sequence V1 + historical evaluator artifact | OBSERVED / NOT ELIGIBLE | structural bearish |
| 0006 | exact | Trendline Geometry V1 / pivot confirmation availability | QA ONLY pending production-frozen confirmation semantics | bullish |
| 0007 | exact | Trendline Geometry V1 / pivot confirmation availability | QA ONLY pending production-frozen confirmation semantics | bearish |
| 0018 | convergence adapter | Trendline Geometry V1 candidate source family found | FOUND / UNVERIFIED exact convergence producer binding | contextual only until validated |
| 0019 | convergence adapter | Trendline Geometry V1 candidate source family found | FOUND / UNVERIFIED exact convergence producer binding | contextual only until validated |
| 0021 | historical evaluator | Existing historical evaluator output | SOURCE-BACKED / ELIGIBLE | directional/context |
| 0022 | historical evaluator | Existing historical evaluator output | SOURCE-BACKED / ELIGIBLE | directional/context |
| 0023 | historical evaluator | Existing historical evaluator output | SOURCE-BACKED / ELIGIBLE | directional/context |
| 0025 | exact comparator | Four-Week Lookback V1 | SOURCE-BACKED / ELIGIBLE | bullish |
| 0026 | exact comparator | Four-Week Lookback V1 | SOURCE-BACKED / ELIGIBLE | bearish |
| 0028 | exact evaluator | RSI Divergence V1 + Pivot Sequence | SOURCE-BACKED / ELIGIBLE | bearish warning |
| 0029 | exact evaluator | RSI Divergence V1 + Pivot Sequence | SOURCE-BACKED / ELIGIBLE | bullish warning |
| 0030 | P&F runtime | No P&F producer identified in recovered archive index | NOT EVALUABLE | neutral/reference |
| 0031 | P&F runtime | No P&F producer identified in recovered archive index | NOT EVALUABLE | neutral/reference |
| 0032 | P&F runtime | No P&F producer identified in recovered archive index | NOT EVALUABLE | neutral/reference |
| 0033 | runtime | No authoritative historical producer identified | NOT EVALUABLE | non-directional/unknown |
| 0034 | wave2 | No exact historical wave producer identified | NOT EVALUABLE | contextual |
| 0035 | wave3 | No exact historical wave producer identified | NOT EVALUABLE | contextual |
| 0036 | wave4 | No exact historical wave producer identified | NOT EVALUABLE | contextual |
| 0037 | Fibonacci zone | No exact historical producer identified | NOT EVALUABLE | contextual |
| 0038 | cycle period | Pivot/structure sources exist, but exact cycle-period producer binding unverified | FOUND / UNVERIFIED | contextual |
| 0039 | process gate | No historical directional producer required | PROCESS ONLY | non-directional |
| 0040 | PSAR regime | Parabolic SAR V1 outputs: H1/H4/D1 | FOUND / UNVERIFIED exact 0040 input binding | contextual |
| 0041 | ADX regime | DMI/ADX V1 outputs: H1/H4/D1 | FOUND / UNVERIFIED exact 0041 input binding | contextual |
| 0042 | capital reserve | Execution/account state only | NOT EVALUABLE | risk gate |
| 0043 | single-market exposure | Execution/account state only | NOT EVALUABLE | risk gate |
| 0044 | market risk | Execution/account state only | NOT EVALUABLE | risk gate |
| 0045 | total margin | Execution/account state only | NOT EVALUABLE | risk gate |
| 0047 | A/D divergence | No authoritative A/D producer identified | NOT EVALUABLE | bearish warning |
| 0048 | TRIN | Workspace contains blocked TRIN contract, not a usable GBPUSD producer | NOT EVALUABLE | context only |
| 0049 | TRIN | Workspace contains blocked TRIN contract, not a usable GBPUSD producer | NOT EVALUABLE | context only |
| 0050 | checklist | Depends on upstream evidence states; no standalone historical producer | NOT EVALUABLE until envelope is complete | process gate |
| 0051 | trade-plan gate | Execution-plan fields are runtime outputs, not market-history producer data | NOT EVALUABLE historically | process gate |

## Recovered producer families confirmed by archive central directory

- FOUR_WEEK_LOOKBACK_V1_OUTPUT
- DMI_ADX_V1_OUTPUT
- PARABOLIC_SAR_V1_OUTPUT
- OSCILLATOR_DIVERGENCE_V1_OUTPUT
- TRENDLINE_GEOMETRY_V1_OUTPUT
- OBV_V1_OUTPUT
- VOLUME_CONFIRMATION_INTEGRATION_V1_OUTPUT
- VOLUME_CONFIRMATION_V2_OUTPUT
- OPEN_INTEREST_V1_OUTPUT
- PIVOT_SEQUENCE_V1_OUTPUT
- PIVOT_SEQUENCE_V2_OUTPUT
- Explicit historical evaluator artifacts for Murphy 0003/0004, 0021/0023, and 0027/0029 families

## Integrity rules

- Never promote FOUND / UNVERIFIED to PASS without exact field/semantic mapping.
- Never use 2025 for tuning/calibration/threshold selection.
- Never synthesize P&F, A/D, TRIN, account state, wave, or cycle values.
- Preserve strict-as-of execution boundary: producer availability timestamp must be <= decision timestamp before evidence is eligible.
