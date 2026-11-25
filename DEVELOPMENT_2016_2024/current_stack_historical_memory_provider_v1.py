from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd


LOCKED_OOS_YEAR = 2025


@dataclass
class HistoricalMemoryProvider:
    context_path: Path
    outcome_path: Path
    similarity_artifact: Path
    retrieval_artifact: Path
    scenario_artifact: Path
    pair: str = "GBPUSD"

    def __post_init__(self) -> None:
        self.context = self._load(self.context_path, required={"pair", "timestamp"})
        self.outcome = self._load(self.outcome_path, required={"pair", "timestamp"})
        self.similarity_meta = self._read_json(self.similarity_artifact)
        self.retrieval_meta = self._read_json(self.retrieval_artifact)
        self.scenario_meta = self._read_json(self.scenario_artifact)

        self.context = self.context[self.context["pair"].astype(str).str.upper().eq(self.pair)]
        self.outcome = self.outcome[self.outcome["pair"].astype(str).str.upper().eq(self.pair)]
        self.context_ts = self.context["timestamp"].astype("int64").to_numpy()
        self.outcome_ts = self.outcome["timestamp"].astype("int64").to_numpy()

    @staticmethod
    def _load(path: Path, *, required: set[str]) -> pd.DataFrame:
        if not path.is_file() or path.stat().st_size == 0:
            raise ValueError(f"MEMORY_SOURCE_MISSING:{path}")
        df = pd.read_csv(path)
        missing = sorted(required - set(df.columns))
        if missing:
            raise ValueError(f"MEMORY_SOURCE_SCHEMA_MISSING:{path}:{missing}")
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="raise", format="mixed")
        return df.sort_values("timestamp", kind="stable").reset_index(drop=True)

    @staticmethod
    def _read_json(path: Path) -> Any:
        import json
        if not path.is_file() or path.stat().st_size == 0:
            raise ValueError(f"MEMORY_ARTIFACT_MISSING:{path}")
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def _asof_pos(ts_ns: Any, query_ns: int) -> int:
        import numpy as np
        pos = int(np.searchsorted(ts_ns, query_ns, side="left")) - 1
        return pos

    def evidence(self, query_as_of: Any, event: dict[str, Any]) -> dict[str, Any]:
        q = pd.Timestamp(query_as_of, tz="UTC") if not isinstance(query_as_of, pd.Timestamp) else query_as_of
        if q.tzinfo is None:
            q = q.tz_localize("UTC")
        if q.year >= LOCKED_OOS_YEAR:
            raise ValueError("2025_OOS_LOCKED")
        query_ns = int(q.value)

        # Historical Context: only strictly prior observations are eligible.
        cpos = self._asof_pos(self.context_ts, query_ns)
        context_payload: dict[str, Any]
        if cpos < 0:
            context_payload = {
                "status": "NOT_EVALUABLE",
                "reason": "NO_PRIOR_HISTORICAL_CONTEXT",
                "candidate_count": 0,
                "future_data_used": False,
                "lookahead_violation": False,
            }
        else:
            crow = self.context.iloc[cpos]
            context_payload = {
                "status": "PASS",
                "candidate_count": int(cpos + 1),
                "query_as_of": q.isoformat(),
                "evidence_time_range": {"earliest": self.context.iloc[0].timestamp.isoformat(), "latest": crow.timestamp.isoformat()},
                "record": {k: (v.item() if hasattr(v, "item") else v) for k, v in crow.to_dict().items()},
                "future_data_used": False,
                "lookahead_violation": False,
                "predicted_return_used_as_direction": False,
            }

        # Historical Outcome: outcome horizons extend after the source timestamp.
        # Require the full 48h horizon to have elapsed before the query time.
        cutoff = q - pd.Timedelta(hours=48)
        outcome_cutoff_ns = int(cutoff.value)
        opos = self._asof_pos(self.outcome_ts, outcome_cutoff_ns)
        outcome_payload: dict[str, Any]
        if opos < 0:
            outcome_payload = {
                "status": "NOT_EVALUABLE",
                "reason": "NO_PRIOR_COMPLETED_OUTCOME_CONTEXT",
                "candidate_count": 0,
                "future_data_used": False,
                "lookahead_violation": False,
            }
        else:
            orow = self.outcome.iloc[opos]
            outcome_payload = {
                "status": "PASS",
                "candidate_count": int(opos + 1),
                "query_as_of": q.isoformat(),
                "evidence_time_range": {"earliest": self.outcome.iloc[0].timestamp.isoformat(), "latest": orow.timestamp.isoformat()},
                "record": {k: (v.item() if hasattr(v, "item") else v) for k, v in orow.to_dict().items()},
                "future_data_used": False,
                "lookahead_violation": False,
                "predicted_return_used_as_direction": False,
            }

        # The stored Similarity/Retrieval/Scenario snapshots are 2025 snapshots.
        # They are deliberately wired as explicit NOT_EVALUABLE inputs in the
        # 2016-2024 replay rather than reused, preventing OOS leakage.
        similarity_payload = {
            "status": "NOT_EVALUABLE",
            "reason": "STORED_SIMILARITY_SNAPSHOT_IS_OOS_2025",
            "candidate_count": 0,
            "artifact_present": True,
            "future_data_used": False,
            "lookahead_violation": False,
            "predicted_return_used_as_direction": False,
        }
        retrieval_payload = {
            "status": "NOT_EVALUABLE",
            "reason": "STORED_RETRIEVAL_SNAPSHOT_IS_OOS_2025",
            "candidate_count": 0,
            "artifact_present": True,
            "future_data_used": False,
            "lookahead_violation": False,
            "predicted_return_used_as_direction": False,
        }
        scenario_payload = {
            "status": "NOT_EVALUABLE",
            "reason": "STORED_SCENARIO_SNAPSHOT_IS_OOS_2025",
            "artifact_present": True,
            "direction_generated": False,
            "future_data_used": False,
            "lookahead_violation": False,
        }

        return {
            "status": "PASS",
            "query_as_of": q.isoformat(),
            "memory_role": "EVIDENCE_ONLY",
            "sources": {
                "historical_context": context_payload,
                "historical_outcome": outcome_payload,
                "similarity": similarity_payload,
                "context_aware_retrieval": retrieval_payload,
                "scenario_engine": scenario_payload,
            },
            "governance": {
                "memory_generated_direction": False,
                "similarity_is_sole_decision_maker": False,
                "predicted_return_used_as_direction": False,
                "final_trade_decision_generated": False,
                "2025_used_for_tuning": False,
                "future_data_allowed": False,
            },
        }
