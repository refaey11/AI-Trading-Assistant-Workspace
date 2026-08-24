# Murphy 34 Final OOS Eligibility Matrix V1

## Scope
The frozen 34-rule scope is represented by `MURPHY_0001` through `MURPHY_0034` in the exact mapping audit. This matrix distinguishes mapping/evaluator/runtime/historical-evidence readiness and does not invent missing semantics or evidence.

## Current evidence
- 34 rules in scope.
- 26/34 are still `EXACT_MAPPING_NOT_FROZEN` in the exact mapping master audit.
- 8/34 have a dedicated evaluator artifact.
- The canonical runtime entrypoint directly wires 10 in-scope rules: 0006, 0007, 0018, 0019, 0025, 0026, 0030, 0031, 0032, 0033.
- MURPHY_0021 has a separate fresh 2025 historical producer.
- MURPHY_0003/0004 have historical evaluation artifacts through the prior 2016-2024 evaluation path.
- MURPHY_0021/0022/0023 have a historical evaluation artifact through the prior 2020-2024 path; 0022/0023 require futures OI and remain NOT_EVALUABLE on the spot-FX source path.
- MURPHY_0027/0029 has a historical artifact whose schema must be reconciled before treating it as authoritative rule-level evidence (the file labels the status columns as 0028/0029).
- The frozen 2025 coverage snapshot has authoritative usable rows only for MURPHY_0021 among the eight observed snapshot rules; 0003/0004/0022/0023/0028/0029/0050 do not currently provide usable 2025 evidence in that snapshot.

## 34-rule mapping state
| Rule | Mapping state | Dedicated evaluator | Canonical runtime entrypoint | Historical evidence note |
|---|---|---:|---:|---|
| 0001 | EXACT_MAPPING_NOT_FROZEN | No | No | No authoritative OOS producer |
| 0002 | EXACT_MAPPING_NOT_FROZEN | No | No | No authoritative OOS producer |
| 0003 | EVALUATOR_ARTIFACT_EXISTS | Yes | No | Historical 2016-2024 artifact; 2025 snapshot has 0 available |
| 0004 | EVALUATOR_ARTIFACT_EXISTS | Yes | No | Historical 2016-2024 artifact; 2025 snapshot has 0 available |
| 0005 | EXACT_MAPPING_NOT_FROZEN | No | No | No authoritative OOS producer |
| 0006 | EXACT_MAPPING_NOT_FROZEN | No | Yes | Runtime exists; exact mapping/evidence policy not frozen |
| 0007 | EXACT_MAPPING_NOT_FROZEN | No | Yes | Runtime exists; exact mapping/evidence policy not frozen |
| 0008 | EXACT_MAPPING_NOT_FROZEN | No | No | Candidate/runtime artifact exists but not registered |
| 0009 | EXACT_MAPPING_NOT_FROZEN | No | No | No authoritative OOS producer |
| 0010 | EXACT_MAPPING_NOT_FROZEN | No | No | No authoritative OOS producer |
| 0011 | EXACT_MAPPING_NOT_FROZEN | No | No | No authoritative OOS producer |
| 0012 | EXACT_MAPPING_NOT_FROZEN | No | No | No authoritative OOS producer |
| 0013 | EXACT_MAPPING_NOT_FROZEN | No | No | No authoritative OOS producer |
| 0014 | EXACT_MAPPING_NOT_FROZEN | No | No | Requires derived feature |
| 0015 | EXACT_MAPPING_NOT_FROZEN | No | No | Requires derived feature |
| 0016 | EXACT_MAPPING_NOT_FROZEN | No | No | Not yet evaluable / derived feature |
| 0017 | EXACT_MAPPING_NOT_FROZEN | No | No | Requires derived feature |
| 0018 | EXACT_MAPPING_NOT_FROZEN | No | Yes | Runtime exists; exact mapping/evidence policy not frozen |
| 0019 | EXACT_MAPPING_NOT_FROZEN | No | Yes | Runtime exists; exact mapping/evidence policy not frozen |
| 0020 | EXACT_MAPPING_NOT_FROZEN | No | No | No authoritative OOS producer |
| 0021 | EVALUATOR_ARTIFACT_EXISTS | Yes | Separate producer | Fresh 2025 source-backed producer exists; snapshot available_rate=1.0 |
| 0022 | EVALUATOR_ARTIFACT_EXISTS | Yes | No | Requires futures OI; spot-FX path is NOT_EVALUABLE |
| 0023 | EVALUATOR_ARTIFACT_EXISTS | Yes | No | Requires futures OI; spot-FX path is NOT_EVALUABLE |
| 0024 | EXACT_MAPPING_NOT_FROZEN | No | No | No authoritative OOS producer |
| 0025 | EXACT_MAPPING_NOT_FROZEN | No | Yes | Runtime exists; exact mapping/evidence policy not frozen |
| 0026 | EXACT_MAPPING_NOT_FROZEN | No | Yes | Runtime exists; exact mapping/evidence policy not frozen |
| 0027 | EVALUATOR_ARTIFACT_EXISTS | Yes | No | Historical artifact exists but needs schema/rule reconciliation |
| 0028 | EVALUATOR_ARTIFACT_EXISTS | Yes | No | Snapshot available_rate=0; historical path needs authoritative refresh |
| 0029 | EVALUATOR_ARTIFACT_EXISTS | Yes | No | Snapshot available_rate=0; adapter exists but not main runtime |
| 0030 | EXACT_MAPPING_NOT_FROZEN | No | Yes | Runtime exists; mapping currently not frozen |
| 0031 | EXACT_MAPPING_NOT_FROZEN | No | Yes | Runtime exists; mapping currently not frozen |
| 0032 | EXACT_MAPPING_NOT_FROZEN | No | Yes | Runtime exists; mapping currently not frozen |
| 0033 | EXACT_MAPPING_NOT_FROZEN | No | Yes | Runtime exists; mapping currently not frozen |
| 0034 | EXACT_MAPPING_NOT_FROZEN | No | No | Elliott Wave mapping not frozen / no verified evaluator path |

## Current 2025 Final-OOS readiness conclusion
**1/34** is currently supported by authoritative usable 2025 historical evidence: `MURPHY_0021`.

The other rules are not counted as final-OOS-ready until their exact mapping is frozen and a source-backed historical producer exists for the required evidence. Rules that require unavailable data (e.g. futures open interest) remain `NOT_EVALUABLE`; no proxy is substituted.

## Next step
Build/validate only the missing source-backed producers for the 34-rule scope, rerun the matrix, and then pass the resulting eligible evidence into the Full Decision Brain assembler. This matrix is an audit gate, not a trading-strategy redesign.
