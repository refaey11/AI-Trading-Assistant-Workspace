import unittest
from dataclasses import dataclass


@dataclass(frozen=True)
class Evidence:
    event_timestamp: str
    availability_timestamp: str


def is_available(evidence: Evidence, evaluation_availability_timestamp: str) -> bool:
    return evidence.availability_timestamp <= evaluation_availability_timestamp


class AvailabilityGateTests(unittest.TestCase):
    def test_same_timestamp_is_available(self):
        e = Evidence("2024-01-02T10:00:00", "2024-01-02T10:00:00")
        self.assertTrue(is_available(e, "2024-01-02T10:00:00"))

    def test_future_availability_is_rejected(self):
        e = Evidence("2024-01-02T10:00:00", "2024-01-02T10:05:00")
        self.assertFalse(is_available(e, "2024-01-02T10:00:00"))

    def test_later_evidence_cannot_leak_backward(self):
        e = Evidence("2024-01-02T10:00:00", "2024-01-02T10:01:00")
        self.assertFalse(is_available(e, "2024-01-02T10:00:30"))


if __name__ == "__main__":
    unittest.main()
