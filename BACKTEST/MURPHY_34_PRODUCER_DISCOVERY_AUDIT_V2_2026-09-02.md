# Murphy 34 Producer Discovery Audit V2 — 2026-09-02

Status: DIAGNOSTIC / RECOVERY

## Scope

This audit inspects the preserved `GBPUSD_RULE_EVALUATOR_V2_WORKSPACE_PART_03_OF_03.zip.part` reconstruction and the current governed Murphy runtime entry point. It does not change rule semantics, thresholds, risk, or the 2025 OOS lock.

## Confirmed runtime boundary

The canonical Murphy runtime entry point dispatches the governed Murphy IDs including 0003/0004, 0006/0007, 0018/0019, 0021/0022/0023, 0025/0026, 0028/0029, 0030/0031/0032, 0033, 0034–0045, 0047/0048/0049, and 0050/0051.

## Producer families discovered in the preserved workspace

- MARKET_STRUCTURE / M5, M15, M30, H1, H4, D1 structure datasets
- PIVOT_SEQUENCE_V1_OUTPUT and PIVOT_SEQUENCE_V2_OUTPUT
- FOUR_WEEK_LOOKBACK_V1_OUTPUT
- DMI_ADX_V1_OUTPUT
- PARABOLIC_SAR_V1_OUTPUT
- OSCILLATOR_DIVERGENCE_V1_OUTPUT (RSI divergence)
- TRENDLINE_GEOMETRY_V1_OUTPUT
- OBV_V1_OUTPUT
- VOLUME_CONFIRMATION_V2_OUTPUT
- OPEN_INTEREST_V1_OUTPUT (plus an explicit blocked contract)
- Murphy exact-mapping / compatibility / coverage audit artifacts

## Important file-level findings

The preserved workspace contains explicit producer artifacts for at least:

- Four-Week Lookback: `FOUR_WEEK_LOOKBACK_V1_OUTPUT/GBPUSD_H1_2016_2024_FOUR_WEEK_LOOKBACK.csv`
- DMI/ADX: H1, H4, D1 2016–2024 producer outputs
- Parabolic SAR: H1, H4, D1 2016–2024 producer outputs
- RSI divergence: H1 structure, H4 structure, D1 structure, and 2020–2024 aggregate output
- Trendline geometry: multi-timeframe historical structure trendline outputs across 2016–2024 and supporting contract/QA artifacts
- OBV: M5/M15/M30/H1/H4/D1 2020–2024 outputs with manifest/QA/contract
- Volume confirmation: M5/M15/M30/H1/H4/D1 2020–2024 outputs with manifest/QA/contract
- Open Interest: aligned H1/H4/D1 2020–2024 outputs, source audit, QA, and an explicit blocked contract
- Pivot sequence: multi-timeframe structure/pivot outputs and confirmation-availability audits

## Rule-to-producer binding status

### Candidate for direct historical binding after exact schema/as-of validation

- 0003 / 0004 — market structure + reaction peak/trough evidence
- 0006 / 0007 — trendline geometry + third-touch/reaction event evidence
- 0025 / 0026 — Four-Week Lookback
- 0028 / 0029 — RSI divergence + pivot sequence
- 0040 — Parabolic SAR trend regime
- 0041 — DMI/ADX regime

### Producer exists, but binding is not yet promoted

- 0030 / 0031 / 0032 — Pivot/Point-and-Figure-related runtime requires authoritative P&F columns; discovered workspace contains pivot artifacts but this audit does not equate pivot sequence with P&F evidence.
- 0034 / 0035 / 0036 / 0037 / 0038 — runtime evaluators exist; the producer/input chain still requires exact historical schema validation.
- 0047 — runtime requires `index_new_high` and `ad_fails_high`; no promotion without an authoritative breadth/A-D producer.
- 0048 / 0049 — runtime requires TRIN fields; no promotion from unrelated volume data.

### Non-directional/process/risk gates

- 0039 — system-discipline/process context; no directional generation.
- 0042 / 0043 / 0044 / 0045 — account/exposure/risk/margin context; do not synthesize from market OHLC.
- 0050 — pre-trade checklist; direction remains NONE.
- 0051 — trade-plan completeness gate; direction generation remains false.

### Explicitly blocked / not enough authoritative historical evidence in current reconstruction

- 0018 / 0019 — runtime convergence evaluators exist, but the historical producer chain still needs authoritative upper/lower geometry payload binding.
- 0033 — no source-backed historical producer promoted yet.
- Any rule whose required evidence is absent remains `NOT_EVALUABLE`.

## Archive reconstruction limitation

The four local `.bcut` files reconstruct the raw bytes of workspace archive part 03. The resulting file is a valid ZIP segment with a central directory, but many local file headers/data ranges refer to earlier split segments. Therefore the current local reconstruction is sufficient for producer discovery but is not by itself sufficient to claim complete extraction of every mapping/output file.

## Governance decision

No producer is promoted solely because its filename exists. Promotion requires:

1. exact required field compatibility with the runtime evaluator;
2. real 2016–2024 source-backed values;
3. strict point-in-time/as-of eligibility;
4. no proxy substitution or fabricated values;
5. direction only where the frozen rule semantics allow it.

2025 remains OOS and locked from tuning/calibration/fitting.

## Next executable step

Bind the confirmed families (0003/0004, 0006/0007, 0025/0026, 0028/0029, 0040/0041) against their exact historical schemas, run bounded 2016–2024 validation, then expand to the remaining recoverable rules. Do not run the final full backtest until this gate passes.
