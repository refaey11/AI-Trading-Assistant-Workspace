# Field-Level MTF and Volume Contract Matrix — 2026-11-25

## Scope and guardrails
Read-only inspection of GitHub-tracked source and audit documents on branch `fix/similarity-direction-isolation-2026-11-25`. This matrix describes field contracts, not data values. No market-data payloads or fixture rows were opened. No 2025/2026 data was accessed. No runtime code was changed and no tests/workflows were run.

## Important correction to prior audit wording
The existing `audits/evidence/MTF_ALIGNMENT_6_TIMEFRAME_SOURCE_CLOSURE_2026-08-21.md` explicitly closes source-family provenance for the six-timeframe `MTF_ALIGNMENT_GBPUSD_V1` dataset and confirms field-family compatibility with Decision Brain. Therefore MTF source-family provenance is **CLOSED at artifact-family level**. The separate `BACKTEST/MTF_PROVENANCE_BLOCKER_2026-09-02.md` still records unresolved exact raw-to-feature semantics, numeric encoding, missing-value policy, scaling, producer lineage details, and timestamp semantics for the seven numeric Brain inputs. These are different levels of provenance and must not be conflated.

## A. Seven directional MTF fields consumed by Brain

| Brain input field | Brain use | Source-family evidence | Numeric encoding / range | Availability & timestamp | Murphy authority |
|---|---|---|---|---|---|
| `mtf_trend_score` | Sign and magnitude add bullish/bearish MTF evidence | MTF_ALIGNMENT_V1 aggregate field confirmed | Exact canonical numeric formula/range not proven by inspected producer contract | Backward as-of join; exact completed-bar lineage and source timestamp contract require producer-level proof | No field-level Murphy derivation/provenance |
| `M5_trend_regime` | Included in mean trend-regime score | Six-TF source family and trend-regime feature family confirmed | Exact token-to-number encoding not proven | M5 base observation; exact serialization/missing policy not proven in GitHub source | Not proven |
| `M15_trend_regime` | Included in mean trend-regime score | Same six-TF evidence | Exact numeric encoding not proven | Higher-TF closed-bar anti-leakage principle documented; exact field-level producer timestamp contract not proven | Not proven |
| `M30_trend_regime` | Included in mean trend-regime score | Same six-TF evidence | Exact numeric encoding not proven | Same as above | Not proven |
| `H1_trend_regime` | Included in mean trend-regime score | Same six-TF evidence | Exact numeric encoding not proven | Same as above | Not proven |
| `H4_trend_regime` | Included in mean trend-regime score | Same six-TF evidence | Exact numeric encoding not proven | Same as above | Not proven |
| `D1_trend_regime` | Included in mean trend-regime score | Same six-TF evidence | Exact numeric encoding not proven | Same as above | Not proven |

### MTF adapter behavior established from code
- `mtf_brain_input_join_v1.py` performs a backward as-of join and validates numeric presence/NaN. It does not encode, scale, impute, or generate direction.
- `mtf_source_contract_gate_v1.py` likewise validates numeric presence/timestamps only.
- The 2026-09-02 blocker explicitly says the V5.4 inline categorical mapping is not proven to be the original canonical producer encoding.
- The 2026-08-21 source-closure audit confirms six-TF artifact provenance and closed-bar higher-timeframe alignment at the evidence-document level, but does not claim final runtime PASS or establish every numeric encoding detail.

## B. Six Volume fields consumed by Brain

| Brain input field | Brain use | GitHub producer/adapter contract | Encoding / availability | Timestamp / source | Murphy authority |
|---|---|---|---|---|---|
| `M5_volume_regime` | Included in mean volume score when volume_available | No tracked producer/adapter mapping found in inspected branch | Numeric meaning/range and missing policy not established | Historical evidence documents M1_TitanFX_2020_2024 source artifacts; exact completed-bar handoff not established | Not proven |
| `M15_volume_regime` | Same | Not found | Not established | Same | Not proven |
| `M30_volume_regime` | Same | Not found | Not established | Same | Not proven |
| `H1_volume_regime` | Same | Not found | Not established | Same | Not proven |
| `H4_volume_regime` | Same | Not found | Not established | Same | Not proven |
| `D1_volume_regime` | Same | Not found | Not established | Audit evidence records D1 source coverage, but not a tracked Brain-field producer contract | Not proven |

