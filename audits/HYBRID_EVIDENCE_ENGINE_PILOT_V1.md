# Hybrid Evidence Engine — Murphy Pilot V1

Status: PROPOSAL / PILOT ONLY
Date: 2026-08-16

## Goal
Test whether descriptive Murphy concepts can be operationalized as engineering evidence without changing canonical rule meaning.

## Pilot scope
Use three descriptive concepts from the current Murphy rule queue:
1. Horizontalness of a boundary/level.
2. Convergence of two boundaries.
3. Breakout significance / relative penetration.

These are pilot concepts, not new Murphy rules.

## Architecture
### Canonical layer
Only source-supported facts are represented here:
- required structure exists;
- direction/order/sequence conditions pass;
- canonical breakout event exists when the rule requires one.

Canonical failure cannot be overridden by engineering evidence.

### Engineering layer
Versioned evidence functions measure descriptive concepts without claiming source authorship:
- ENG_HORIZONTALNESS_V1
- ENG_CONVERGENCE_V1
- ENG_RELATIVE_PENETRATION_V1

Each produces an ordinal evidence grade LOW/MEDIUM/HIGH plus raw measurements and provenance. No production decision is emitted.

## Parameter policy
Parameters must be pre-declared and versioned. They may not be selected by maximizing 2019–2024 profitability or any trading outcome. 2025 is excluded entirely from tuning/selection.

Initial pilot deliberately avoids a learned model. Use deterministic normalized geometry/relative measures and simple monotonic membership functions only where needed. Similarity Memory remains a separate historical-evidence module.

## Acceptance tests
1. Canonical semantics unchanged.
2. Engineering evidence cannot override a failed hard gate.
3. No future timestamps/values enter an evidence record.
4. Prefix replay invariance.
5. Future-suffix mutation invariance.
6. Parameter provenance recorded.
7. 2016–2018 calibration/warm-up only.
8. 2019–2024 evaluation only.
9. 2025 excluded from tuning/selection.
10. Pilot does not generate BUY/SELL.

## Promotion rule
If the pilot demonstrates stable, auditable evidence without leakage or outcome-driven parameter selection, the architecture may be proposed for additional Murphy qualitative rules. If it fails, it is abandoned without changing canonical rules.
