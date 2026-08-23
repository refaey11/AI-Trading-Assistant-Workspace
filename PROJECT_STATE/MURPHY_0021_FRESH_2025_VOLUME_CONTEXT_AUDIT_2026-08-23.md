# Murphy 0021 Fresh 2025 — Volume Context Audit

Date: 2026-08-23

## Observed fresh run
- 2025 input rows: 6,225
- output rows: 6,225
- PASS: 0
- FAIL: 6,180
- NOT_EVALUABLE: 45
- tuning: false

## Root cause identified
The first fresh producer run computed `volume_direction` directly from the supplied H1 source `volume` column.

The existing project contract and historical Volume Confirmation V2 artifact use a source-faithful H1 volume context derived from M1 TitanFX bars aggregated to H1, then compare current aggregated H1 volume with previous completed H1 volume. The existing artifact is `VOLUME_CONFIRMATION_V2_OUTPUT/GBPUSD_H1_VOLUME_CONTEXT_2020_2024.csv` and records `m1_count`, `previous_volume`, `volume_direction`, and `source_timeframe=M1_TitanFX_2020_2024`.

Therefore the first 0-PASS result is treated as a context-wiring mismatch, not a rule-performance conclusion.

## Controlled fix
- Reuse the existing Murphy 0021 semantics unchanged.
- Derive H1 `volume_direction` from the authoritative M1 source using the existing project aggregation convention.
- Compare current aggregated H1 volume with previous completed H1 volume.
- Carry 2024 history into the 2025 context so the first 2025 H1 row has a previous completed H1 volume when available.
- No new threshold, proxy, tuning, or 2025 calibration.

## Data governance
The fresh 2025 input gate previously established that the authoritative M1 source contains 372,632 rows, 2025 has no zero/null volume, and the source period is TitanFX_2020_2026. The 2025 OOS lock remains active.

## Next check
Rerun PR/CI after the canonical M1-derived volume wiring. Only the resulting fresh artifact may determine the next action.