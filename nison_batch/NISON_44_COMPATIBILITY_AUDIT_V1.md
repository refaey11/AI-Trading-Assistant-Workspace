# Nison 44 — Compatibility Audit V1

## Scope
Batch audit of all 44 Steve Nison registry entries against the existing Nison project infrastructure. Audit only; no rule is frozen or rewritten.

## Source / infrastructure findings
- Integrated registry contains exactly 44 Steve Nison entries, all with `integration_role=confirmation`.
- Existing Nison Candlestick Confirmation V1 is explicitly an engineering prototype; it warns that exact Nison textual criteria/context still require source mapping before canonical use.
- Existing Nison Context Engine V1 uses engineering filters and explicitly states its thresholds are not canonical Steve Nison thresholds.
- Rules 0035–0038 have dedicated structural evaluator artifacts, but their closure reports leave qualitative/sessionization gates open.

## Governance
- Nison is confirmation-only and cannot create direction alone.
- No invented ATR/pip/%/lookback/tolerance/proxy becomes canonical.
- 2025 is excluded from tuning, selection, calibration and optimization.
- Existing components are reused only after compatibility is proven.
- Unit-test success does not equal production freeze.

## 44-rule audit matrix

| Rule | Name | Compatibility state | Decision |
|---|---|---|---|
| 0001 | Bullish Engulfing | PARTIAL_EXISTING_ENGINE | PARTIAL; exact source mapping + compatibility + QA required |
| 0002 | Bearish Engulfing | PARTIAL_EXISTING_ENGINE | PARTIAL; exact source mapping + compatibility + QA required |
| 0003 | Dark Cloud Cover | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0004 | Piercing Pattern | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0005 | On Neck | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0006 | In Neck | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0007 | Thrusting | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0008 | Morning Star | PARTIAL_EXISTING_ENGINE | PARTIAL; exact source mapping + compatibility + QA required |
| 0009 | Evening Star | PARTIAL_EXISTING_ENGINE | PARTIAL; exact source mapping + compatibility + QA required |
| 0010 | Morning Doji Star | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0011 | Evening Doji Star | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0012 | Abandoned Baby | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0013 | Harami | PARTIAL_EXISTING_ENGINE | PARTIAL; exact source mapping + compatibility + QA required |
| 0014 | Harami Cross | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0015 | Tweezers Top | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0016 | Tweezers Bottom | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0017 | Upside Gap Two Crows | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0018 | Three Black Crows | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0019 | Bullish Counterattack Lines | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0020 | Bearish Counterattack Lines | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0021 | Three Mountains | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0022 | Three Rivers | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0023 | Three Buddha Tops | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0024 | Three Buddha Bottoms | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0025 | Dumpling Top | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0026 | Fry Pan Bottom | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0027 | Tower Top | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0028 | Tower Bottom | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0029 | Unique Three River Bottom | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0030 | Three Rising Methods | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0031 | Three Falling Methods | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0032 | Three White Soldiers | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0033 | Advance Block (Stalled Pattern) | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0034 | Separating Lines | NO_APPROVED_CANONICAL_OPERATOR_FOUND | NOT_EVALUABLE until source-bounded contract |
| 0035 | Tasuki Gap | DEDICATED_STRUCTURAL_EVALUATOR | PARTIAL; qualitative comparator + QA/freeze gates open |
| 0036 | Gapping Play | DEDICATED_STRUCTURAL_EVALUATOR | PARTIAL; qualitative definitions + QA/freeze gates open |
| 0037 | Side-by-Side White Lines | DEDICATED_STRUCTURAL_EVALUATOR | PARTIAL; same-open/similar-body + QA/freeze gates open |
| 0038 | Windows | DEDICATED_STRUCTURAL_EVALUATOR | STRUCTURAL COMPATIBILITY PASS; freeze still pending |
| 0039 | Multiple Technical Techniques | TOPIC/CHAPTER RECORD | NOT_EVALUABLE; must be decomposed from source |
| 0040 | Candlestick Clusters | TOPIC/CHAPTER RECORD | NOT_EVALUABLE; must be decomposed from source |
| 0041 | Trend Lines | TOPIC/CHAPTER RECORD | NOT_EVALUABLE; must be decomposed from source |
| 0042 | Support/Resistance | TOPIC/CHAPTER RECORD | NOT_EVALUABLE; must be decomposed from source |
| 0043 | False Breakouts | TOPIC/CHAPTER RECORD | NOT_EVALUABLE; must be decomposed from source |
| 0044 | Polarity Principle | TOPIC/CHAPTER RECORD | NOT_EVALUABLE; must be decomposed from source |

## Specific findings
### 0001–0002, 0008–0009, 0013
Existing engineering infrastructure contains broad matching pattern families, but the source package itself says the prototype is not an exact reproduction of Nison. These remain compatibility candidates, not canonical evaluators.

### 0035–0038
Dedicated evaluators exist. Existing evidence says 0038 is structurally compatible, while 0035/0037 have unresolved qualitative comparators and 0036 has unresolved qualitative definitions. Historical replay evidence for 2016–2024 excludes 2025, but unresolved contracts prevent canonical freeze.

### 0039–0044
The registry records these as chapter/topic-level entries rather than closed deterministic rule contracts. They must be decomposed from the authoritative Nison material before any evaluator or direction logic is claimed. They must not be converted into generic scoring.

## Next batch
1. Source-map the remaining 35 entries in batches.
2. Decompose each rule into HARD_CANONICAL / QUALITATIVE_MEASURABLE / QUALITATIVE_UNMEASURABLE / EVIDENCE_ONLY clauses.
3. Reuse only compatible approved primitives through documented adapters.
4. Implement the smallest missing deterministic evaluator.
5. Run unit tests, 2016–2024 historical QA, availability/no-lookahead, then explicit freeze governance.

## Verdict
**44-rule inventory: PASS. Compatibility audit: PARTIAL / OPEN. Production freeze: NOT GRANTED.**