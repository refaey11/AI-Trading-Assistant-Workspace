# Dynamic MTF Recovery + Time/Session Exhaustive Search — 2026-08-22

## Recovery performed
The reconstructed workspace ZIP was repaired with ZIP central-directory recovery (`zip -FF`) to recover entries that were previously unreadable due to bad local headers.

## Recovered Dynamic MTF artifacts
The repaired archive contains readable:
- `DYNAMIC_MTF_BINDING_CONTRACT_V1.json`
- `DYNAMIC_TIMEFRAME_SELECTION_EXAMPLES_V1.csv`
- `DYNAMIC_TIMEFRAME_SELECTION_POLICY_V1_DRAFT.json`

The authoritative contract is `DYNAMIC_MTF_BINDING_V1` and is a specification/integration contract. It defines dynamic role assignment, higher-timeframe-first evaluation, no fixed global entry timeframe, NOT_EVALUABLE on missing required data, and explicitly states that MTF assigns roles/evidence and does not generate BUY/SELL.

The examples cover 15–30m (M5/M15), 30–120m (M15/M30/H1), and several-hours (M30/H1/H4) holding horizons.

The policy file remains V1-DRAFT / architecture policy and contains no frozen numeric score/threshold/weight.

## Time/Session search
The repaired archive contains 241 entries. A filename scan and content-level scan found:
- no Time/Session Context artifact
- no Session Context runtime/contract
- no session-boundary source text

GitHub file search and Dropbox search also returned no matching Time/Session runtime/contract artifact in the connected repository/backups searched in this audit.

## Status
- Dynamic MTF source contract: RECOVERED / READABLE
- Dynamic MTF examples: RECOVERED / READABLE
- Dynamic selection policy: RECOVERED / READABLE / DRAFT (non-authoritative for numeric tuning)
- Time/Session source/runtime: NOT FOUND in exhaustive sources searched
- No semantics were invented.
- 2025 remains protected OOS.

## Next controlled action
Build/verify a deterministic Dynamic MTF runtime adapter from the authoritative binding contract only, using existing six-timeframe evidence. Do not invent Time/Session rules. Keep Time/Session `NOT_EVALUABLE/BLOCKED` until an authoritative source is recovered or the project governance explicitly removes it as a required standalone dependency.