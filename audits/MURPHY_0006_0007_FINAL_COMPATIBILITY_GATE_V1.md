# Murphy 0006/0007 — Final Compatibility Gate V1

Date: 2026-08-13
Branch: murphy-0006-0007-event-operator-v1
Status: OPERATIONAL GATE OPEN / NOT PRODUCTION FROZEN

## Scope audited
Workspace/File Library state, Murphy source clarification, Rule Registry/current-state artifacts, Confirmation Layer contract, Candidate Evidence V4, Pivot V2 availability/no-lookahead, Trendline Geometry V1, Event Operator proposal, and 2016-2024 confirmation-availability QA.

## Verified
- Existing Pivot V2 and Geometry V1 are reusable and remain unchanged.
- Official candidate population reproduces: 347 total; 166 for 0006; 181 for 0007.
- Official strong-candidate population reproduces: 32 for 0006; 30 for 0007; 62 total.
- Candidate evidence exposes candidate pivot, line price, daily range intersection, directional reaction evidence, and observation-only no-break field.
- Confirmation Layer contract exposes the required output shape: third touch, reaction, no-break, confirmation timestamp and availability.
- Pivot availability preserves no-lookahead; reaction confirmation availability is later than the raw pivot timestamp.
- 15 provisional event-chain confirmations were reproduced for 2016-2024: 8 for 0006 and 7 for 0007.
- 2025 was excluded.

## Not found / not source-locked
No authoritative project contract was found that defines all of the following as deterministic 0006/0007 operators:
1. successful third-touch tolerance/criterion beyond the qualitative source semantics;
2. reaction magnitude/duration or an explicit project-approved reaction event definition;
3. a 0006/0007-specific no-break contract;
4. a production confirmation timing rule beyond the existing Pivot availability mechanism.

The current source-compatible event representation uses the next confirmed opposite-family pivot as the reaction event and post-touch D1 line-hold as no-break evidence. These are operational representations, not claims that Murphy states those exact algorithms verbatim.

## Prohibited bindings
- no ATR threshold
- no pip tolerance
- no percentage touch tolerance
- no fixed lookback
- no invented reaction magnitude/duration
- no automatic 3% binding
- no automatic 2-day binding
- no 2025 tuning

## Gate decision
COMPATIBILITY: PASS for architecture/integration boundary.
OPERATIONAL SOURCE-LOCK: NOT CLOSED.
PRODUCTION EVALUATION: NOT_EVALUABLE until the event representation receives project approval or an authoritative operator is found.

## Next smallest safe action
Keep the event operator isolated on the feature branch. Run deterministic contract tests against explicit evidence cases, but do not promote the 15 provisional confirmations to production PASS or freeze the rules. Historical QA may be used to validate determinism/availability only; it must not be used to tune an unsupported operator.

## Rationale
This gate closes the repeated search loop: the missing item is now precisely identified as an approval/provenance boundary, not missing market data or missing architecture. No upstream component should be rebuilt.
