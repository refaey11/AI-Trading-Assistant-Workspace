from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = {
    "replay_v2_engine": ROOT / "DEVELOPMENT_2016_2024/current_stack_historical_replay_v2.py",
    "replay_v3_wiring": ROOT / "DEVELOPMENT_2016_2024/current_stack_historical_replay_v3.py",
    "memory_provider": ROOT / "DEVELOPMENT_2016_2024/current_stack_historical_memory_provider_v1.py",
    "runtime_bridge": ROOT / "RUNTIME/DECISION_RUNTIME_V1/full_brain_runtime_bridge_v1.py",
    "decision_brain": ROOT / "RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py",
    "handoff": ROOT / "compatibility/decision_brain_v1_handoff_adapter.py",
    "memory_handoff": ROOT / "compatibility/memory_decision_handoff_adapter_v1.py",
    "memory_shadow_bridge": ROOT / "compatibility/memory_evidence_shadow_bridge_v1.py",
    "evaluator": ROOT / "evaluation/three_book_decision_evaluator_v1.py",
}


def require(text: str, markers: list[str], label: str, failures: list[str]) -> None:
    missing = [m for m in markers if m not in text]
    if missing:
        failures.append(f"{label}:missing={missing}")


def main() -> None:
    failures: list[str] = []
    report = {
        "gate": "CURRENT_STACK_RUNTIME_WIRING_V1",
        "window": "2016-2024",
        "status": "PASS",
        "checks": {},
        "failures": failures,
    }

    texts: dict[str, str] = {}
    for name, path in FILES.items():
        if not path.is_file():
            failures.append(f"FILE_MISSING:{name}:{path}")
            continue
        texts[name] = path.read_text(encoding="utf-8")
        report["checks"][name] = {"present": True}

    if "replay_v3_wiring" in texts:
        replay = texts["replay_v3_wiring"]
        require(
            replay,
            [
                "HistoricalMemoryProvider",
                "historical_context",
                "historical_outcome",
                "similarity_artifact",
                "retrieval_artifact",
                "scenario_artifact",
                "historical_evidence",
                "memory_full_stack_wired",
            ],
            "REPLAY_V3_MEMORY_WIRING",
            failures,
        )
        if "historical_evidence=None" in replay or "similarity=None" in replay:
            failures.append("REPLAY_V3_NOT_WIRED:hard-null-memory-input")
        report["checks"]["replay_v3_wiring"].update({
            "historical_memory_provider_invoked": "HistoricalMemoryProvider" in replay and "provider.evidence" in replay,
            "historical_evidence_injected": "historical_evidence" in replay and "provider.evidence" in replay,
            "similarity_artifact_referenced": "similarity_artifact" in replay,
            "retrieval_artifact_referenced": "retrieval_artifact" in replay,
            "scenario_artifact_referenced": "scenario_artifact" in replay,
            "memory_full_stack_wired_marker": "memory_full_stack_wired" in replay,
        })

    if "memory_provider" in texts:
        provider = texts["memory_provider"]
        require(provider, ["historical_context", "historical_outcome", "similarity", "context_aware_retrieval", "scenario_engine"], "MEMORY_PROVIDER_SOURCES", failures)
        require(provider, ["query_as_of", "LOCKED_OOS_YEAR", "future_data_used", "predicted_return_used_as_direction"], "MEMORY_PROVIDER_GOVERNANCE", failures)

    if "runtime_bridge" in texts:
        require(texts["runtime_bridge"], ["historical_evidence", "nison_evidence", "risk_evidence", "tiz_evidence"], "RUNTIME_BRIDGE_INPUTS", failures)

    if "decision_brain" in texts:
        require(texts["decision_brain"], ["def assess(", "similarity"], "DECISION_BRAIN_HOOK", failures)

    if "handoff" in texts:
        require(texts["handoff"], ["historical_evidence", "consumed_by_decision_boundary", "predicted_return_used_as_direction"], "BRAIN_MEMORY_HANDOFF", failures)

    if "memory_handoff" in texts:
        require(texts["memory_handoff"], ["build_memory_handoff", "historical_context", "historical_outcome", "similarity", "context_aware_retrieval"], "MEMORY_HANDOFF_ADAPTER", failures)

    if "memory_shadow_bridge" in texts:
        require(texts["memory_shadow_bridge"], ["EVIDENCE_ONLY", "future_data_allowed", "memory_generated_direction"], "MEMORY_SHADOW_GOVERNANCE", failures)

    if "evaluator" in texts:
        require(texts["evaluator"], ["NISON_CONTRADICTION", "risk_pass", "BUY", "SELL"], "THREE_BOOK_CONTRACT", failures)

    if failures:
        report["status"] = "BLOCKED"

    out = Path("artifacts/runtime_wiring")
    out.mkdir(parents=True, exist_ok=True)
    (out / "current_stack_runtime_wiring_2016_2024.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    if failures:
        raise SystemExit("BLOCKED_CURRENT_STACK_RUNTIME_WIRING")


if __name__ == "__main__":
    main()
