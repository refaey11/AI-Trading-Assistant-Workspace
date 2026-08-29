# Murphy 34 Source Coverage Ledger — 2026-08-29

## Purpose
Map the official 34 runtime-verified Murphy rules to the user-supplied Murphy source/evidence archive before any Decision Brain integration. This is an inventory/audit only; no Murphy semantics are changed.

## Official runtime boundary
The frozen allowlist defines 34 Murphy runtime-verified rules and 44 Nison rules, total 78. Murphy 0008 is blocked and is not part of the 34-rule runtime set.

## Supplied Murphy archive coverage
The current archive is `قواعد مورفي  2(6).zip` and contains grouped evidence/freeze/replay packs. The grouped packs cover the following 30 of the 34 runtime-verified Murphy rules:

- 0003, 0004 — grouped frozen backup
- 0006, 0007 — real-data candidate evidence + final freeze review pack
- 0021, 0022, 0023 — clean historical evaluation pack
- 0028, 0029 — RSI/divergence recovery and QA packs
- 0030, 0031, 0032 — grouped freeze backup
- 0033 — local freeze pack
- 0034–0045 — grouped production freeze / replay / evaluator / adapter QA pack (12 rules)
- 0047, 0048, 0049 — ingestion + closed-final replay pack
- 0050, 0051 — final closure pack

Total directly/group-covered by this archive: 30/34.

## Four runtime-verified Murphy rules not found as dedicated evidence packs in the supplied Murphy archive
- MURPHY_0018 — Falling wedge
- MURPHY_0019 — Rising wedge
- MURPHY_0025 — Four-week breakout
- MURPHY_0026 — Four-week breakdown

These four rules do exist in the broader Master Knowledge Base candidate-rule registry, but that registry records them as candidate / UNTESTED and is not equivalent to historical evidence production.

## Interpretation
This is NOT a reason to rebuild Murphy. It is a source-coverage gap:

30/34 = archive evidence/freeze coverage
4/34 = candidate definitions present, dedicated runtime evidence not yet located in the current Murphy evidence pack

Before Gate 3C claims full 34-rule consumption, the four rules above must be located in an authoritative evidence producer/package or explicitly remain NOT_EVALUABLE. Do not invent synthetic evidence for them.

## Binding rule
Every Murphy rule enters the Decision Brain through its existing governed evidence producer/adapter. The integration layer may normalize transport fields and provenance, but may not rewrite rule semantics, invent thresholds, or create directional mappings.

## Next action
Search all existing project sources (GitHub/Dropbox/workspace archives) for authoritative evidence producers for 0018/0019/0025/0026. If found, bind them into the same full 34-rule envelope. If not found, preserve NOT_EVALUABLE and keep Gate 3C fail-closed for a claimed full-34 run.