### Volume boundary established from code and audit records
- `market_state_contract_adapter_v1.py` receives a single `volume` value, sets `volume_evaluable = (volume is not None)`, and returns a Market State object with `volume_state`. It does not emit `volume_available` or any of the six Brain `*_volume_regime` fields.
- Its tests cover a missing base volume as UNKNOWN, but do not test six-TF volume-regime production or zero-as-unavailable provenance.
- The August 21 volume lineage audit records non-zero M1-derived volume source artifacts for GBPUSD 2020–2024 across M5/M15/M30/H1/H4/D1. It explicitly says compatibility/propagation into Market State remains OPEN.
- The August 22 volume audit records the 2025 HistData volume as all-zero and says not to treat it as volume evidence. 2025 remains locked OOS and must not be used as a substitute or tuning source.
- The tracked source tree inspected for this matrix contains no committed `VOLUME_CONFIRMATION_V2` producer implementation or adapter mapping from its raw outputs to Brain's six regime fields.

## C. Additional directional inputs and authority

The recovered Brain's directional bias is calculated from the MTF evidence and trend-regime evidence; when `volume_available` is true, its volume mean can also contribute bullish evidence (positive mean) or neutral/weak evidence (non-positive mean). The Brain does not treat negative volume mean as bearish evidence in the inspected implementation.

The canonical Gate 3C builder constructs `brain_row = {**market, **mtf}`. This is a broad merge, not a directional-field whitelist. It does not attach per-field Murphy provenance to the MTF/market values. Separately validating Murphy/Risk direction and pass-rule linkage does not establish that Brain's internal directional features are derived from Murphy.

Similarity is now passed as `None` on the aligned knowledge handoff; the recovered Brain still has an optional Similarity-to-direction code path for any caller that supplies non-null Similarity. The existing caller review is not an exhaustive proof over every dynamic/indirect invocation in the full repository.

## D. Contract status summary

| Contract | Status |
|---|---|
| Six-timeframe MTF source-family provenance | CLOSED / CONFIRMED |
| Six timeframe names and feature family | CLOSED / CONFIRMED |
| Higher-timeframe closed-bar alignment principle | DOCUMENTED / CONFIRMED at evidence level |
| Seven MTF Brain fields present/numeric in adapter contract | VALIDATED structurally by join/gate only |
| Exact canonical numeric semantics for seven MTF fields | OPEN |
| Six volume source artifacts for GBPUSD 2020–2024 | DOCUMENTED / CONFIRMED at artifact-evidence level |
| Volume producer source and mapping to six Brain fields | OPEN / NOT EVALUABLE |
| Market State adapter produces six Brain volume fields | NO — inspected code does not |
| Field-level Murphy provenance for MTF/Volume directional fields | NOT PROVEN |
| Brain direction is Murphy-only | NOT PROVEN |
| 2025 volume availability | BLOCKED / UNKNOWN; do not inspect or tune in this workstream |

## E. Required next gate
Do not patch frozen Brain or runtime yet. First recover/identify the GitHub-tracked canonical producer contracts (or explicitly record unavailable source code) for:
1. seven MTF fields: formula, numeric encoding, missing policy, scale, timestamp and source lineage;
2. six Volume fields: raw volume input, timeframe aggregation, regime formula/encoding, availability policy, completed-bar timestamps and source lineage.

Then make a formal architecture decision:
- **Model A:** prove all directional MTF/Volume fields are derived from the exact governed Murphy direction event; or
- **Model B:** make Murphy the sole direction authority and restrict MTF/Volume to non-directional context, with Brain no longer allowed to independently change directional bias.

Any implementation must follow an explicit decision, a compatibility audit, and fail-closed tests. No 2025 tuning or data access.
