# Point-in-Time Evidence Join Policy V1

## Purpose
Provide one timing policy for both historical OOS and live execution without changing rule semantics.

## Core rule
An evidence record may be used at decision timestamp `T` only when `available_time <= T` and `status == AVAILABLE`.

## Ordering
1. Order evidence by `available_time`, not by event_time.
2. At decision time `T`, use only records with `available_time <= T`.
3. When multiple records for the same feature are eligible, prefer the latest authoritative record by `available_time`.
4. Never replace missing evidence with a proxy unless the existing rule contract explicitly permits that proxy.
5. If a rule requires an unavailable feature, return `NOT_EVALUABLE`; do not convert missing evidence to PASS or directional confirmation.
6. Record the selected evidence IDs in lineage for auditability.

## Lagged evidence
Lagged data is valid only when the rule contract permits using the latest previously available observation. For end-of-day futures open interest, the join must use the latest completed report that was actually available before `T`.

## OOS governance
2025 remains out-of-sample and cannot be used to tune thresholds, rule semantics, feature definitions, or source-selection policy.

## Live parity
The live path must apply the same availability rule and evidence selection semantics. The difference between backtest and live is the transport/source, not the decision semantics.
