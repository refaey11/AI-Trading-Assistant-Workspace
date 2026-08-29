# Murphy Source Binding Plan V1 — 2026-08-29

## Purpose
Bind the user-supplied Murphy archive to the existing Decision Brain evidence path without rebuilding or changing Murphy rule semantics.

## Source of truth
`قواعد مورفي  2(6).zip` uploaded in this conversation.

## Inspection result
The archive was recursively unpacked, including nested backup/freeze ZIPs. The inspected material contains rule-specific evidence, production freeze records, QA/closure records, replay summaries, and provenance artifacts.

The strongest inspected batch record for `0034–0045` explicitly freezes rules `0034,0035,0036,0037,0038,0039,0040,0041,0042,0043,0044,0045` with their existing roles and no new semantics.

## Binding rule
Each existing Murphy rule remains responsible only for its own evidence. The runtime must:
1. preserve the source rule ID;
2. preserve event/candidate timestamp and availability timestamp where provided;
3. reject future evidence relative to the canonical event `as_of`;
4. retain NOT_EVALUABLE/FAIL states rather than converting them into signals;
5. aggregate the resulting rule evidence at the governed Murphy envelope;
6. pass the full governed envelope to the existing Three-Book/Decision boundary.

## No semantic changes
- No new Murphy thresholds.
- No invented proxies for unavailable inputs.
- No rule remapping to make historical counts match.
- No direction generation from historical memory.
- No Nison/TIZ semantics altered.
- No 2025 tuning.

## Gate 3C selection
The first real event must be chosen only after confirming that the required Murphy evidence exists for that exact pre-2025 `as_of`. Do not force an event timestamp merely because an unrelated Murphy file contains that date.

## Completion criterion
Murphy binding is complete only when the selected event can carry the governed full Murphy evidence envelope expected by the existing Decision Boundary, with provenance intact.

## Next action
Perform a strict timestamp/rule-coverage join using the uploaded archive and identify the earliest valid pre-2025 candidate event that has sufficient governed Murphy evidence. Then join Nison, PIT Memory, TIZ state, Risk, and execute the existing Gate 3C assembler.
