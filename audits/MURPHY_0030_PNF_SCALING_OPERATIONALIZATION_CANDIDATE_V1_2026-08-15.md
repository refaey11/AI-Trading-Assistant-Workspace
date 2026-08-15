# Murphy 0030 — P&F Scaling Operationalization Candidate V1
Date: 2026-08-15
Status: CANDIDATE ONLY — NOT FROZEN / NOT PRODUCTION

## Purpose
Define a reproducible candidate for the missing GBPUSD P&F box-scaling parameter without claiming it is Murphy/Tower source text and without using historical trading outcomes for selection.

## Source evidence
- Murphy describes Kenneth Tower's logarithmic P&F method and says a 3-year volatility screening process determines the percentage box size for each stock.
- Murphy provides examples (AOL 3.6%, Intel 3.2%) but does not publish the screening formula in the audited text.
- External P&F references document percentage/logarithmic box sizing and describe 1% as a reasonable starting point for log-scaled P&F analysis. This is external methodology, not Murphy authority.

## Candidate configuration
- Representation: logarithmic / percentage P&F.
- Reversal: 3 boxes, because the Murphy 0030 source mapping uses 3-box reversal.
- Price construction: High/Low, consistent with the Murphy construction mapping.
- Candidate box percentage: 1.0%.
- Sampling candidate: completed D1 OHLC, because the audited Murphy construction for the relevant P&F implementation is based on High/Low and the project already has canonical D1 lineage.

## Provenance boundary
The 1.0% value is NOT claimed to be prescribed by Murphy or Kenneth Tower for GBPUSD. It is a project operationalization candidate derived from an external P&F convention. It must not be described as a Murphy rule.

## Selection rule
This candidate was NOT selected by backtest performance, 2025 results, or historical outcome optimization.
No alternative percentage may be compared on trading performance as part of this gate.

## Acceptance gate before use
1. Confirm the candidate P&F engine implements percentage/logarithmic scaling deterministically.
2. Confirm 3-box High/Low construction.
3. Confirm historical-prefix replay has identical P&F state prefixes.
4. Confirm no future-bar information changes an already emitted state.
5. Confirm availability timestamps are explicit.
6. Confirm the candidate does not alter Murphy semantic identity.
7. Governance must explicitly approve and freeze this operationalization before evaluator QA.

## Rejection conditions
Reject the candidate and return NOT_EVALUABLE if any of the following cannot be proven:
- deterministic construction;
- no-lookahead;
- reproducible availability;
- exact High/Low 3-box behavior;
- clear separation between source semantics and project operationalization.

## Important
This document does not freeze 0030 and does not authorize historical evaluation. It only converts the unresolved scaling question into a controlled, auditable candidate for compatibility testing.
