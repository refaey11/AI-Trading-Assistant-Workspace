from nison_0001_0010_router import evaluate_rule
from test_nison_0011_0020_runtime import CASES


def test_router_0011_0020():
    for rid, payload in CASES.items():
        out = evaluate_rule(rid, payload)
        assert out["status"] == "PASS", (rid, out)


if __name__ == "__main__":
    test_router_0011_0020()
    print("Nison router smoke 0011-0020: PASS")
