from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd

MURPHY_RULES = {
    "MURPHY_0003","MURPHY_0004","MURPHY_0006","MURPHY_0007","MURPHY_0018","MURPHY_0019",
    "MURPHY_0021","MURPHY_0022","MURPHY_0023","MURPHY_0025","MURPHY_0026","MURPHY_0028",
    "MURPHY_0029","MURPHY_0030","MURPHY_0031","MURPHY_0032","MURPHY_0033","MURPHY_0034",
    "MURPHY_0035","MURPHY_0036","MURPHY_0037","MURPHY_0038","MURPHY_0039","MURPHY_0040",
    "MURPHY_0041","MURPHY_0042","MURPHY_0043","MURPHY_0044","MURPHY_0045","MURPHY_0047",
    "MURPHY_0048","MURPHY_0049","MURPHY_0050","MURPHY_0051",
}
NISON_RULES = {f"NISON_{i:04d}" for i in range(1, 45)}
ALL_RULES = MURPHY_RULES | NISON_RULES

@dataclass(frozen=True)
class EventResult:
    timestamp: pd.Timestamp
    status: str
    direction: str
    eligible: bool
    missing_rules: tuple[str, ...]
    contradiction: bool
    risk_pass: bool


def _norm(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "timestamp" not in out.columns:
        raise ValueError("timestamp column required")
    out["timestamp"] = pd.to_datetime(out["timestamp"], utc=True)
    return out


def aggregate_rule_evidence(rule_output: pd.DataFrame) -> pd.DataFrame:
    """Aggregate existing per-rule runtime output without inventing rule semantics."""
    rule_output = _norm(rule_output)
    required = {"timestamp", "rule_id", "status"}
    missing = required - set(rule_output.columns)
    if missing:
        raise ValueError(f"rule output missing columns: {sorted(missing)}")
    rule_output = rule_output[rule_output["rule_id"].isin(ALL_RULES)].copy()
    rows = []
    for ts, g in rule_output.groupby("timestamp", sort=True):
        seen = set(g["rule_id"].astype(str))
        missing_rules = tuple(sorted(ALL_RULES - seen))
        murphy_pass = int(((g.rule_id.isin(MURPHY_RULES)) & (g.status == "PASS")).sum())
        nison_contradiction = bool(((g.rule_id.isin(NISON_RULES)) & g.status.astype(str).isin({"CONTRADICTORY", "CONTRADICTION", "FAIL_CONTRADICTION"})).any())
        directions = set()
        if "directional_confirmation" in g.columns:
            for value in g["directional_confirmation"].dropna().astype(str):
                for part in value.split("|"):
                    if part in {"BULLISH", "BEARISH"}:
                        directions.add(part)
        direction = "BUY" if directions == {"BULLISH"} else "SELL" if directions == {"BEARISH"} else "NO_TRADE"
        rows.append({
            "timestamp": ts,
            "rule_count_seen": len(seen),
            "missing_rule_count": len(missing_rules),
            "missing_rules": "|".join(missing_rules),
            "murphy_pass_count": murphy_pass,
            "nison_contradiction": nison_contradiction,
            "direction": direction,
        })
    return pd.DataFrame(rows)


def build_frozen_events(
    market: pd.DataFrame,
    rule_output: pd.DataFrame,
    risk_output: pd.DataFrame,
    tiz_output: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Join existing producer outputs into one deterministic 2025 event stream.

    This function is deliberately an orchestration boundary: it never creates a
    PASS for a missing rule/evidence source and never infers TIZ/Risk semantics.
    """
    market = _norm(market)
    agg = aggregate_rule_evidence(rule_output)
    risk = _norm(risk_output)
    for col in ("risk_pass",):
        if col not in risk.columns:
            raise ValueError(f"risk output missing {col}")
    risk = risk[[c for c in ["timestamp", "risk_pass", "stop_loss", "take_profit", "position_size"] if c in risk.columns]]
    events = market.merge(agg, on="timestamp", how="left").merge(risk, on="timestamp", how="left")
    if tiz_output is not None:
        tiz = _norm(tiz_output)
        keep = [c for c in ["timestamp", "tiz_process_state"] if c in tiz.columns]
        events = events.merge(tiz[keep], on="timestamp", how="left")
    events["risk_pass"] = events["risk_pass"].fillna(False).astype(bool)
    events["nison_contradiction"] = events["nison_contradiction"].fillna(False).astype(bool)
    events["direction"] = events["direction"].fillna("NO_TRADE")
    events["eligible"] = (
        events["missing_rule_count"].fillna(len(ALL_RULES)).eq(0)
        & events["murphy_pass_count"].fillna(0).gt(0)
        & events["direction"].isin(["BUY", "SELL"])
        & ~events["nison_contradiction"]
        & events["risk_pass"]
    )
    events["status"] = events["eligible"].map({True: "ELIGIBLE", False: "NOT_ELIGIBLE"})
    return events.sort_values("timestamp").reset_index(drop=True)
