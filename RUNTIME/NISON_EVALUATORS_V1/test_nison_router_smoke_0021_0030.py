from nison_0001_0010_router import evaluate_rule


def test_router_0021_0030():
    for i in range(21, 31):
        rid = f"CANDLE_RULE_{i:04d}"
        if i == 30:
            payload = {"context": {"trend": "Uptrend", "formation_complete": True,
                                   "final_bullish_strong": True,
                                   "confirmation": {"confirmed": True}}}
        else:
            payload = {"context": {"formation_confirmed": True,
                                   "confirmation": {"confirmed": True}}}
        out = evaluate_rule(rid, payload)
        assert out["status"] == "PASS", (rid, out)


if __name__ == "__main__":
    test_router_0021_0030()
    print("Nison router smoke 0021-0030: PASS")
