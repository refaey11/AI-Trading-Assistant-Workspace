# Canonical Book Rule Status Inventory V1

**Purpose:** Single governance inventory for the 102-rule book universe. This file records current canonical status and provenance boundaries without rewriting any book rule.

**Canonical-date policy:** Where older artifacts conflict with later authoritative closure/checkpoint records, the latest authoritative record takes precedence unless explicitly superseded by a newer canonical record.

## Totals

| Book | Total | Canonical current status |
|---|---:|---|
| John Murphy | 51 | 35 CLOSED/FROZEN, 16 OPEN/DEFERRED |
| Steve Nison | 44 | 44/44 FROZEN |
| Trading in the Zone | 7 | 7 DEFERRED / NOT YET AUTHORITATIVELY EVALUABLE |
| **TOTAL** | **102** | **79 frozen/closed + 23 not currently frozen** |

## 1. Murphy — 51 rules

- **35 rules:** canonical status = `CLOSED/FROZEN`.
- **16 rules:** canonical status = `OPEN/DEFERRED`.
- The 35 closed rules are preserved as existing source/evaluator evidence; they must not be rebuilt from scratch.
- The 16 remaining rules are not to be silently treated as closed or fabricated as substitutes.
- Integration eligibility: only closed/frozen authoritative outputs may enter the Rule Adapter as authoritative Murphy evidence.

## 2. Nison — 44 rules

Canonical checkpoint: **NISON = 44/44 FROZEN**.

- `001–038`: 38/38 candlestick-pattern source-contracts frozen.
- `039–044`: 6/6 methodology/context entries frozen separately.
- Nison remains **evidence / confirmation / context only**.
- Nison cannot create standalone trade direction.
- Older artifacts reporting Nison as open/incomplete are stale for current-status purposes unless a newer authoritative record explicitly supersedes the canonical checkpoint.
- Integration eligibility: frozen/source-locked Nison outputs may confirm or contradict an existing directional context; they may not create direction alone.

## 3. Trading in the Zone — 7 rules

Current canonical status: all seven are **DEFERRED** rather than frozen runtime rules.

- `PSY_0001` — `DEFERRED_NOT_EVALUABLE`
- `PSY_0002` — `DEFERRED_CANDIDATE_NOT_AUTHORITATIVE`
- `PSY_0003` — `DEFERRED_PROCESS_ONLY`
- `PSY_0004` — `DEFERRED_NOT_EVALUABLE`
- `PSY_0005` — `DEFERRED_NOT_EVALUABLE`
- `PSY_0006` — `DEFERRED_NOT_EVALUABLE`
- `PSY_0007` — `DEFERRED_CANDIDATE_NOT_AUTHORITATIVE`

Trading in the Zone remains a **psychology/process gate only** and must never generate BUY/SELL direction or independently reverse market direction. Deferred status does not block project continuation; unresolved rules remain unavailable until their specified authoritative evidence dependencies exist.

## Integration boundary

```text
Frozen Murphy evidence (35)
        +
Frozen Nison evidence (44)
        +
Trading in the Zone authoritative process evidence when available
        ↓
Rule Adapter (normalize; do not rewrite rules)
        ↓
Knowledge Alignment
        ↓
Contradiction / Process Gates
        ↓
Risk Engine
        ↓
Existing Decision Brain
```

## Hard governance

1. Do not rebuild existing frozen book knowledge from scratch.
2. Do not copy the 102 rules into a new Brain registry.
3. Use provenance references and existing authoritative outputs.
4. If status is unresolved or evidence is unavailable, return `ABSTAIN`, `UNAVAILABLE`, or `NEEDS_REVIEW`.
5. Nison cannot generate direction alone.
6. Trading in the Zone cannot generate direction.
7. Similarity remains historical evidence only and cannot override hard gates.
8. 2025 remains OOS and must not be used for tuning, calibration, threshold selection, or implementation selection.

## Current canonical inventory summary

**Murphy:** 35/51 closed.

**Nison:** 44/44 frozen.

**Trading in the Zone:** 0/7 frozen runtime rules; 7/7 formally deferred with explicit reasons and reopen dependencies.
