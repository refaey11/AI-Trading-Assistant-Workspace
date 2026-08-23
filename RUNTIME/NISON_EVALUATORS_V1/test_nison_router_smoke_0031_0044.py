from nison_0001_0010_router import evaluate_rule


def test_router_0031_0044():
    # Router smoke verifies dispatch/contract surface only.
    # Semantic PASS/FAIL behavior is covered by test_nison_0031_0044_runtime.py.
    for i in range(31, 39):
        rid = f"CANDLE_RULE_{i:04d}"
        payload = {"context": {"confirmation": {"confirmed": True}}}
        if rid == "CANDLE_RULE_0038":
            payload = {"context": {
                "previous_session": {"high": 10.0, "low": 9.0},
                "current_session": {"high": 12.0, "low": 10.5},
                "direction": "bullish",
            }}
        out = evaluate_rule(rid, payload)
        assert out["rule_id"] == rid, (rid, out)
        assert out["status"] in {"PASS", "FAIL", "NOT_EVALUABLE"}, (rid, out)
        assert out["provenance"]["standalone_direction"] is False

    for i in range(39, 45):
        rid = f"NISON_MODULE_{i:04d}"
        out = evaluate_rule(rid, {"context": {
            "evidence_available": True,
            "role": "context",
            "confirmation": {"confirmed": True},
        }})
        assert out["rule_id"] == rid, (rid, out)
        assert out["status"] == "PASS", (rid, out)
        assert out["provenance"]["standalone_direction"] is False


if __name__ == "__main__":
    test_router_0031_0044()
    print("Nison router smoke 0031-0044: PASS")
