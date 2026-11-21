import unittest

from event_lifecycle_v1_synthetic_oracle import (
    SyntheticPivot,
    evaluate_event_lifecycle,
)


def high(pid="H1", price=10.0, source=0, available=0):
    return SyntheticPivot(pid, "HIGH", price, source, available)


def low(pid="L1", price=10.0, source=0, available=0):
    return SyntheticPivot(pid, "LOW", price, source, available)


class ApprovedEventLifecyclePolicyTests(unittest.TestCase):
    def test_upward_cross_emits_once(self):
        events = evaluate_event_lifecycle([9, 11], [high()])
        self.assertEqual([(e.pivot_id, e.direction, e.bar_index) for e in events],
                         [("H1", "UP", 1)])

    def test_closes_remaining_beyond_level_do_not_repeat(self):
        events = evaluate_event_lifecycle([9, 11, 12, 13, 14], [high()])
        self.assertEqual(len(events), 1)

    def test_recross_rearms_then_allows_new_event(self):
        events = evaluate_event_lifecycle([9, 11, 12, 9, 11], [high()])
        self.assertEqual([e.bar_index for e in events], [1, 4])
        self.assertNotEqual(events[0].event_id, events[1].event_id)

    def test_equality_is_pre_break_side_and_rearms(self):
        events = evaluate_event_lifecycle([9, 11, 10, 10, 11], [high()])
        self.assertEqual([e.bar_index for e in events], [1, 4])

    def test_downward_cross_rearms_symmetrically(self):
        events = evaluate_event_lifecycle([11, 9, 8, 11, 9], [low()])
        self.assertEqual([e.direction for e in events], ["DOWN", "DOWN"])
        self.assertEqual([e.bar_index for e in events], [1, 4])

    def test_no_age_expiry_after_long_synthetic_wait(self):
        closes = [9.0] + [9.5] * 500 + [11.0]
        events = evaluate_event_lifecycle(closes, [high()])
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].bar_index, 501)

    def test_new_same_kind_pivot_supersedes_old_boundary(self):
        pivots = [high("OLD", 10, 0, 0), high("NEW", 15, 1, 2)]
        events = evaluate_event_lifecycle([9, 11, 14, 16], pivots)
        self.assertEqual([(e.pivot_id, e.bar_index) for e in events],
                         [("OLD", 1), ("NEW", 3)])

    def test_superseded_boundary_cannot_emit_later(self):
        pivots = [high("OLD", 10, 0, 0), high("NEW", 15, 1, 2)]
        events = evaluate_event_lifecycle([9, 11, 14, 9, 11], pivots)
        self.assertEqual([e.pivot_id for e in events], ["OLD"])

    def test_high_and_low_lifecycles_are_independent(self):
        pivots = [high("H", 10, 0, 0), low("L", 5, 0, 0)]
        events = evaluate_event_lifecycle([7, 11, 4, 7, 11, 4], pivots)
        self.assertEqual([(e.pivot_id, e.direction) for e in events],
                         [("H", "UP"), ("L", "DOWN"), ("H", "UP"), ("L", "DOWN")])

    def test_same_bar_as_pivot_availability_cannot_use_boundary(self):
        events = evaluate_event_lifecycle([9, 11], [high(available=1)])
        self.assertEqual(events, [])

    def test_rearm_does_not_invalidate_boundary(self):
        events = evaluate_event_lifecycle([9, 11, 9, 11], [high()])
        self.assertEqual([e.pivot_id for e in events], ["H1", "H1"])

    def test_close_only_input_has_no_wick_only_event_path(self):
        events = evaluate_event_lifecycle([9, 9.5], [high(price=10)])
        self.assertEqual(events, [])

    def test_replay_is_deterministic(self):
        closes = [9, 11, 12, 9, 11, 8, 11]
        pivots = [high(), low("L1", 5)]
        self.assertEqual(evaluate_event_lifecycle(closes, pivots),
                         evaluate_event_lifecycle(closes, pivots))

    def test_rejects_duplicate_synthetic_pivot_ids(self):
        with self.assertRaises(ValueError):
            evaluate_event_lifecycle([9, 11], [high(), high()])

    def test_rejects_boolean_prices_and_closes(self):
        with self.assertRaises(ValueError):
            evaluate_event_lifecycle([9, 11], [high(price=True)])
        with self.assertRaises(ValueError):
            evaluate_event_lifecycle([9, True], [high()])


if __name__ == "__main__":
    unittest.main()
