# AI Trading Assistant — Decision Brain
## Current Project Status — 2026-08-12

### Purpose
This file records the latest verified stopping point so future work resumes from the exact current state instead of rebuilding or guessing.

### Source-of-truth policy
- Workspace / File Library artifacts are the project source of truth.
- GitHub is the development/provenance mirror and must not silently replace Workspace truth.
- Existing components must be audited and integrated, not rebuilt.
- Compatibility audit is required before any new integration.
- 2025 is OOS and must never be used for tuning or implementation selection.

### Architecture status
- John Murphy technical context / market structure: integrated work exists.
- Steve Nison: integrated confirmation knowledge exists.
- Trading in the Zone: psychology/process gate; it cannot generate market direction.
- Similarity / Historical Memory: historical evidence only; it cannot be the sole decision maker.
- Decision Brain: combines current market evidence, book knowledge, historical memory, and risk.
- Existing Trendline Geometry V1 is an upstream primitive and must not be rebuilt.

### Current blocking item
MURPHY_0006 and MURPHY_0007 remain `NOT_YET_EVALUABLE`.

Both currently carry the registry wording:
`A third successful touch and reaction confirms the trendline.`

The exact operational semantics have NOT been proven yet for:
- successful touch
- reaction after touch
- third touch vs. subsequent reaction as the confirmation event
- exact availability timestamp
- chronology / no-lookahead details
- the source-defined distinction between 0006 and 0007

Do NOT infer 0006 = bullish or 0007 = bearish from numbering.

### Required next sequence
`authoritative source semantics → compatibility audit against Trendline Geometry V1 → availability/no-lookahead contract → evaluator → unit tests → 2016–2024 historical QA → freeze`

### Explicitly prohibited before source contract is frozen
- inventing touch tolerances
- inventing ATR/percentage thresholds
- inventing lookbacks
- inferring direction from rule numbering
- implementing an evaluator around guessed semantics
- tuning on historical data before the source contract is frozen
- using 2025 for tuning

### Historical Memory / project assets
The latest GitHub release `workspace-v1` was updated on 2026-08-12 and contains the project backup plus multiple component assets, including the 3-book integration, AI Decision Engine, API, backtest, Historical Memory, Feature Engineering, Market Structure, and Master Evidence related assets. The large `HISTORICAL_MEMORY_V1.zip` asset is present in the release; its binary contents are not to be treated as inspected merely from asset metadata.

### Exact stopping point
The project is stopped immediately BEFORE the final compatibility audit of 0006/0007 against the existing Trendline Geometry V1, pending recovery of authoritative original rule/database records that distinguish the two rules and define the confirmation operator.

### Resume rule
When resuming, first recover and verify the authoritative 0006/0007 source records. Do not jump directly to evaluator implementation. Preserve all existing components and contracts.
