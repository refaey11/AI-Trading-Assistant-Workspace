# Murphy 20-Rule Unified Runtime Status — 2026-08-22

## Runtime-implemented set
Total: 20 rules

### Existing verified runtime set (8)
0003, 0004, 0021, 0022, 0023, 0028, 0029, 0050

### Newly integrated runtime batch (12)
0034, 0035, 0036, 0037, 0038, 0039, 0040, 0041, 0042, 0043, 0044, 0045

## Integration status
- Unified dispatcher coverage: 20 rules.
- Integration tests: PASS for all 20 dispatcher routes.
- New batch evaluator tests: 12/12 PASS.
- Missing/insufficient evidence remains fail-closed as NOT_EVALUABLE.
- No frozen rule semantics were intentionally changed.

## Counting convention
`20 Runtime Implemented` means the 20 rules have executable runtime routing and integration-test coverage.
It does NOT mean all 20 have completed production/historical performance verification.

## Remaining in the active 35-rule scope
35 - 20 = 15 rules remaining for runtime implementation/recovery.

## Next execution target
Work the remaining 15 active rules as the next batch, using existing artifacts first; recover missing implementations only from canonical/frozen rule definitions without inventing semantics.

## Hard boundaries
- Parked 16 remain out of scope.
- 2025 remains OOS and must not be used for tuning.
- Historical/similarity layers remain evidence only and cannot independently create direction.
- Trading in the Zone remains a psychology/process gate, not a directional generator.
