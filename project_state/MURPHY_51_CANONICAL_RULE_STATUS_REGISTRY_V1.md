# MURPHY 51 — CANONICAL RULE STATUS REGISTRY V1

Date: 2026-08-15
Authority: **Canonical project-status registry**

## Purpose
This file is the single authoritative lookup for questions of the form:
- “What Murphy rules are left?”
- “How many Murphy rules are finished?”
- “What is the next Murphy rule?”
- “Which Murphy rules are frozen?”
- “What is the current status of Murphy 51?”

Do NOT answer those questions from model memory, old chat handoffs, old snapshots, or inferred status.

## Mandatory lookup procedure for every chat/agent
1. Read this registry first.
2. Treat the status in this registry as authoritative for the 51-rule status question.
3. If a rule is marked FROZEN, do not reopen or rework it unless new contradictory evidence or an approved semantic change exists.
4. For a specific rule's technical details, then read that rule's canonical contract/provenance/backup.
5. If an older artifact conflicts with this registry, report the conflict but do not downgrade the current status from the older artifact.
6. Never invent a rule status from absence of a file.
7. 2025 is OOS and must not be used for tuning, selection, calibration, optimization, or status decisions.

## Current headline state
- Total Murphy rules: **51**
- Production Frozen: **12**
- Remaining / not yet Production Frozen: **39**
- Current next rule: **0030**
- Frozen rules are CLOSED and must not be reworked as routine cleanup.

## Production Frozen — 12/51
| Rule | Status | Action |
|---|---|---|
| 0003 | PRODUCTION FROZEN | CLOSED |
| 0004 | PRODUCTION FROZEN | CLOSED |
| 0006 | FROZEN — EVALUATOR + DECISION-BRAIN-EVIDENCE LEVEL | CLOSED at this governance level |
| 0007 | FROZEN — EVALUATOR + DECISION-BRAIN-EVIDENCE LEVEL | CLOSED at this governance level |
| 0008 | PRODUCTION FROZEN | CLOSED |
| 0021 | PRODUCTION FROZEN | CLOSED |
| 0022 | PRODUCTION FROZEN | CLOSED |
| 0023 | PRODUCTION FROZEN | CLOSED |
| 0025 | PRODUCTION FROZEN | CLOSED |
| 0026 | PRODUCTION FROZEN | CLOSED |
| 0028 | PRODUCTION FROZEN | CLOSED |
| 0029 | PRODUCTION FROZEN | CLOSED |

## Remaining — 39/51
The remaining set is exactly:

**0001, 0002, 0005, 0009, 0010, 0011, 0012, 0013, 0014, 0015, 0016, 0017, 0018, 0019, 0020, 0024, 0027, 0030, 0031, 0032, 0033, 0034, 0035, 0036, 0037, 0038, 0039, 0040, 0041, 0042, 0043, 0044, 0045, 0046, 0047, 0048, 0049, 0050, 0051**

### Next queue position
**0030 is the next rule to audit.**

No work should jump to another remaining rule unless the project explicitly changes scope.

## Status semantics for the remaining set
For a remaining rule, use the project's latest authoritative evidence to assign one of these states when supported:
- NOT_EVALUABLE — required evidence/contract is insufficient for evaluation.
- PARTIAL — some required components/evidence exist, but a freeze gate remains.
- IN_PROGRESS — active work is currently being performed.
- BLOCKED — a known dependency or governance blocker prevents completion.
- FREEZE_CANDIDATE — technical gates are passed but explicit governance freeze remains.
- PRODUCTION FROZEN — all required gates and governance freeze are complete.

Do not convert NOT_EVALUABLE/PARTIAL/BLOCKED into a guessed completion state.

## Freeze rules / global governance
- Existing components must be audited and integrated before any rebuild.
- Compatibility audit is required before new integration.
- Do not invent operators, thresholds, tolerances, timeframes, lookbacks, proxies, or semantic definitions.
- 2025 is OOS and must never be used for tuning/selection/calibration/optimization.
- NOT_EVALUABLE is preferred over fabricated evidence.
- Similarity Memory is historical evidence only and never the sole decision maker.
- Trading in the Zone is psychology/process gate and cannot generate direction.
- Murphy supplies technical context/market structure; Nison supplies confirmation.

## Anti-confusion rule
If asked only “what is left?”, answer from the **Remaining — 39/51** list above.
If asked “what is next?”, answer **0030**.
If asked “how many are frozen?”, answer **12/51**.
If asked for a specific rule, use this registry for its headline state and then open the rule-specific evidence.
Never use an older count such as 10/51 or 11/51 when this registry is available.

## Continuity reference
The companion package `MURPHY_12_FROZEN_CONTINUITY_BACKUP_V1` records the problems, solutions, evidence, boundaries, and do-not-repeat instructions for the 12 frozen rules.

## Update rule
Whenever a rule changes status, update THIS registry in the same change set as the rule's canonical freeze/provenance record. A status change is not considered complete until this registry is updated.
