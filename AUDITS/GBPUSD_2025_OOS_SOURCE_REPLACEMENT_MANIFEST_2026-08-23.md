# GBPUSD 2025 OOS Source Replacement Manifest — 2026-08-23

## Purpose
Replace the obsolete 2025 HistData source reference in the OOS planning record with the source-derived GBPUSD master that was directly inspected in the active workspace.

## Authoritative candidate source inspected
- Archive: `GBPUSD_M1_MASTER_2016_2026_V1(1).zip`
- ZIP SHA-256: `edb39db9c91dcfd2f3b5b11fa25734810d50cf501be37555d5ec9951715d8202`
- Extracted master CSV SHA-256: `e0383c003fdb08e8776e68a4e8d1cc30529c0be55799295c0ffbdd52a80e1bb8`

## 2025 verification
- Rows: 372,632 M1
- Timestamp duplicates: 0
- Zero volume: 0
- Null volume: 0
- `volume_available=True`: 372,632 / 372,632
- `source_period=TitanFX_2020_2026`: 372,632 / 372,632
- Range: 2025-01-02 00:00:00 through 2025-12-31 23:59:00

## Gaps
84 timestamp intervals exceed one minute. The long gaps are predominantly Friday-to-Monday market closures; short intraday gaps remain documented and are not filled or synthesized by this checkpoint.

## OOS governance
This source replacement does not modify rules, thresholds, TIZ semantics, Risk policy, or Decision Brain logic. 2025 remains evaluation-only and must not be used for tuning, calibration, or implementation selection.

## Status
`SOURCE_PROVENANCE_CHECK = PASS` for the inspected master dataset.

This does not by itself authorize the OOS performance run. The exact Decision-Event Stream still requires the current TIZ/Risk boundaries and source-to-runtime handoff to be authoritative.
