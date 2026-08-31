from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
from typing import Any

from current_stack_historical_memory_provider_v1 import HistoricalMemoryProvider

ROOT = Path(__file__).resolve().parents[1]


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if not spec or not spec.loader:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(h1: Path, market_state: Path, murphy: Path, nison: Path, mtf: Path,
        historical_context: Path, historical_outcome: Path,
        similarity_artifact: Path, retrieval_artifact: Path, scenario_artifact: Path,
        output_dir: Path) -> None:
    replay = _load_module(
        ROOT / "DEVELOPMENT_2016_2024" / "current_stack_historical_replay_v2.py",
        "current_stack_historical_replay_v2_engine",
    )
    provider = HistoricalMemoryProvider(
        context_path=historical_context,
        outcome_path=historical_outcome,
        similarity_artifact=similarity_artifact,
        retrieval_artifact=retrieval_artifact,
        scenario_artifact=scenario_artifact,
    )

    original_load_module = replay.load_module

    def patched_load_module(path: Path, name: str):
        module = original_load_module(path, name)
        if name == "current_full_brain_bridge_v2":
            original_cycle = module.run_full_brain_cycle

            def wrapped_cycle(**kwargs: Any):
                enriched = dict(kwargs)
                query_as_of = enriched.get("query_as_of")
                event_row = dict(enriched.get("row") or {})
                memory = provider.evidence(query_as_of, event_row)
                enriched["historical_evidence"] = {
                    "status": memory["status"],
                    "memory_role": memory["memory_role"],
                    "sources": memory["sources"],
                    "governance": memory["governance"],
                    "query_as_of": memory["query_as_of"],
                }
                result = original_cycle(**enriched)
                if isinstance(result, dict):
                    result.setdefault("provenance", {}).update({
                        "historical_memory_provider": "current_stack_historical_memory_provider_v1",
                        "memory_full_stack_wired": True,
                        "memory_evidence_only": True,
                        "similarity_snapshot_reuse_forbidden": True,
                        "retrieval_snapshot_reuse_forbidden": True,
                        "scenario_snapshot_reuse_forbidden": True,
                    })
                    result.setdefault("historical_memory", memory)
                return result

            module.run_full_brain_cycle = wrapped_cycle
        return module

    replay.load_module = patched_load_module
    replay.run(h1, market_state, murphy, nison, mtf, output_dir)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    for arg in ["h1", "market_state", "murphy", "nison", "mtf", "historical_context", "historical_outcome", "similarity_artifact", "retrieval_artifact", "scenario_artifact", "output_dir"]:
        p.add_argument(f"--{arg.replace('_','-')}", required=True, type=Path)
    a = p.parse_args()
    run(a.h1, a.market_state, a.murphy, a.nison, a.mtf, a.historical_context, a.historical_outcome, a.similarity_artifact, a.retrieval_artifact, a.scenario_artifact, a.output_dir)
