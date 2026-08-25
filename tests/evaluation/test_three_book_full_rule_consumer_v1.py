import json
from pathlib import Path

from evaluation.three_book_decision_evaluator_v1 import evaluate_three_book_decision


ROOT = Path(__file__).resolve().parents[2]
ALLOWLIST = ROOT / "governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json"


def _ids():
    data = json.loads(ALLOWLIST.read_text(encoding="utf-8"))
    return data["verified_runtime"]["MURPHY"], data["verified_runtime"]["NISON"]


def _evidence_sets(*, murphy_bearish=False, nison_contradiction=False):
    murphy_ids, nison_ids = _ids()
    murphy = {}
    for i, rule_id in enumerate(murphy_ids):
        murphy[rule_id] = {
            "source_rule_id": rule_id,
            "status": "PASS" if i == 0 else "NOT_EVALUABLE",
            "directional_confirmation": (
                "BEARISH" if murphy_bearish and i == 0 else "BULLISH" if i == 0 else "UNKNOWN"
            ),
        }
    nison = {}
    for i, rule_id in enumerate(nison_ids):
        nison[rule_id] = {
            "source_rule_id": rule_id,
            "confirmation": "CONTRADICTED" if nison_contradiction and i == 0 else "CONFIRMED" if i == 0 else "NOT_EVALUABLE",
            "contradiction": bool(nison_contradiction and i == 0),
        }
    return murphy, nison


def _base(murphy, nison):
    return {
        "brain_assessment": {"directional_bias": "BULLISH", "confidence": 0.7},
        "murphy_evidence": {"status": "PASS", "direction": "BULLISH", "evidence_set": murphy},
        "nison_evidence": {"confirmation": "NOT_EVALUABLE", "contradiction": False, "evidence_set": nison},
        "tiz_evidence": {"process_gate": "READY"},
        "risk_evidence": {"risk_pass": True, "stop_loss": "1.2450"},
        "source_rule_ids": [*murphy.keys(), *nison.keys()],
        "timestamp": "2024-12-31T00:00:00+00:00",
    }


def test_full_78_rule_envelope_is_consumed_and_can_confirm_direction():
    murphy, nison = _evidence_sets()
    result = evaluate_three_book_decision(**_base(murphy, nison))
    assert result["status"] == "EXECUTABLE"
    assert result["decision"]["final"] == "BUY"
    assert result["audit"]["full_rule_consumer"]["murphy_rule_count"] == 34
    assert result["audit"]["full_rule_consumer"]["nison_rule_count"] == 44


def test_full_murphy_conflict_blocks_execution():
    murphy, nison = _evidence_sets()
    murphy["MURPHY_0004"] = {
        "source_rule_id": "MURPHY_0004",
        "status": "PASS",
        "directional_confirmation": "BEARISH",
    }
    result = evaluate_three_book_decision(**_base(murphy, nison))
    assert result["status"] == "NO_TRADE"
    assert "MURPHY_FULL_RULE_CONFLICT" in result["decision"]["reasons_against"]


def test_full_nison_contradiction_blocks_execution():
    murphy, nison = _evidence_sets(nison_contradiction=True)
    result = evaluate_three_book_decision(**_base(murphy, nison))
    assert result["status"] == "NO_TRADE"
    assert "NISON_FULL_RULE_CONTRADICTION" in result["decision"]["reasons_against"]


def test_incomplete_full_rule_envelope_fails_closed():
    murphy, nison = _evidence_sets()
    nison.pop(next(iter(nison)))
    result = evaluate_three_book_decision(**_base(murphy, nison))
    assert result["status"] == "NO_TRADE"
    assert "FULL_RULE_EVIDENCE_INCOMPLETE" in result["decision"]["reasons_against"]
