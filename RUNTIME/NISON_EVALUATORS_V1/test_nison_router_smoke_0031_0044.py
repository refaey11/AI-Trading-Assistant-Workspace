from nison_0001_0010_router import evaluate_rule


def test_router_0031_0044():
    for i in range(31, 38):
        rid = f"CANDLE_RULE_{i:04d}"
        out = evaluate_rule(rid, {"context": {"formation_confirmed": True, "confirmation": {"confirmed": True}}})
        assert out["status"] == "PASS", (rid, out)

    out = evaluate_rule("CANDLE_RULE_0038", {"context": {
        "previous_session": {"high": 10.0, "low": 9.0},
        "current_session": {"high": 12.0, "low": 10.5},
        "direction": "bullish",
    }})
    assert out["status"] == "PASS", ("CANDLE_RULE_0038", out)

    for i in range(39, 45):
        rid = f"NISON_MODULE_{i:04d}"
        out = evaluate_rule(rid, {"context": {"evidence_available": True, "role": "context"}})
        assert out["status"] == "PASS", (rid, out)
        assert out["provenance"]["standalone_direction"] is False


if __name__ == "__main__":
    test_router_0031_0044()
    print("Nison router smoke 0031-0044: PASS")
