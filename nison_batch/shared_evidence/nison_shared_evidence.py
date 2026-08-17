from dataclasses import dataclass
from typing import Sequence

@dataclass(frozen=True)
class EvidenceEvent:
    kind: str
    timestamp: int
    direction: str = "neutral"
    source: str = ""
    independent: bool = True
    available: bool = True


def _ordered(events: Sequence[EvidenceEvent]) -> bool:
    return all(a.timestamp < b.timestamp for a, b in zip(events, events[1:]))


def cluster_evidence(events: Sequence[EvidenceEvent]) -> dict:
    """Nison 0040: evidence-only. Caller supplies canonical zone membership."""
    if not events or not all(e.available for e in events):
        return {"available": False, "direction": "neutral", "statement": "insufficient cluster evidence"}
    ordered = sorted(events, key=lambda e: e.timestamp)
    if not _ordered(ordered):
        return {"available": False, "direction": "neutral", "statement": "invalid chronology"}
    return {"available": True, "direction": "neutral", "statement": "candlestick cluster evidence present"}


def confluence_evidence(events: Sequence[EvidenceEvent]) -> dict:
    """Nison 0039: no invented score/count; requires independently supplied evidence."""
    usable = [e for e in events if e.available and e.independent]
    if not usable:
        return {"available": False, "direction": "neutral", "statement": "insufficient confluence evidence"}
    return {"available": True, "direction": "neutral", "statement": "multiple independent technical evidence items present"}


def trendline_confirmation(trendline_event: EvidenceEvent, candle_event: EvidenceEvent) -> dict:
    if not trendline_event.available or not candle_event.available or candle_event.timestamp <= trendline_event.timestamp:
        return {"available": False, "direction": "neutral", "statement": "trendline confirmation unavailable"}
    if trendline_event.kind not in {"trendline_touch", "trendline_break"}:
        return {"available": False, "direction": "neutral", "statement": "invalid trendline event"}
    return {"available": True, "direction": candle_event.direction, "statement": "trendline event followed by candlestick confirmation"}


def support_resistance_confirmation(level_event: EvidenceEvent, candle_event: EvidenceEvent) -> dict:
    if not level_event.available or not candle_event.available or candle_event.timestamp <= level_event.timestamp:
        return {"available": False, "direction": "neutral", "statement": "support/resistance confirmation unavailable"}
    if level_event.kind not in {"support_test", "resistance_test"}:
        return {"available": False, "direction": "neutral", "statement": "invalid level event"}
    return {"available": True, "direction": candle_event.direction, "statement": "level test followed by candlestick confirmation"}


def false_breakout_confirmation(break_event: EvidenceEvent, return_event: EvidenceEvent, candle_event: EvidenceEvent) -> dict:
    seq = [break_event, return_event, candle_event]
    if not all(e.available for e in seq) or not _ordered(seq):
        return {"available": False, "direction": "neutral", "statement": "false-breakout confirmation unavailable"}
    if break_event.kind not in {"upthrust", "spring"} or return_event.kind != "return_inside_range":
        return {"available": False, "direction": "neutral", "statement": "invalid false-breakout sequence"}
    return {"available": True, "direction": candle_event.direction, "statement": "false breakout returned inside range and received candlestick confirmation"}


def polarity_confirmation(break_event: EvidenceEvent, retest_event: EvidenceEvent, candle_event: EvidenceEvent) -> dict:
    seq = [break_event, retest_event, candle_event]
    if not all(e.available for e in seq) or not _ordered(seq):
        return {"available": False, "direction": "neutral", "statement": "polarity confirmation unavailable"}
    if break_event.kind != "level_break" or retest_event.kind != "successful_retest":
        return {"available": False, "direction": "neutral", "statement": "invalid polarity sequence"}
    return {"available": True, "direction": candle_event.direction, "statement": "broken level successfully retested and candlestick-confirmed"}
