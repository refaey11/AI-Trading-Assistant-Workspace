from compatibility.governed_78_rule_adapter_v1 import (
    build_governed_78_package,
    assert_governed_78_package,
)

MURPHY_IDS = [
    "MURPHY_0003", "MURPHY_0004", "MURPHY_0006", "MURPHY_0007",
    "MURPHY_0018", "MURPHY_0019", "MURPHY_0021", "MURPHY_0022", "MURPHY_0023",
    "MURPHY_0025", "MURPHY_0026", "MURPHY_0028", "MURPHY_0029", "MURPHY_0030",
    "MURPHY_0031", "MURPHY_0032", "MURPHY_0033", "MURPHY_0034", "MURPHY_0035",
    "MURPHY_0036", "MURPHY_0037", "MURPHY_0038", "MURPHY_0039", "MURPHY_0040",
    "MURPHY_0041", "MURPHY_0042", "MURPHY_0043", "MURPHY_0044", "MURPHY_0045",
    "MURPHY_0047", "MURPHY_0048", "MURPHY_0049", "MURPHY_0050", "MURPHY_0051",
]
NISON_IDS = [f"NISON_{i:04d}" for i in range(1, 45)]


def _rows(ids, **extra):
    return [{"source_rule_id": rid, "status": "NOT_EVALUABLE", **extra} for rid in ids]


def test_adapter_accepts_exact_frozen_78_and_returns_receipt():
    result = build_governed_78_package(
        query_as_of="2025-01-02T00:00:00Z",
        murphy_rows=_rows(MURPHY_IDS),
        nison_rows=_rows(NISON_IDS),
        mode="oos_evaluation",
        provenance={"test": "adapter"},
    )
    assert result.status == "PASS"
    assert result.package["receipt"]["all_78_rules_present"] is True
    assert result.package["receipt"]["murphy_rule_count"] == 34
    assert result.package["receipt"]["nison_rule_count"] == 44
    assert result.package["governance"]["adapter_generates_direction"] is False
    assert_governed_78_package(result.package)


def test_adapter_rejects_missing_rule():
    result = build_governed_78_package(
        query_as_of="2025-01-02T00:00:00Z",
        murphy_rows=_rows(MURPHY_IDS[:-1]),
        nison_rows=_rows(NISON_IDS),
        mode="oos_evaluation",
    )
    assert result.status == "NOT_EVALUABLE"
    assert "MURPHY_RULE_COUNT_33" in result.reason


def test_adapter_rejects_unknown_rule():
    result = build_governed_78_package(
        query_as_of="2025-01-02T00:00:00Z",
        murphy_rows=_rows(MURPHY_IDS[:-1] + ["MURPHY_FAKE"]),
        nison_rows=_rows(NISON_IDS),
        mode="oos_evaluation",
    )
    assert result.status == "NOT_EVALUABLE"
    assert "UNKNOWN_RULE_IDS" in result.reason


def test_adapter_preserves_not_evaluable_and_creates_no_direction():
    murphy = _rows(MURPHY_IDS)
    nison = _rows(NISON_IDS)
    murphy[0]["status"] = "PASS"
    murphy[0]["directional_confirmation"] = "BULLISH"
    result = build_governed_78_package(
        query_as_of="2025-01-02T00:00:00Z",
        murphy_rows=murphy,
        nison_rows=nison,
        mode="oos_evaluation",
    )
    assert result.status == "PASS"
    assert result.package["governance"]["not_evaluable_promoted_to_signal"] is False
    assert result.package["governance"]["adapter_generates_direction"] is False
