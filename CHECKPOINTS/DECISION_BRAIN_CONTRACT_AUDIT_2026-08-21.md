# Decision Brain Contract Audit Checkpoint

Date: 2026-08-21
Status: RECORDED CHECKPOINT — no runtime implementation changed

## Confirmed Architecture Finding

The existing Decision Brain V1/V1.1 is the synthesis layer for current market evidence and normalized knowledge/historical evidence. It must not be rebuilt from scratch.

### Current Market Evidence enters the Decision Brain directly

The current-market side includes:

- M5
- M15
- M30
- H1
- H4
- D1
- MTF / Dynamic Timeframe Context
- volatility context
- volume availability, with the guard `volume unavailable != zero`
- current price action / market-state context
- AS-OF / timestamp discipline

This supersedes the earlier simplified H1/H4-only understanding. Existing Dynamic MTF / Timeframe findings are preserved and must be traced source-faithfully at final runtime binding; no timeframe roles are to be invented.

## Rule Adapter Boundary

The Rule Adapter is not the mandatory entry point for all current market evidence. Its primary role is to normalize existing rule/knowledge outputs into Decision Brain evidence.

Therefore, do not modify the Rule Adapter merely to force the full current market state through it.

## Current Integration Shape

```text
CURRENT MARKET EVIDENCE
M5 / M15 / M30 / H1 / H4 / D1
+ Dynamic MTF / Time Context
+ Volatility
+ Volume Availability
+ Price Action
          |
          v
     DECISION BRAIN
          ^
          |
NORMALIZED KNOWLEDGE / HISTORICAL EVIDENCE
- Murphy: only the 35 officially closed rules; primary technical context
- Nison: closed output; confirmation / contradiction only; must not create direction alone
- Historical Evidence: evidence only; must not determine direction alone
```

## Trading in the Zone

Status: PARKED / DEFERRED.

Trading in the Zone was attempted but was not closed as a source-faithful runtime mapping without inventing thresholds or unsupported rules. It is therefore excluded from the current runtime validation and must not be represented as an active PASS/FAIL process gate until it is properly completed.

## Historical Integration

Historical / Similarity integration remains evidence-only. Existing Run 070 PASS is preserved, but its next integration gate is to replace synthetic Decision Brain input with a real current-market row and official knowledge outputs for end-to-end validation.

## Next Correct Step

Build the final compatibility matrix for the end-to-end smoke test:

1. Map a real Market Reader row to the actual Decision Brain inputs.
2. Bind the verified M5/M15/M30/H1/H4/D1 + Dynamic MTF/Timeframe context source-faithfully.
3. Feed Murphy using only the 35 officially closed rules.
4. Feed Nison as confirmation / contradiction only.
5. Reuse the existing Historical evidence path.
6. Keep Trading in the Zone out of the current runtime test.
7. Run the first real end-to-end smoke test.
8. If a schema gap is proven, create only the smallest compatibility adapter required.

## Governance

- No rebuild of existing Decision Brain.
- No invented MTF aggregation or timeframe roles.
- No future leakage.
- 2025 remains OOS and must not be used for tuning.
- Similarity / Historical evidence is not a standalone decision maker.
- Record each completed project step immediately in GitHub and Dropbox before proceeding to the next major step.
