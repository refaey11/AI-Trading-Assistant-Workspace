# Canonical Decision Pipeline Repair V1

Status: ACTIVE development repair

## Scope
Controlled integration repair only. Murphy, Nison, Similarity, Memory, TIZ, and Decision Brain direction semantics remain unchanged.

## Frozen execution contract
- Stop distance: 0.75 ATR
- Target: 2.0R
- Risk is a hard execution gate
- Development window: 2016-2024
- 2025 remains OOS-locked and must not be used for tuning

## Confirmed V5.4 defect
The V5.4 development replay constructed the canonical RiskRequest with `take_profit_distance = 1.5 * ATR` while recording `rr = 2.0`. That conflicts with the reconciled 2.0R risk boundary.

## Repair rule
The replay must derive reward distance from the same frozen stop distance used by Risk/Execution: `reward_distance = 2.0 * (0.75 * ATR)`.

## Acceptance sequence
1. Static contract validation.
2. One real pre-2025 event end-to-end.
3. Small deterministic event sample.
4. Full 2016-2024 replay.
5. Costs/slippage and profitability analysis only after the integration gate passes.

No profitability claim is authorized by this note alone.
