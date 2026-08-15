# MURPHY STATUS SUPERSESSION MAP V1

Date: 2026-08-15
Authority: **Status-history routing / anti-confusion layer**

## Purpose
Prevent historical handoffs, backups, snapshots, and old progress files from being mistaken for the current Murphy 51 status.

This file does NOT replace rule contracts or evidence. It only controls **which status source wins when answering current-status questions**.

## Mandatory status precedence
When answering any question about current Murphy rule status, frozen count, remaining rules, or next rule, use this precedence:

1. `project_state/MURPHY_51_CANONICAL_RULE_STATUS_REGISTRY_V1.md` — CURRENT STATUS AUTHORITY.
2. A rule's latest dedicated Production Freeze / canonical provenance record, when drilling into that specific frozen rule.
3. Latest validated rule-specific evidence/QA artifacts.
4. Historical handoffs / backups / snapshots — **HISTORY ONLY**.

If a lower-priority historical source conflicts with a higher-priority current source, the historical source MUST NOT downgrade the current status.

## Explicit example: Murphy 0008
Historical files may state that 0008 was waiting on PF-B1 / PF-H1 governance.
That statement is historical and must not be used as the current status after the validated PF-B1/PF-H1 path was promoted and merged.

Current status of 0008: **PRODUCTION FROZEN**.

Evidence of the later promotion path:
- PR #10: `promote: Murphy 0008 validated path to production freeze review`
- PF-H1 and PF-B1 were explicitly defined in the promotion review.
- Validation reported 344 confirmed LOW Support candidates, 326 first-close break candidates, 242 immediate second-close confirmations, 0 availability violations, 0 confirmation chronology violations, 0 retest-before-confirmation violations, 0 2025 confirmations, 233/242 later retests, and 229/242 later role-reversal evidence.
- The PR was merged into `main` on 2026-08-15.

Therefore an older 0008 handoff saying “PF-B1 pending” must be labeled/treated as historical, not current.

## Current canonical headline
- Murphy rules: **51**
- Production Frozen: **12**
- Remaining: **39**
- Next: **0030**

Frozen: `0003, 0004, 0006, 0007, 0008, 0021, 0022, 0023, 0025, 0026, 0028, 0029`.

## Required behavior for every chat/agent
If a historical handoff is opened first:
- STOP before answering current status.
- Read the Canonical Rule Status Registry.
- Reconcile the historical statement against the registry.
- Use the registry for the current answer.
- Mention the historical conflict only if it materially explains the discrepancy.

Never answer “0008 is the current rule” merely because an old handoff says so.
Never answer “11/51” from an older snapshot when the current registry says 12/51.
Never reopen a frozen rule because an old handoff shows unfinished work that has since been superseded.

## Historical-source banner standard
When practical, prepend a historical file with:

`HISTORICAL SNAPSHOT — DO NOT USE FOR CURRENT MURPHY STATUS. Read MURPHY_51_CANONICAL_RULE_STATUS_REGISTRY_V1.md first.`

If a file cannot safely be edited because it is an immutable archive, this map is the authoritative supersession instruction.

## Update rule
Whenever a newer production-freeze or canonical status decision supersedes a historical state, add a short supersession entry here and update the Canonical Rule Status Registry in the same workflow.

## Next
After this anti-confusion layer is in place, work proceeds from **0030 Compatibility Audit**. Do not re-audit 0008 merely because an old handoff still contains PF-B1 work-in-progress language.
