# Local Project Archives — Rule Source Discovery Audit

Date: 2026-08-21
Status: SOURCE ARTIFACTS LOCATED / EXACT 79-ROW RUNTIME MANIFEST NOT YET LOCATED

## Correction to previous search boundary
The previous Dropbox keyword search failed to locate a directly named `79_RULE` artifact. That did not mean the underlying source material was absent. The current project workspace contains the uploaded project archives directly, including:
- `AI_Trading_Assistant_MASTER_KB_V1.zip`
- `AI_Trading_Assistant_3_BOOK_INTEGRATION_V1.zip`

These archives were inspected directly.

## Three-Book Integration contract located
Inside `AI_Trading_Assistant_3_BOOK_INTEGRATION_V1.zip`:
`01_Integrated_Knowledge/04_Integration_Layer/THREE_BOOK_INTEGRATION.json`

The source contract defines:
- Murphy role: Market structure and technical framework.
- Steve Nison role: Candlestick evidence and price-action confirmation.
- Trading in the Zone role: Execution psychology and process discipline.

Its declared decision flow is:
1. Murphy determines whether a technically valid market context/setup exists.
2. Nison provides candlestick confirmation or rejects weak price-action confirmation.
3. Trading in the Zone supplies an execution/process gate; psychology never creates a trade signal by itself.
4. Risk Engine calculates whether the trade is executable.
5. Decision Engine returns BUY, SELL, or NO_TRADE.
6. Every decision is logged.

## Master KB source evidence
`AI_Trading_Assistant_MASTER_KB_V1.zip` contains extensive source-rule material, including Murphy technical-analysis content and Nison candlestick formation/trading-rule files. The archive itself demonstrates that the knowledge source corpus exists in the current project workspace.

## Compatibility with current project authority
The source archives support the role boundaries already established by the authoritative project state:
- Murphy = technical context/market structure.
- Nison = confirmation/contradiction; not standalone direction.
- Trading in the Zone = process/psychology gate; never direction generation.

These semantics are also compatible with the existing `rule_adapter_contract_v1.json` precedence model.

## Important limitation
This direct archive inspection has NOT yet located a single explicit runtime manifest containing exactly the authoritative 79 row identities. Therefore this audit must not claim that all 79 rules were already executed through the adapter.

Current distinction:
- Source corpus / integration semantics: LOCATED and evidenced.
- Exact 79-rule provenance manifest for runtime allow-list: NOT YET LOCATED in the inspected archives.

## Consequence for the adapter
The existing Rule Adapter can be audited against real source semantics now, but a strict `79-only` runtime allow-list still requires the authoritative manifest/provenance file.

Do not substitute the full Master KB or the older 102-rule registry as an automatic runtime allow-list.

## Next safe action
Search the remaining project archives and workspace audit artifacts for the exact 79-rule provenance manifest, using identifiers, counts, and audit terms rather than only the literal filename `79_RULE`.

After locating that manifest:
1. derive/verify the allow-list;
2. run the existing Rule Adapter against representative accepted and rejected inputs;
3. prove source_rule_id traceability;
4. record test evidence before any end-to-end integration.

## Governance preserved
- No rebuild of completed knowledge modules.
- 2025 remains final OOS and is never used for tuning/calibration.
- Similarity remains historical evidence only.
- Volume unavailable is not treated as zero volume.
