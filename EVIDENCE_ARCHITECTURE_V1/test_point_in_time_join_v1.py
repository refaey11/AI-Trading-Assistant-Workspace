from EVIDENCE_ARCHITECTURE_V1.point_in_time_join_v1 import join_point_in_time


def rec(eid, feature, event, available, value, quality="AUTHORITATIVE"):
    return {
        "evidence_id": eid,
        "event_time": event,
        "available_time": available,
        "source": "TEST",
        "instrument": "GBPUSD",
        "feature": feature,
        "value": value,
        "quality": quality,
        "status": "AVAILABLE",
    }


def test_future_evidence_is_rejected():
    records = [rec("e1", "price", "2025-01-01T09:00:00Z", "2025-01-01T09:00:00Z", 1.25),
               rec("e2", "oi_direction", "2025-01-01T10:00:00Z", "2025-01-01T11:00:00Z", "UP")]
    out = join_point_in_time(records, "2025-01-01T10:00:00Z", required_features=["price", "oi_direction"])
    assert out["status"] == "NOT_EVALUABLE"
    assert out["missing_features"] == ["oi_direction"]


def test_latest_available_record_wins():
    records = [rec("e1", "price", "2025-01-01T09:00:00Z", "2025-01-01T09:00:00Z", 1.25),
               rec("e2", "price", "2025-01-01T09:30:00Z", "2025-01-01T09:31:00Z", 1.26)]
    out = join_point_in_time(records, "2025-01-01T10:00:00Z", required_features=["price"])
    assert out["status"] == "AVAILABLE"
    assert out["selected"]["price"]["value"] == 1.26


def test_missing_evidence_fails_closed():
    records = [rec("e1", "price", "2025-01-01T09:00:00Z", "2025-01-01T09:00:00Z", 1.25)]
    out = join_point_in_time(records, "2025-01-01T10:00:00Z", required_features=["price", "volume"])
    assert out["status"] == "NOT_EVALUABLE"
    assert out["selected"] == {}
