from __future__ import annotations

import pandas as pd


def apply_execution_eligibility(events: pd.DataFrame) -> pd.DataFrame:
    """Mark only fully evidenced rows as execution-eligible.

    Missing/non-authoritative Nison/TIZ/Risk evidence is fail-closed. This
    helper does not create direction, thresholds, or psychology semantics.
    """
    out = events.copy()
    tiz_ok = out["tiz_process_state"].isin({"READY", "PASS", "AVAILABLE"})
    risk_ok = out["risk_pass"].eq(True)
    nison_ok = out["nison_status"].isin({"PASS", "CONFIRMED", "AVAILABLE"})

    out["execution_eligible"] = tiz_ok & risk_ok & nison_ok
    out["execution_eligibility_reason"] = "ELIGIBLE"
    out.loc[~nison_ok, "execution_eligibility_reason"] = "NISON_NOT_AUTHORITATIVE"
    out.loc[nison_ok & ~tiz_ok, "execution_eligibility_reason"] = "TIZ_NOT_AUTHORITATIVE"
    out.loc[nison_ok & tiz_ok & ~risk_ok, "execution_eligibility_reason"] = "RISK_NOT_PASSED"
    return out
