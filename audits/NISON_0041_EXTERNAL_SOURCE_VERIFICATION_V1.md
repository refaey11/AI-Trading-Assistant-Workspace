# Nison 0041 — External Source Verification V1

Date: 2026-08-17

## Purpose
Verify whether the four currently qualitative Nison 0041 pattern families have source-supported operational criteria, without tuning against project data.

## External verification findings

### Hammer
Google Books and searchable reproductions of Steve Nison's Japanese Candlestick Charting Techniques report three core criteria: real body at the upper end of the range; long lower shadow at least twice the real body; no or very short upper shadow. The source also notes that longer lower shadows and smaller bodies make the pattern more meaningful. Google Books: https://books.google.com/books/about/Japanese_Candlestick_Charting_Techniques.html?id=rbn8NeXOYV4C
A searchable reproduction states the same criteria and explicitly describes the two-times lower-shadow condition. These are source-derived criteria, not thresholds learned from project data.

### Shooting Star
Searchable Nison-derived material identifies: market in uptrend; small real body near the bottom of the session; upper shadow at least twice the real body; very small lower shadow acceptable. Nison's text also describes the body color as non-essential. This provides an operational core predicate, with the caveat that Nison treats candlestick guidelines as non-rigid rather than mathematical guarantees.

### Morning Star
Searchable Nison source material identifies: downtrend; tall/long black first real body; small second real body that gaps lower to form a star; third white real body moving well into the first black real body. Nison describes gaps as ideal/strengthening rather than always mandatory. The source also notes that lack of the second gap does not necessarily invalidate the formation.

### Evening Star
Searchable Nison educational material identifies the mirror structure: market in uptrend; first long white candle; second small real body that does not or only slightly overlaps the first body; third black candle that gets deeply into the first real body. Gap characteristics are described as factors that strengthen the pattern rather than unconditional requirements.

## Critical governance conclusion
External research confirms that the four patterns have more detailed source criteria than the previous adapter contract captured. However, several terms remain intentionally qualitative in Nison's treatment (small, long/tall, deeply/well into, ideal gap), and Nison explicitly describes candlestick interpretation as guidelines rather than rigid rules in the book's visual summary.

Therefore the correct project treatment is:
- promote exact source-stated relationships (for example, Hammer lower shadow >= 2x real body; Shooting Star upper shadow >= 2x real body) into the canonical pattern contract;
- do not invent numerical definitions for qualitative terms such as "small" or "deeply into";
- preserve optional/ideal gaps as source-qualified features, not mandatory rules unless the specific source clause says mandatory;
- do not tune these definitions on 2016–2024 outcomes;
- 2025 remains excluded.

## Verdict
EXTERNAL SOURCE SUPPORT = CONFIRMED
CANONICAL CONTRACT REVISION = JUSTIFIED
FULL DETERMINISTIC EVALUATION = STILL PARTIAL until qualitative terms are either source-locked by an existing canonical Nison contract or explicitly retained as NOT_EVALUABLE.
