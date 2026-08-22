from murphy_0029_runtime_adapter import evaluate_0029


def test_bullish_low_pass():
    r = evaluate_0029({"divergence_type": "BULLISH", "pivot_type": "LOW"})
    assert r["status"] == "PASS"
    assert r["directional_confirmation"] == "BULLISH"


def test_wrong_direction_fail():
    r = evaluate_0029({"divergence_type": "BEARISH", "pivot_type": "HIGH"})
    assert r["status"] == "FAIL"
    assert r["directional_confirmation"] == "NONE"


def test_missing_evidence_not_evaluable():
    r = evaluate_0029({"divergence_type": None, "pivot_type": "LOW"})
    assert r["status"] == "NOT_EVALUABLE"


def test_historical_population_matches_existing_status():
    import csv
    path = "MURPHY_0029_EVALUATION_2016_2024_V1(2).csv"
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        got = evaluate_0029(row)
        assert got["status"] == row["rule_0029_status"]

    assert sum(evaluate_0029(r)["status"] == "PASS" for r in rows) == 2930
    assert sum(evaluate_0029(r)["status"] == "FAIL" for r in rows) == 2889
