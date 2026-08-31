from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]

REPO_FILES = {
    "decision_brain": "RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py",
    "decision_brain_spec": "RECOVERED_SOURCES/DECISION_BRAIN_V1/DECISION_BRAIN_V1_SPEC.json",
    "runtime_bridge": "RUNTIME/DECISION_RUNTIME_V1/full_brain_runtime_bridge_v1.py",
    "three_book_evaluator": "evaluation/three_book_decision_evaluator_v1.py",
    "brain_handoff": "compatibility/decision_brain_v1_handoff_adapter.py",
    "risk_runtime": "risk_engine/risk_execution_runtime_v1.py",
    "execution_adapter": "OOS_2025/execution_oos_adapter_v1.py",
    "execution_compatibility": "OOS_2025/execution_oos_compatibility_v1.py",
    "risk_profile": "OOS_2025/frozen_candidate_risk_profile_v1.py",
    "tiz_boundary": "03_TIZ/TIZ_RUNTIME_BOUNDARY_RESOLUTION_V2.json",
    "rule_allowlist": "governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json",
    "current_replay": "DEVELOPMENT_2016_2024/current_stack_historical_replay_v2.py",
    "adapters_dir": "ADAPTERS",
}

DROPBOX_FILES = {
    "h1_source": "/New 8/GBPUSD_H1_2016_2025_MASTER.zip",
    "murphy_source": "/New 8/MURPHY_HISTORICAL_34_RULE_FANIN_2016_2024.zip",
    "nison_source": "/New 8/NISON_2016_2024_FULL_EVIDENCE.csv",
    "market_state": "/New 8/GBPUSD_MARKET_STATE 6.csv",
    "mtf_source": "/MTF_ALIGNMENT_GBPUSD_V1.zip",
    "historical_context": "/ai_trading_assistant_full_project_v1/AI_Trading_Assistant_HISTORICAL_CONTEXT_MEMORY_V1/HISTORICAL_CONTEXT_MEMORY.csv",
    "historical_outcome": "/ai_trading_assistant_full_project_v1/AI_Trading_Assistant_HISTORICAL_OUTCOME_MEMORY_V1/HISTORICAL_OUTCOMES.csv",
    "similarity_memory": "/ai_trading_assistant_full_project_v1/AI_Trading_Assistant_SIMILARITY_MEMORY_V2/SIMILAR_CONTEXT_READS.json",
    "context_retrieval": "/ai_trading_assistant_full_project_v1/AI_Trading_Assistant_CONTEXT_AWARE_RETRIEVAL_V2/CONTEXT_AWARE_READINGS.json",
    "scenario_engine": "/AI_Trading_Assistant_FULL_PROJECT_V1/AI_Trading_Assistant_MARKET_SCENARIO_ENGINE_V1.zip",
}

ROLE_ASSERTIONS = {
    "decision_brain": ["def assess(", "similarity"],
    "runtime_bridge": ["historical_evidence", "nison_evidence", "risk_evidence", "tiz_evidence"],
    "three_book_evaluator": ["NISON_CONTRADICTION", "risk_pass", "BUY", "SELL"],
    "brain_handoff": ["historical_evidence", "predicted_return_used_as_direction", "similarity=None"],
    "risk_runtime": ["RiskRequest", "risk_budget_locked", "ALLOWED_RISK_PROFILES"],
    "execution_adapter": ["0.75 ATR", "2R target"],
}


def dropbox_metadata(path: str, token: str) -> dict:
    req = Request(
        "https://api.dropboxapi.com/2/files/get_metadata",
        data=json.dumps({"path": path}).encode(),
        method="POST",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    with urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def main() -> None:
    report: dict = {
        "gate": "CURRENT_STACK_COMPONENT_COMPLETENESS_V1",
        "window": "2016-2024",
        "status": "PASS",
        "repo": {},
        "dropbox": {},
        "role_assertions": {},
        "missing": [],
        "contract_failures": [],
    }

    for name, rel in REPO_FILES.items():
        p = ROOT / rel
        ok = p.is_dir() if name.endswith("_dir") else p.is_file()
        report["repo"][name] = {"path": rel, "present": ok}
        if not ok:
            report["missing"].append(f"REPO:{name}:{rel}")

    for name, needles in ROLE_ASSERTIONS.items():
        rel = REPO_FILES[name]
        p = ROOT / rel
        text = p.read_text(encoding="utf-8") if p.is_file() else ""
        failed = [needle for needle in needles if needle not in text]
        report["role_assertions"][name] = {"required_markers": needles, "failed": failed, "contract_valid": not failed}
        if failed:
            report["contract_failures"].append(f"ROLE:{name}:{','.join(failed)}")

    token = os.environ.get("DROPBOX_ACCESS_TOKEN", "").strip().removeprefix("Bearer ").strip('"')
    if not token:
        raise SystemExit("BLOCKED_COMPONENT_GATE_NO_DROPBOX_TOKEN")

    for name, path in DROPBOX_FILES.items():
        try:
            meta = dropbox_metadata(path, token)
            report["dropbox"][name] = {
                "path": path,
                "present": True,
                "object_type": meta.get(".tag"),
                "size": meta.get("size"),
                "server_modified": meta.get("server_modified"),
            }
        except Exception as exc:
            report["dropbox"][name] = {"path": path, "present": False, "error": str(exc)}
            report["missing"].append(f"DROPBOX:{name}:{path}")

    if report["missing"] or report["contract_failures"]:
        report["status"] = "BLOCKED"

    out = Path("artifacts/component_completeness")
    out.mkdir(parents=True, exist_ok=True)
    (out / "current_stack_component_completeness_2016_2024.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    if report["status"] != "PASS":
        raise SystemExit("BLOCKED_CURRENT_STACK_COMPONENT_COMPLETENESS")


if __name__ == "__main__":
    main()
