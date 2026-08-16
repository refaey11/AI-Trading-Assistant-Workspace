# Nison 0038 Windows — Freeze Manifest Candidate V2

Status: CANDIDATE ONLY — NOT PRODUCTION FROZEN

## Evidence
- Rule: 0038 Windows
- Canonical structural operator: previous-session high < current-session low for bullish Window; current-session high < previous-session low for bearish Window.
- Inputs: previous/current session OHLC + existing trend context.
- Historical replay: GBPUSD D1 calendar-date sessions, 2016-01-03 through 2024-12-31.
- Rows: 2,544.
- Structural Windows: 6 total (2 bullish, 4 bearish).
- Availability violations: 0.
- 2025 used: false.
- Invented thresholds: false.
- Deterministic unit tests: 6/6 pass.
- Compatibility sign-off: PASS for the structural Window operator.

## Governance boundary
This manifest candidate does NOT grant Production Freeze.

Remaining blockers:
1. Official production freeze approval/record must be explicitly created through the project governance path.
2. Upstream raw MT5 timestamp-to-session conversion is outside the 0038 evaluator contract and must remain owned by the upstream sessionization layer.
3. The evaluator does not implement future Window closure behavior; this manifest freezes only the structural Window evidence contract if governance approves that scope.

## Role boundary
Nison remains confirmation-only. 0038 evidence cannot create direction by itself and cannot override Murphy, process, or risk hard gates.

## OOS boundary
2025 is excluded from tuning, selection, calibration and optimization. The 2016–2024 replay is historical QA only.

## Decision
STRUCTURAL_QA = PASS
COMPATIBILITY = PASS
AVAILABILITY_NO_LOOKAHEAD = PASS (within the evaluator's stated session-level scope)
PRODUCTION_FREEZE = BLOCKED_PENDING_GOVERNANCE_AND_UPSTREAM_SESSIONIZATION_SCOPE
