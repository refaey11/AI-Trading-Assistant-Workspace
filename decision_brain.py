from dataclasses import dataclass, asdict
from typing import Dict, List, Any
import math

@dataclass
class Evidence:
    module: str
    statement: str
    direction: str
    strength: float

@dataclass
class MarketAssessment:
    market_state: str
    directional_bias: str
    confidence: float
    evidence: List[Dict[str, Any]]
    contradictions: List[Dict[str, Any]]
    no_trade_reasons: List[str]

def _clip(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, float(x)))

def _mean(vals):
    vals=[float(v) for v in vals if v is not None and not math.isnan(float(v))]
    return sum(vals)/len(vals) if vals else 0.0

def assess(row: Dict[str, Any], similarity: Dict[str, Any] | None = None) -> MarketAssessment:
    """V1 is an evidence aggregator, not a trading signal generator."""
    evidence=[]
    mtf=float(row.get("mtf_trend_score", 0) or 0)
    if mtf > 0:
        evidence.append(Evidence("MTF", "Multi-timeframe context is bullish.", "bullish", _clip(abs(mtf))))
    elif mtf < 0:
        evidence.append(Evidence("MTF", "Multi-timeframe context is bearish.", "bearish", _clip(abs(mtf))))
    else:
        evidence.append(Evidence("MTF", "Multi-timeframe context is neutral/mixed.", "neutral", 0.2))
    regs=[row.get(k) for k in ["M5_trend_regime","M15_trend_regime","M30_trend_regime","H1_trend_regime","H4_trend_regime","D1_trend_regime"]]
    tr=_mean(regs)
    if tr > 0.20:
        evidence.append(Evidence("Structure", "Trend regimes lean bullish across timeframes.", "bullish", _clip(abs(tr))))
    elif tr < -0.20:
        evidence.append(Evidence("Structure", "Trend regimes lean bearish across timeframes.", "bearish", _clip(abs(tr))))
    else:
        evidence.append(Evidence("Structure", "Trend regimes are mixed/transitioning.", "neutral", 0.35))
    if bool(row.get("volume_available", False)):
        v=[]
        for k in ["M5_volume_regime","M15_volume_regime","M30_volume_regime","H1_volume_regime","H4_volume_regime","D1_volume_regime"]:
            if k in row and row[k] is not None:
                try: v.append(float(row[k]))
                except: pass
        vv=_mean(v)
        evidence.append(Evidence("Volume", "Volume regime supports participation/confirmation." if vv>0 else "Volume regime is weak/contradictory.", "bullish" if vv>0 else "neutral", _clip(abs(vv))))
    else:
        evidence.append(Evidence("Volume", "Volume data is unavailable for this historical regime.", "neutral", 0.0))
    if similarity:
        s=float(similarity.get("predicted_return", 0) or 0)
        if s > 0:
            evidence.append(Evidence("HistoricalMemory", "Historical analogs lean upward.", "bullish", _clip(abs(s)*100)))
        elif s < 0:
            evidence.append(Evidence("HistoricalMemory", "Historical analogs lean downward.", "bearish", _clip(abs(s)*100)))
        else:
            evidence.append(Evidence("HistoricalMemory", "Historical analogs are inconclusive.", "neutral", 0.2))
    bull=sum(e.strength for e in evidence if e.direction=="bullish")
    bear=sum(e.strength for e in evidence if e.direction=="bearish")
    total=bull+bear
    bias="neutral"
    if total:
        gap=abs(bull-bear)/total
        if gap < 0.15: bias="conflicted"
        else: bias="bullish" if bull>bear else "bearish"
    if bias=="conflicted": state="uncertain"
    elif abs(tr)<0.20: state="range/transition"
    else: state="trend"
    confidence=_clip(abs(bull-bear)/(bull+bear+1e-9))
    contradictions=[asdict(e) for e in evidence if (e.direction=="bullish" and bear>bull) or (e.direction=="bearish" and bull>bear)]
    no_trade=[]
    if bias in ("neutral","conflicted"): no_trade.append("Evidence is not directionally aligned.")
    if confidence < 0.25: no_trade.append("Confidence is below the V1 decision threshold.")
    if not bool(row.get("volume_available", False)): no_trade.append("Volume confirmation is unavailable for this historical regime.")
    return MarketAssessment(state,bias,confidence,[asdict(e) for e in evidence],contradictions,no_trade)
