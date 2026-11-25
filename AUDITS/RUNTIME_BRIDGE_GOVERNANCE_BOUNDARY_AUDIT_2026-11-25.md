# Runtime Bridge and Governed Handoff Authority Contract Audit — 2026-11-25

## Scope
Static inspection of GitHub-tracked source on `fix/similarity-direction-isolation-2026-11-25`. No runtime code changed, no tests/workflows run, no market-data payloads opened, and no 2025/2026 data accessed.

## 1. Bridge checks
`RUNTIME/DECISION_RUNTIME_V1/full_brain_runtime_bridge_v1.py`:
- requires non-empty Murphy, Nison, and Risk evidence mappings;
- checks `authoritative=True` only for Risk;
- does not require Murphy or Nison `authoritative=True`;
- does not validate Murphy status, direction, rule provenance, or Murphy/Risk directional agreement;
- does not require Nison confirmation or reject absent/unverified Nison;
- forwards the supplied row into the assembler without a field-level direction-authority contract.

This means the bridge's own callable boundary is weaker than Gate 3C's upstream checks. A direct caller can bypass Gate 3C's stronger evidence validation.

## 2. Governed handoff checks
`compatibility/decision_brain_v1_handoff_adapter.py`:
- calls the recovered Brain with Similarity set to None (the aligned-path remediation);
- records Murphy and Nison evidence but does not validate their authority/status before returning governance status PASS;
- Risk FAIL becomes a hard block and Risk NOT_EVALUABLE becomes needs-review;
- Nison contradiction becomes needs-review;
- Nison absent/unknown confirmation is not itself a block;
- Murphy evidence is not a hard gate at this adapter boundary.

The adapter's `PASS` is therefore a handoff/assessment result, not proof that Murphy/Nison source authority has been authenticated.

## 3. Three-book evaluator checks
`evaluation/three_book_decision_evaluator_v1.py`:
- enforces rule allowlist membership;
- requires Murphy status PASS;
- rejects an actual directional conflict between Brain bias and Murphy direction;
- requires Risk pass and stop loss;
- rejects Nison contradiction;
- allows Nison confirmation to be absent/unknown, assigning medium rather than strong logic;
- does not itself require Murphy `authoritative=True`, source provenance, or exact Risk/Murphy pass-rule linkage.

This is a downstream decision filter, not a substitute for authenticated evidence contracts. A Brain bias matching Murphy direction is not proof the Brain's directional bias was derived from Murphy.

## 4. Canonical Gate 3C difference
`RUNTIME/DECISION_RUNTIME_V1/gate3c_single_event_e2e_v1.py` adds upstream checks for:
- Murphy authoritative=True and status PASS;
- known governed Murphy rule IDs;
- full 44-rule Nison envelope;
- authoritative Risk;
- Murphy/Risk direction, pass-rule and directional-source agreement.

These are valuable protections for that particular caller. They do not harden direct calls to the public bridge or other callers that invoke the assembler/governed adapter without Gate 3C.

## 5. Direct caller review boundary
The branch recursive tree and inspected source paths identify Gate 3C as the runtime bridge caller. The historical OOS producer/assembler and knowledge adapters use separate governed handoff/assembler paths. This is a focused static review; it is not an exhaustive proof against dynamically imported, generated, or future callers.

## 6. Required contract before implementation
Before modifying the bridge/adapter, approve and encode one shared fail-closed evidence contract:
1. Murphy: explicit authority, PASS status, allowed governed rule IDs, direction in canonical enum, and source-provenance binding.
2. Risk: explicit authority, PASS, valid direction, and exact directional linkage to Murphy where required by the selected event contract.
3. Nison: full required rule envelope and explicit confirmation state; missing/unverified must not silently be treated as confirmed. Whether missing Nison blocks or routes to review must be decided in the canonical policy.
4. Brain directional inputs: an explicit policy stating whether MTF/Volume may generate directional bias or are context-only. This audit does not select the policy.
5. Public bridge: enforce the same contract internally so direct callers cannot bypass it.
6. Tests: direct bridge bypass attempts, absent Murphy authority, absent Nison authority/confirmation, direction mismatch, provenance mismatch, and valid canonical Gate 3C path.

Do not invent new evidence field names or enum semantics. Reuse established project contracts after a compatibility audit.

## Status
- Gate 3C upstream checks: inspected, present.
- Bridge standalone Murphy/Nison authority enforcement: GAP.
- Governed handoff standalone Murphy/Nison authority enforcement: GAP.
- Evaluator: Murphy PASS and Risk pass/conflict checks present; authority/provenance checks are incomplete at this boundary; Nison absence remains non-blocking.
- Runtime tests/workflows: not run.
- No source/runtime changes made.
