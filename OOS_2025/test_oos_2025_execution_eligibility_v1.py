import pandas as pd

from OOS_2025.oos_2025_execution_eligibility_v1 import apply_execution_eligibility


def test_missing_authoritative_evidence_is_not_eligible():
    events = pd.DataFrame([
        {
            "nison_status": "NOT_EVALUABLE",
            "tiz_process_state": "NOT_EVALUABLE",
            "risk_pass": False,
        }
    ])
    out = apply_execution_eligibility(events)
    assert out.loc[0, "execution_eligible"] is False
    assert out.loc[0, "execution_eligibility_reason"] == "NISON_NOT_AUTHORITATIVE"


def test_fully_evidenced_row_is_eligible():
    events = pd.DataFrame([
        {
            "nison_status": "PASS",
            "tiz_process_state": "READY",
            "risk_pass": True,
        }
    ])
    out = apply_execution_eligibility(events)
    assert bool(out.loc[0, "execution_eligible"]) is True
    assert out.loc[0, "execution_eligibility_reason"] == "ELIGIBLE"
