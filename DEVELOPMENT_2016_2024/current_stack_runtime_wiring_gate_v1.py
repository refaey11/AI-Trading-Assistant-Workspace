from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = {
    "replay": ROOT / "DEVELOPMENT_2016_2024/current_stack_historical_replay_v2.py",
    "runtime_bridge": ROOT / "RUNTIME/DECISION_RUNTIME_V1/full_brain_runtime_bridge_v1.py",
    "decision_brain": ROOT / "RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py",
    "handoff": ROOT / "compatibility/decision_brain_v1_handoff_adapter.py",
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

    if "replay" in texts:
        replay = texts["replay"]
        forbidden = {
            "historical_evidence=None": "historical_evidence must be populated from historical memory/retrieval for the full-stack replay",
            "similarity=None": "similarity evidence must not be hard-null when the component is declared mandatory",
        }
        for needle, reason in forbidden.items():
            if needle in replay:
                failures.append(f"REPLAY_NOT_WIRED:{needle}:{reason}")

        require(
            replay,
            ["historical_context", "historical_outcome", "similarity_memory", "context_retrieval", "scenario_engine"],
            "REPLAY_SOURCE_WIRING",
            failures,
        )
        report["checks"]["replay"].update({
            "historical_evidence_populated": "historical_evidence=None" not in replay,
            "similarity_not_hard_null": "similarity=None" not in replay,
            "memory_and_retrieval_sources_referenced": all(x in replay for x in ["historical_context", "historical_outcome", "similarity_memory", "context_retrieval"]),
            "scenario_source_referenced": "scenario_engine" in replay,
        })

    if "runtime_bridge" in texts:
        require(texts["runtime_bridge"], ["historical_evidence", "nison_evidence", "risk_evidence", "tiz_evidence"], "RUNTIME_BRIDGE_INPUTS", failures)

    if "decision_brain" in texts:
        require(texts["decision_brain"], ["def assess(", "similarity"], "DECISION_BRAIN_MEMORY_HOOK", failures)

    if "handoff" in texts:
        require(texts["handoff"], ["historical_evidence"], "HANDOFF_HISTORICAL_HOOK", failures)

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
