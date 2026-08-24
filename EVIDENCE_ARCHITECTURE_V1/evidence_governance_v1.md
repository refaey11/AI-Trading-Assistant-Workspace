# Evidence Architecture Governance V1

1. Rule semantics are immutable in the evidence layer.
2. Adapters may normalize source data, timestamps, units, and availability metadata; they may not invent directional evidence.
3. Proxies are prohibited by default. A proxy requires an existing frozen rule contract explicitly permitting it.
4. Evidence selection is point-in-time: `available_time <= decision_time`.
5. 2025 remains OOS and cannot tune source selection, thresholds, feature definitions, or rule semantics.
6. Historical and live paths must use the same normalized evidence schema and selection semantics.
7. Missing required evidence produces `NOT_EVALUABLE`, never PASS, FAIL-as-direction, or synthetic confirmation.
8. Every final decision must be auditable back to the evidence IDs used.
9. Source adapters must declare their authoritative source and availability policy.
10. Execution code must not be imported into evidence adapters; the layer ends at normalized evidence.
