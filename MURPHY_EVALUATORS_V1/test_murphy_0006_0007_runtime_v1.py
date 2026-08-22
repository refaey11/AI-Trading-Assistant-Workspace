from murphy_0006_0007_runtime_v1 import evaluate_0006, evaluate_0007

def lp(_): return 100.0

def base(family):
    return [
        {"timestamp": 1, "available_at": 2, "family": family, "line_available_at": 1,
         "bar_low": (100.0 if family == "LOW" else 99.9),
         "bar_high": (100.1 if family == "LOW" else 100.0)},
        {"timestamp": 2, "available_at": 3, "family": "HIGH" if family == "LOW" else "LOW",
         "line_available_at": 1,
         "bar_low": (100.2 if family == "LOW" else 99.8),
         "bar_high": (100.4 if family == "LOW" else 99.9)},
    ]

def test_0006_confirmed():
    r=evaluate_0006(base("LOW"), lp); assert r["status"]=="CONFIRMED" and r["direction"]=="BULLISH"

def test_0007_confirmed():
    r=evaluate_0007(base("HIGH"), lp); assert r["status"]=="CONFIRMED" and r["direction"]=="BEARISH"

def test_lookahead_rejected():
    ev=base("LOW"); ev[0]["available_at"]=0
    r=evaluate_0006(ev, lp); assert r["status"]=="NOT_EVALUABLE"

def test_missing_evidence():
    r=evaluate_0006([], lp); assert r["status"]=="NOT_EVALUABLE"

def test_wrong_first_candidate_rejected():
    ev=base("LOW"); ev[0]["bar_low"]=100.2
    r=evaluate_0006(ev, lp); assert r["status"]=="NOT_EVALUABLE"
