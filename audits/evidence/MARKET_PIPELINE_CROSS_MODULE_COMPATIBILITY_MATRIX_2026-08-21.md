# Market Pipeline — Cross-Module Compatibility Matrix
Date: 2026-08-21
Status: AUDIT COMPLETE — GAP REGISTER

## Modules audited
1. MARKET_READER_V1
2. MARKET_STATE_READER_V1
3. MARKET_SCENARIO_ENGINE_V1
4. MULTI_TIMEFRAME_READER_V1
5. Time / Dynamic Timeframe Context

## Compatibility matrix

| Boundary / capability | Evidence status | Compatibility verdict | Required action |
|---|---|---|---|
| Market Reader -> Market State | Both contracts/outputs audited, but runtime generator provenance unavailable | PARTIAL | Do not rebuild; preserve as provenance/evidence gap |
| Market State -> Scenario | Scenario artifacts contain market_state inputs | COMPATIBLE AT ARTIFACT LEVEL | Runtime lineage still unproven |
| Knowledge -> Scenario | Retrieved knowledge + scenario analysis artifacts present | COMPATIBLE AT ARTIFACT LEVEL | Knowledge quality/alignment belongs to next phase |
| MTF -> Project pipeline | H4/H1 module scope proven | COMPATIBLE WITH MODULE SCOPE | Preserve separately proven project-level six-timeframe evidence |
| Six-timeframe architecture | Already proven/recorded at project level | PASS | Do not downgrade because one module is H4/H1-only |
| Time / Dynamic TF context | No standalone contract/module found | MISSING AS STANDALONE COMPONENT | Treat as explicit architecture gap; define later only after compatibility review |
| Volume availability semantics | Upstream evidence exists for confirmed 2020-2024 window; historical Market State handling remains inconsistent | PARTIAL | Preserve explicit UNAVAILABLE != 0 semantics; do not fabricate |
| AS-OF / completed-bar provenance | Archived outputs alone cannot prove runtime semantics for several modules | UNPROVEN | Register provenance gap; do not claim no-lookahead PASS |
| 2016-2024 QA window | Historical outputs cover required period | PASS FOR COVERAGE | Use for development/QA only |
| 2025 | Present in historical artifacts | OOS RESERVED | Never use for tuning; final evaluation only |

## What the full audit proved
- The five audited components exist as distinct project artifacts or evidenced architecture elements.
- The project has real historical outputs for major market-reading stages.
- Scenario artifacts already consume market-state and retrieved-knowledge structures at the artifact level.
- The six-timeframe architecture remains proven/recorded separately at project level.
- MULTI_TIMEFRAME_READER_V1 is correctly scoped to H4/H1 and must not be misclassified as a failed six-timeframe implementation.

## True gaps after cross-module review

### G1 — Runtime provenance / AS-OF evidence
Several archived modules contain outputs and contracts but not the source generator needed to prove completed-bar semantics and strict no-lookahead.

Classification: EVIDENCE / PROVENANCE GAP.

Action: Do not rebuild modules solely for this reason. Preserve as an explicit gate for any runtime integration.

### G2 — Volume availability semantics
The project must preserve the distinction:
`volume unavailable != volume zero`

Confirmed 2020-2024 upstream volume evidence must not be silently erased; periods without confirmed source must remain unavailable/not-evaluable rather than converted into market conclusions.

Classification: DATA/CONTRACT GAP.

Action: Resolve at the integration boundary with the smallest compatible adapter after source lineage is available; no blanket module rewrite.

### G3 — Standalone Time / Dynamic Timeframe Context
No separately auditable standalone contract/component was found in the audited artifacts.

Classification: ARCHITECTURE GAP.

Action: Keep explicit and open. Do not invent implementation now. Revisit after Knowledge Alignment and before final Decision Brain integration so the contract is driven by the complete pipeline.

## Pipeline audit verdict

```text
COMPONENT AUDIT: COMPLETE
ARTIFACT-LEVEL COMPATIBILITY: PARTIAL / MOSTLY COMPATIBLE
GAPS: 3 REGISTERED (G1 provenance, G2 volume semantics, G3 time/dynamic context)
BLOCKER TO KNOWLEDGE ALIGNMENT: NO
```

## Freeze / resume rule
Do not reopen individual module audits unless a downstream compatibility test produces new evidence.

The project now moves to the next planned phase:
**Murphy + Nison + Trading in the Zone -> Knowledge Alignment**.

Before any integration, perform a compatibility audit of existing knowledge artifacts. Do not rebuild existing project knowledge from scratch. Murphy provides technical context/market structure; Nison provides confirmation; Trading in the Zone provides psychology/process gating and must not generate market direction. Historical similarity/memory remains evidence only and never the sole decision-maker.
