# Murphy 0006–0007 Source Deep Audit V2
Date: 2026-08-13

## New source evidence recovered
The uploaded Murphy Chapter 4 source contains a concrete trendline illustration describing the third test:
- A temporary trendline is drawn between two points.
- The line is tested for a third time at point 5 to confirm its validity.
- The text describes an uptrend line drawn upward through lows from which price rebounded.
- After the third test, price rebounds again from the line and the line is maintained without penetration.
- The chapter also explains that a trendline's importance depends on how long it remains unbroken and how many successful tests it receives.

This is stronger source evidence for the EVENT SEQUENCE than the prior registry wording alone:
TWO ANCHORS → THIRD TEST → REBOUND/REACTION → LINE MAINTAINED WITHOUT PENETRATION.

## What this proves
1. The third test is a separate event after the two defining anchors.
2. The third test is associated with a subsequent rebound/reaction away from the trendline.
3. The example explicitly describes the line remaining valid without penetration after the reaction.
4. Successful tests increase trendline validity/importance.

## What this does NOT prove
The source illustration still does NOT supply a production numeric/operator contract for:
- price-to-line touch tolerance;
- minimum reaction magnitude;
- reaction duration/bar count;
- exact rule-specific no-break threshold;
- exact confirmation availability timestamp.

Therefore this source evidence cannot be converted into a deterministic PASS predicate without adding unsupported semantics.

## Important additional source point
The chapter's general two-day / 3% break examples are not a binding 0006/0007 operator. The source text itself distinguishes those general price/time filters from the major trendline context; the project handoff already records that they must not be automatically assigned to 0006/0007.

## Compatibility conclusion
Existing PIVOT_SEQUENCE_V2 and TRENDLINE_GEOMETRY_V1 remain reusable. Geometry supplies the two anchors and line availability but intentionally excludes breakout detection. The smallest missing layer remains a source-safe confirmation operator above Geometry.

Current status:
- Source event sequence: strengthened / CLOSED qualitatively.
- Third-touch production predicate: OPEN.
- Reaction production predicate: OPEN.
- No-break production predicate: OPEN.
- Confirmation timing: OPEN.
- 0006/0007 production: NOT_EVALUABLE.

No components were rebuilt or modified by this audit.
2025 remains OOS and excluded from tuning/selection.