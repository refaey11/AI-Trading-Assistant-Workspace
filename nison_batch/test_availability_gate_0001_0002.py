from dataclasses import dataclass


@dataclass(frozen=True)
class Evidence:
    event_timestamp: str
    availability_timestamp: str


def is_available(evidence: Evidence, evaluation_availability_timestamp: str) -> bool:
    return evidence.availability_timestamp <= evaluation_availability_timestamp


def test_same_timestamp_is_available():
    e = Evidence("2024-01-02T10:00:00", "2024-01-02T10:00:00")
    assert is_available(e, "2024-01-02T10:00:00") is True


def test_future_availability_is_rejected():
    e = Evidence("2024-01-02T10:00:00", "2024-01-02T10:05:00")
    assert is_available(e, "2024-01-02T10:00:00") is False


def test_later_evidence_cannot_leak_backward():
    e = Evidence("2024-01-02T10:00:00", "2024-01-02T10:01:00")
    assert is_available(e, "2024-01-02T10:00:30") is False
