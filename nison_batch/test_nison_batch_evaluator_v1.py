from nison_batch_evaluator_v1 import *

def bar(o,c,h=None,l=None):
    return {"open":o,"close":c,"high": h if h is not None else max(o,c), "low": l if l is not None else min(o,c)}

def test_separating_lines():
    r=separating_lines(bar(10,8),bar(10,12),equal_open=lambda a,b:a["open"]==b["open"])
    assert (r.state,r.side)==("PASS","bullish")

def test_windows():
    r=windows(bar(10,11,h=11),bar(12,13),gap_up=lambda a,b:b["open"]>a["high"],gap_down=lambda a,b:b["open"]<a["low"])
    assert r.state=="PASS" and r.side=="bullish"

def test_qualitative_gate():
    assert three_mountains(structure_ok=None).state=="NOT_EVALUABLE"

def test_buddha_bottoms():
    r=three_buddha_bottoms(structure_ok=True)
    assert (r.state,r.side)==("PASS","bullish")
