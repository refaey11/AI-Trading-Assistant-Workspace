# Murphy 0006/0007 Event-Based Confirmation Operator V1

Status: PROPOSAL / SOURCE-COMPATIBLE OPERATIONALIZATION CANDIDATE — NOT PRODUCTION FROZEN

## Purpose
Close the missing Confirmation Layer using only events already exposed by the canonical Pivot/Geometry/Evidence layers, without introducing ATR, pip, percentage, lookback, or fixed-bar thresholds.

## Source semantics preserved
- 0006: LOW reaction family + UP trendline + third successful touch + reaction away from line + line holds => bullish.
- 0007: HIGH reaction family + DOWN trendline + third successful touch + reaction away from line + line holds => bearish.

## Operational event chain
### 0006
1. Existing line is LOW/UP and has two defining anchors.
2. After line availability, the next confirmed LOW pivot is the third-touch candidate.
3. The completed D1 range of that pivot intersects the line: low <= line_price <= high.
4. The next confirmed opposite-family HIGH pivot is the reaction candidate.
5. Reaction direction is upward/away from an UP support line.
6. Between the touch event and reaction confirmation, subsequent completed D1 ranges do not violate the UP line (low >= line_price). The touch bar itself is allowed to intersect the line.
7. Confirmation availability is the reaction pivot's confirmed availability timestamp.

### 0007
Mirror of 0006:
1. Existing line is HIGH/DOWN and has two defining anchors.
2. After line availability, the next confirmed HIGH pivot is the third-touch candidate.
3. The completed D1 range intersects the line.
4. The next confirmed opposite-family LOW pivot is the reaction candidate.
5. Reaction direction is downward/away from a DOWN resistance line.
6. Between the touch and reaction confirmation, subsequent completed D1 ranges do not violate the DOWN line (high <= line_price). The touch bar itself may intersect.
7. Confirmation availability is the reaction pivot's confirmed availability timestamp.

## Provenance boundary
This operator does NOT claim Murphy specifies “next opposite-family confirmed pivot” or the exact post-touch interval predicate verbatim. These are deterministic representations of the already-established qualitative events and must pass compatibility review and historical QA before production freeze.

## Evidence basis
The existing candidate evidence run already selects the first confirmed same-type pivot after point 2, tests D1 range intersection, records the next confirmed opposite-type pivot as reaction candidate, and records directional consistency. The candidate population covers 2016–2024 only.

## Explicitly prohibited
- 3% as touch tolerance
- 2-day as reaction/no-break definition
- ATR/pip/percentage tolerance
- invented reaction magnitude
- invented lookback
- 2025 tuning
- lookahead before pivot availability

## Current gate
This file is an implementation proposal only. Production PASS/FAIL remains blocked until compatibility review, deterministic tests, and 2016–2024 historical QA pass.
