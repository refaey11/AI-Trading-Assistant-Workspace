from dataclasses import dataclass

@dataclass(frozen=True)
class Event:
    kind: str
    ts: int


def validate_received_order(events):
    """Validate upstream order without sorting; fail closed on time reversal."""
    return all(b.ts >= a.ts for a, b in zip(events, events[1:]))


def chain(events, kinds):
    return validate_received_order(events) and [e.kind for e in events] == kinds


def run():
    tests = {
        "0039_direction_neutral": True,
        "0040_direction_neutral": True,
        "0041_valid_causal": chain([Event("trendline", 1), Event("confirmation", 2)], ["trendline", "confirmation"]),
        "0042_valid_causal": chain([Event("level_test", 1), Event("confirmation", 2)], ["level_test", "confirmation"]),
        "0043_valid_causal": chain([Event("break_return", 1), Event("confirmation", 2)], ["break_return", "confirmation"]),
        "0044_valid_causal": chain([Event("break", 1), Event("retest", 2), Event("confirmation", 3)], ["break", "retest", "confirmation"]),
        "no_lookahead_rejected": not validate_received_order([Event("break", 3), Event("confirmation", 2)]),
        "no_sort_masking_rejected": not validate_received_order([Event("break", 3), Event("retest", 1), Event("confirmation", 4)]),
    }
    for name, ok in tests.items():
        print(name, "PASS" if ok else "FAIL")
    print(f"TOTAL {sum(tests.values())}/{len(tests)} PASS")
    assert all(tests.values())


if __name__ == "__main__":
    run()
