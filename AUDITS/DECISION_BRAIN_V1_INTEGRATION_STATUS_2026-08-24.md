# Decision Brain V1 Integration Status — 2026-08-24

## Current frozen boundary
- Verified runtime rules: 78
- Murphy: 34
- Nison: 44
- Murphy_0008 remains explicitly blocked/not evaluable.
- Nison role: confirmation/contradiction only.
- TIZ role: process/psychology gate only.
- Similarity role: historical evidence only.
- Risk role: hard gate.
- 2025 remains evaluation-only; no tuning.

## Nison availability policy
- Nison NOT_EVALUABLE does not become PASS, contradiction, or standalone direction.
- Nison NOT_EVALUABLE does not globally block Decision Brain integration.
- Directional Nison PASS may provide confirmation.
- Directional Nison FAIL may provide contradiction only when the runtime explicitly supplies direction.
- Missing source-backed evidence remains fail-closed inside Nison evaluators.

## Integration objective
Allow Decision Brain V1 event flow to continue using the verified Murphy runtime and whatever Nison evidence is actually available, without fabricating missing Nison evidence and without treating missing Nison evidence as a global blocker.

## Explicitly out of scope
- No changes to frozen Nison rule semantics.
- No invented thresholds.
- No 2025 tuning.
- No Nison direction generation.
- No modification of Murphy direction role.

## Next verification
Run the 78-rule Decision Brain event-stream/regression suite against the new Nison availability policy, then record PASS/FAIL and coverage separately for runtime-boundary integrity versus 2025 evidence availability.
