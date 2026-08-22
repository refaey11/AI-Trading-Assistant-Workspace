# GBPUSD 2025 Upstream Feature Compatibility Audit — 2026-08-23

## Scope
Extend existing documented upstream feature producers to 2025 without changing definitions, thresholds, or OOS governance.

## 2024 compatibility results
- Volume Confirmation V2: PASS. After matching the existing bar-close timestamp semantics (`label=right`, `closed=right`), 2024 H1/H4 volume, volume_direction, and volume_ratio_to_previous matched the existing artifacts exactly.
- OBV V1: PASS for directional semantics. OBV_DIRECTION and OBV_SLOPE_1BAR matched the existing 2024 artifact; the absolute OBV level differs only by a constant origin, which the contract explicitly treats as arbitrary.
- DMI/ADX V1: NOT_COMPATIBLE_YET. Fresh reproduction did not numerically match the existing 2024 artifact; do not use the fresh reproduction for OOS until the canonical producer/initialization semantics are recovered.
- Parabolic SAR V1: NOT_COMPATIBLE_YET. Fresh reproduction did not match the existing 2024 artifact; do not use the fresh reproduction for OOS until the canonical producer semantics are recovered.
- Four-week lookback: NOT_COMPATIBLE_YET. Fresh reproduction did not match the legacy 2024 artifact; retain as blocked until the canonical source/producer semantics are reconciled.

## 2025 implication
- Safe to extend now: Volume Confirmation V2 and OBV directional/slope evidence, subject to the existing contracts.
- Still blocked: DMI/ADX, Parabolic SAR, four-week lookback.
- No 2025 tuning or threshold selection was performed.
- TIZ remains direction-neutral/deferred; no TIZ semantics were invented.

## OOS rule
Only compatibility-verified upstream evidence may enter the 2025 frozen decision path. Unverified/reconstructed features remain NOT_EVALUABLE.
