# ENTRY / DECISION TIMESTAMP BINDING AUDIT V1

Date: 2026-09-03
Branch: `diagnostic/murphy-34-recovery-2026-09-02`
Scope: 2016-2024 only; 2025 remains locked OOS.

## Canonical decision convention

The governed V5.4 replay defines H1/market/MTF rows as **bar-start timestamped**. At decision time `T`, producer evidence may be consumed only when its evidence availability timestamp is strictly before `T` (`availability_timestamp < decision_timestamp`). Entry is the **prior completed H1 close** and exit simulation begins from the H1 bar at the decision timestamp.

Source: commit `64d17c3236a1311968a4d248b01fe36a17ec862d`, message `fix: enforce strict asof execution inputs in V5.4 replay`.

## Audit result

The historical archive contains the producer payloads needed for the Murphy recovery, but the current evidence compiler does not yet preserve producer-level availability timestamps through the fan-in. Its generic as-of join currently allows exact timestamp matches. Therefore archive presence is **not** equivalent to decision-time eligibility.

Producer families audited on the H1 decision grid:

| Producer | Evidence availability field | Strict prior-evidence coverage | Exact timestamp rows rejected by `< T` | Status |
|---|---|---:|---:|---|
| DMI/ADX | `timestamp` | 99.9982% | 55,998 | READY_FOR_BINDING |
| Parabolic SAR | `timestamp` | 99.9982% | 55,998 | READY_FOR_BINDING |
| Four-week lookback | `timestamp` | 99.9982% | 53,314 | READY_FOR_BINDING |
| Volume context | `bar_close_timestamp` | 55.5859% | 31,123 | READY_FOR_BINDING |
| OBV | `bar_close_timestamp` | 55.5859% | 31,123 | READY_FOR_BINDING |
| Open Interest | `safe_availability_timestamp` | 55.2341% | 258 | READY_FOR_BINDING |
| RSI divergence | `availability_timestamp` | 55.5323% | 2,509 | READY_FOR_BINDING |
| Trendline geometry | `availability_timestamp` | 99.9625% | 14,954 | READY_FOR_BINDING |
| Pivot Sequence V2 | `availability_timestamp` | 99.9786% | 14,956 | READY_FOR_BINDING |

## Critical finding: OI

There are **258 H1 Open Interest rows where `safe_availability_timestamp == decision timestamp`**. These rows are not valid under the strict rule and must be excluded from the decision envelope rather than treated as available.

## Gate decision

**Timestamp convention: PASS.**

**Full fan-in strict-as-of gate: NOT YET PASS.**

Reason: the current canonical evidence compiler uses generic `merge_asof(... allow_exact_matches=True)` and the fan-in schema does not yet carry/compare each producer's true availability timestamp against the decision timestamp. The replay's strict-as-of contract exists, but it must be enforced at the adapter/fan-in boundary for each evidence family.

## Prohibited action

Do not publish or label a 2016-2024 profitability result as an official governed backtest until this producer-level binding gate is closed.

## Next governed action

Add/verify adapter-level fields and checks so every producer contributes an explicit `availability_timestamp`, and enforce:

`availability_timestamp < decision_timestamp`

Then rerun the diagnostic 2016-2024 replay. Only after the diagnostic replay passes the governance gates should the official profitability backtest be considered.
