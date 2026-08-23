# Murphy Runtime Eligibility Matrix V1

## Scope
This is an audit of the Murphy runtime actually present on branch `decision-brain-historical-event-producer-v1`. It does **not** infer missing rules from names, and it does not create new rule semantics.

## Directly wired in `murphy_runtime_entrypoint_v1.py`
- MURPHY_0006
- MURPHY_0007
- MURPHY_0018
- MURPHY_0019
- MURPHY_0025
- MURPHY_0026
- MURPHY_0030
- MURPHY_0031
- MURPHY_0032
- MURPHY_0033
- MURPHY_0047
- MURPHY_0048
- MURPHY_0049
- MURPHY_0051

**Direct runtime-entrypoint count: 14**

## Separate production path already implemented
- MURPHY_0021 — fresh 2025 producer exists and is source-backed.

**Current operational candidate count including the separate 0021 producer: 15**

## Code exists but is not wired through the main runtime entrypoint
- MURPHY_0008 — candidate/runtime files exist, but main runtime entrypoint does not register it.
- MURPHY_0022 — evaluator function exists, but main runtime entrypoint does not register it; requires futures OI evidence.
- MURPHY_0023 — evaluator function exists, but main runtime entrypoint does not register it; requires futures OI evidence.
- MURPHY_0029 — runtime adapter exists, but main runtime entrypoint does not register it.

## Historical 2025 snapshot-only evidence observed, but not currently operational as a usable runtime stream
- MURPHY_0003
- MURPHY_0004
- MURPHY_0028
- MURPHY_0050

The frozen 2025 coverage snapshot reports zero available rows for these four rules, so they cannot be treated as usable historical evidence without an authoritative producer.

## Important distinction
The project-level references to a broader Murphy rule set must not be collapsed into the **current runnable runtime set**. The runtime audit above is the only safe basis for deciding what can enter the final OOS path without inventing evidence.

## Current conclusion
- **14** Murphy rules are directly wired into the canonical runtime entrypoint.
- **+1** (`MURPHY_0021`) has a separate fresh historical producer.
- **4** additional rules have code/evaluator artifacts but are not wired into the main runtime entrypoint.
- **4** rules appear in the frozen 2025 snapshot but currently have zero available historical rows.

Therefore, the current evidence does **not** support claiming that all 34 project-level Murphy rules are ready for the final OOS test. The next engineering step is to reconcile the frozen 34-rule scope with the runtime registry and build source-backed historical producers only for rules whose contracts and required data are actually available.
