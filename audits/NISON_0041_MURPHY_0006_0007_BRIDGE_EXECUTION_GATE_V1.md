# Nison 0041 → Murphy 0006/0007 Bridge Execution Gate V1

Status: READY FOR RUNTIME REPLAY / NOT FROZEN

## Reuse decision
Nison 0041 must reuse the existing validated Murphy 0006/0007 trendline evidence layer. No new Trendline Geometry engine is created.

Existing project evidence:
- PIVOT_SEQUENCE_V2
- TRENDLINE_GEOMETRY_V1
- Murphy 0006/0007 confirmation/evaluator layer
- Nison confirmation/evidence adapter

## Causal pipeline
1. Canonical Pivot/Trendline evidence becomes available.
2. Murphy 0006/0007 structural confirmation is available.
3. Nison 0041 evaluates only the required candlestick confirmation at or after the structural evidence availability timestamp.
4. If confirmation evidence is earlier than its prerequisite event, fail closed.
5. Nison output remains evidence/confirmation and cannot create direction independently.

## Data gate
The project D1 File Library artifact is 2,544 rows covering 2016–2024 and excludes 2025 from the replay policy. The current search-accessible artifact confirms timestamp/OHLC and D1 fields, but the complete CSV bytes are not mounted in the current runtime. Therefore a full 0041 historical replay is not falsely claimed in this commit.

## Required runtime test
Run the bridge on the complete D1 bytes and report:
- structural Murphy confirmations consumed;
- Nison 0041 confirmations;
- NOT_EVALUABLE cases and reasons;
- availability violations;
- causal/no-lookahead violations;
- 2025 rows consumed (must be 0).

## Governance
No ATR, pip, percentage, body, lookback, tolerance, or trend proxy is introduced by this bridge. Existing project source/contract semantics remain authoritative. If a required Nison-specific confirmation field is unavailable, return NOT_EVALUABLE rather than infer PASS.
