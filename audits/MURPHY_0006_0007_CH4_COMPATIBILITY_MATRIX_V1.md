# MURPHY 0006/0007 — CHAPTER 4 COMPATIBILITY MATRIX V1

Date: 2026-08-14
Status: GOVERNANCE INPUT — NOT PRODUCTION FROZEN

## Source basis
Supplied John Murphy Chapter 4 project source artifacts and the existing 0006/0007 operational contract.

## Compatibility matrix

| Murphy Chapter 4 semantic | Current project contract | Status | Boundary |
|---|---|---|---|
| Up trendline connects successive reaction lows | 0006 uses LOW-family pivots and UP geometry | COMPATIBLE | Semantic mapping; source-lock of original rule record still required |
| Down trendline connects successive reaction highs | 0007 uses HIGH-family pivots and DOWN geometry | COMPATIBLE | Semantic mapping; source-lock of original rule record still required |
| Tentative trendline requires two points | Existing geometry provides two anchors | COMPATIBLE | Reuses canonical Geometry V1 |
| Confirmed trendline requires a third successful touch and reaction without breaking | Contract requires third touch, directional reaction, and line-hold | COMPATIBLE AT QUALITATIVE LEVEL | Exact deterministic meanings remain project operationalization |
| More successful tests increase trendline validity | Contract does not manufacture later touches after first failed eligible candidate | COMPATIBLE / CONSERVATIVE | This is an implementation guardrail, not verbatim source wording |
| Trendline should enclose the daily price range | Existing line-hold checks completed D1 bars | PARTIAL / OPERATIONALIZED | Exact source-to-code geometry equivalence is not separately source-locked |
| Murphy price-break filter examples include 3% | Contract does NOT bind 3% to 0006/0007 | CORRECT EXCLUSION | General example; no rule-specific authorization found |
| Murphy time-break filter example includes 2 consecutive daily closes | Contract does NOT bind 2-day to 0006/0007 | CORRECT EXCLUSION | General example; no rule-specific authorization found |
| Break/no-break is qualitative trendline semantics | Contract uses completed-D1 line-hold: UP low >= line; DOWN high <= line | OPERATIONALIZATION | Deterministic project choice, not verbatim Murphy numeric rule |
| Confirmation availability must respect pivot availability | Contract uses reaction availability timestamp | COMPATIBLE | No-lookahead gate |

## Explicit conclusions

1. Chapter 4 supports the qualitative structure needed for 0006/0007: trendline family, two anchors, third successful touch, reaction, and no meaningful break.
2. Chapter 4 does NOT establish a 0006/0007-specific numeric tolerance for touch, reaction magnitude/duration, or no-break.
3. The 3% and 2-day examples are retained as general Murphy breakout/filter concepts only. They are NOT automatically binding for 0006/0007.
4. The current deterministic clauses (event ordering, first eligible same-family third-touch candidate, D1 range intersection, opposite-family reaction, completed-D1 line-hold, availability timing) are project operationalization and must remain labeled as such.
5. No ATR, pip tolerance, arbitrary percentage, fixed lookback, or 2025 tuning is authorized.

## Governance decision required
The remaining question is not whether the current operator is compatible with Murphy's qualitative semantics; it is whether the project governance authority accepts this explicit operationalization as the smallest deterministic contract for 0006/0007.

Until that decision is recorded:
- QA may remain PASS for the current candidate;
- production confirmation remains NOT_FROZEN;
- no semantic change should be made merely to improve historical counts.

## Evidence boundary
This matrix does not claim that the original Rule Registry records for MURPHY_0006/MURPHY_0007 have been recovered. If those records are found, this matrix must be rechecked against their exact fields before freeze.
