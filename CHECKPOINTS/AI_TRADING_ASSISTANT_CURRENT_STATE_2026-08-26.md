# AI Trading Assistant — Current State Checkpoint

Date: 2026-08-26

## Locked project truth
- Do NOT rebuild any existing subsystem.
- 34 Murphy rules are already wired into the governed decision boundary.
- 44 Nison rules are already wired into the same decision boundary.
- 78-rule governed package = 34 Murphy + 44 Nison and is already working.
- Risk and Execution are already present.
- Memory subsystems exist but the current 2025 producer does not explicitly consume them through the Decision Brain boundary.
- Historical Context Memory, Historical Outcome Memory, Similarity Memory, and Context-Aware Retrieval are therefore a wiring/consumption problem, not a rebuild problem.
- MTF data exists but is not explicitly wired as a separate evidence object at the current Decision Brain boundary.
- 2025 OOS is permanently locked: no tuning, no threshold fitting, no policy/semantic changes using 2025.

## Immediate execution path
1. Build/validate a shadow-only historical-evidence bridge on chronological development data 2016–2024.
2. Feed the four existing memory sources into the single historical_evidence envelope without changing direction semantics.
3. Measure availability, candidate counts, lookahead violations, timestamp coverage, agreement/conflict with Murphy direction, downstream consumption, and prove memory cannot generate direction.
4. Audit MTF consumption.
5. Then analyze the final execution funnel using the existing runtime; do not infer causes without the actual artifact.

## Important correction
The recent 0021 context experiment was diagnostic only. Do not treat MURPHY_0021 as a replacement for the full Murphy runtime.
Do not create a new arbitration policy or hard veto based on that experiment.

## Current known 2025 funnel
The latest governed manifest showed 6,225 events, 2,691 EXECUTABLE and 3,534 NO_TRADE. The 3,534 NO_TRADE were associated with MURPHY_FULL_RULE_NO_DIRECTIONAL_PASS. The 2,691 were eligible/executable and risk-passing before later execution censoring. This does NOT by itself prove the exact reason for any reduction to final trade count; use the actual execution/backtest artifacts.

## Historical evidence already found
The older Final Backtest Engine artifact covers 2016–2018 and produced 33 executed trades with PF 2.2176 and expectancy 0.4725R, but it is not the same as the current full 78-rule evaluation. Do not substitute it for the current 78-rule development evaluation.

## Decision rule
Do not change strategy, risk limits, or rule semantics until the development-data wiring and execution funnel are measured with authoritative current artifacts.

