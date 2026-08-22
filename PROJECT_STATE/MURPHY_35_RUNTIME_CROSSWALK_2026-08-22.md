# Murphy 35 Runtime Crosswalk — 2026-08-22

Source of record: `MURPHY_35_RUNTIME_CROSSWALK_2026-08-22.csv`.

## Current confirmed runtime baseline

- Runtime Verified baseline: **8/35**
- Rules: `MURPHY_0003`, `MURPHY_0004`, `MURPHY_0021`, `MURPHY_0022`, `MURPHY_0023`, `MURPHY_0028`, `MURPHY_0029`, `MURPHY_0050`
- This baseline is the currently confirmed bound-and-tested runtime set. Do not inflate the count from artifact presence alone.

## Execution queue from the latest crosswalk

- `BIND_AND_TEST`: **8 rules**
- `RECOVER_AND_BIND`: **18 rules**
- `SEARCH_CANONICAL_ARTIFACT`: **9 rules**

The 9 canonical-artifact search rules are:

`MURPHY_0008`, `MURPHY_0025`, `MURPHY_0026`, `MURPHY_0031`, `MURPHY_0035`, `MURPHY_0036`, `MURPHY_0039`, `MURPHY_0043`, `MURPHY_0044`.

## Artifact availability categories

- `VERIFIED_ARTIFACT_PRESENT`: **8**
- `RECOVERY_ARTIFACT_PRESENT`: **12**
- `FEATURE_OR_MAPPING_PRESENT`: **11**
- `NO_DIRECT_ARTIFACT_FOUND`: **4**

## Execution rule

For every Murphy rule in scope:

`Frozen Rule -> Canonical/Recovered Artifact -> Adapter Binding -> Test -> Runtime Status`

No frozen semantics are to be changed during runtime integration. The 16 non-scope rules remain parked. 2025 remains OOS and must not be used for tuning.

## Next authoritative work

1. Process the 18 `RECOVER_AND_BIND` rules.
2. Process the 8 `BIND_AND_TEST` rules without changing semantics.
3. Search and reconcile canonical artifacts for the 9-rule search queue.
4. Only mark a rule Runtime Verified after binding and test evidence exists.
