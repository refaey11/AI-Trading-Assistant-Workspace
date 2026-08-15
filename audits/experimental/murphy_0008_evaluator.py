from __future__ import annotations
import pandas as pd

RULE_ID = "MURPHY_0008"


def evaluate_event(pivot: dict, d1: pd.DataFrame) -> dict:
    required_pivot = {"pivot_timestamp", "pivot_type", "pivot_price", "availability_timestamp"}
    required_d1 = {"timestamp", "open", "high", "low", "close"}
    if not required_pivot.issubset(pivot) or not required_d1.issubset(d1.columns):
        return {"rule_id": RULE_ID, "status": "NOT_EVALUABLE"}
    if pivot["pivot_type"] != "LOW":
        return {"rule_id": RULE_ID, "status": "NOT_EVALUABLE"}

    support = pivot["pivot_price"]
    availability = pd.Timestamp(pivot["availability_timestamp"])
    bars = d1.sort_values("timestamp").reset_index(drop=True)
    eligible = bars[bars["timestamp"] > availability].reset_index(drop=True)
    if eligible.empty:
        return {"rule_id": RULE_ID, "status": "NOT_EVALUABLE"}

    below = eligible["close"] < support
    candidate_indexes = below[below].index.tolist()
    if not candidate_indexes:
        return {"rule_id": RULE_ID, "status": "NOT_CONFIRMED", "support_price": support}

    i = candidate_indexes[0]
    if i + 1 >= len(eligible) or not (eligible.loc[i + 1, "close"] < support):
        return {
            "rule_id": RULE_ID,
            "status": "NOT_CONFIRMED",
            "support_price": support,
            "candidate_break_timestamp": eligible.loc[i, "timestamp"],
        }

    first = eligible.loc[i]
    second = eligible.loc[i + 1]
    later = eligible.iloc[i + 2 :].copy()
    intersects = later[(later["low"] <= support) & (later["high"] >= support)]
    role = intersects[intersects["close"] < support]

    return {
        "rule_id": RULE_ID,
        "status": "CONFIRMED",
        "support_pivot_timestamp": pd.Timestamp(pivot["pivot_timestamp"]),
        "support_availability_timestamp": availability,
        "support_price": support,
        "candidate_break_timestamp": first["timestamp"],
        "confirmation_timestamp": second["timestamp"],
        "retest_timestamp": intersects.iloc[0]["timestamp"] if len(intersects) else pd.NaT,
        "role_reversal_timestamp": role.iloc[0]["timestamp"] if len(role) else pd.NaT,
    }
