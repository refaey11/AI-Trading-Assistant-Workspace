from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Iterable, Mapping

ALLOWLIST_PATH = Path("governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json")

# These are existing runtime entrypoints only. This registry does not implement
# any rule semantics; it reports whether the already-existing runtime surface
# is present and usable from the repository checkout.
SHARED_MURPHY_ENTRYPOINT = Path("MURPHY_EVALUATORS_V1/murphy_runtime_entrypoint_v1.py")
MURPHY_0003_0004_ENTRYPOINT = Path("audits/MURPHY_0003_0004_EVALUATOR_V2/murphy_0003_0004_evaluator_v2.py")
MURPHY_0021_0023_BRIDGE = Path("bridges/murphy_0021_0023_evaluator_to_evidence_bridge.py")
MURPHY_0034_0045_ENTRYPOINT = Path("runtime/murphy_0034_0045_runtime.py")
MURPHY_0050_ENTRYPOINT = Path("MURPHY_EVALUATORS_V1/murphy_0050_evaluator.py")
NISON_ROUTER = Path("RUNTIME/NISON_EVALUATORS_V1/nison_0001_0010_router.py")
NISON_RUNTIME_DIR = Path("RUNTIME/NISON_EVALUATORS_V1")


def _load_allowlist(root: Path) -> dict:
    return json.loads((root / ALLOWLIST_PATH).read_text(encoding="utf-8"))


def _nison_runtime_surface(root: Path) -> dict[str, object]:
    required = [
        "nison_0001_0002_engulfing.py",
        "nison_0003_0010_runtime.py",
        "nison_0011_0020_runtime.py",
        "nison_0021_0030_runtime.py",
        "nison_0031_0044_runtime.py",
        "nison_0001_0010_router.py",
    ]
    missing = [name for name in required if not (root / NISON_RUNTIME_DIR / name).exists()]
    return {
        "entrypoint_available": not missing,
        "missing_files": missing,
        "entrypoint": str(NISON_ROUTER),
    }


def _murphy_entrypoint_surface(root: Path, rule_id: str) -> dict[str, object]:
    numeric = int(rule_id[-4:])
    if rule_id in {"MURPHY_0003", "MURPHY_0004"}:
        path = MURPHY_0003_0004_ENTRYPOINT
    elif rule_id in {"MURPHY_0021", "MURPHY_0022", "MURPHY_0023"}:
        path = MURPHY_0021_0023_BRIDGE
    elif 34 <= numeric <= 45:
        path = MURPHY_0034_0045_ENTRYPOINT
    elif rule_id == "MURPHY_0050":
        path = MURPHY_0050_ENTRYPOINT
    else:
        path = SHARED_MURPHY_ENTRYPOINT

    exists = (root / path).exists()
    dependency_missing = False
    dependency = None
    if rule_id in {f"MURPHY_{i:04d}" for i in range(34, 46)} and exists:
        dependency = "murphy_batch_evaluators"
        dependency_missing = not any(
            (root / candidate).exists()
            for candidate in (
                Path("murphy_batch_evaluators.py"),
                Path("RUNTIME/murphy_batch_evaluators.py"),
                Path("MURPHY_EVALUATORS_V1/murphy_batch_evaluators.py"),
            )
        )

    return {
        "entrypoint": str(path),
        "entrypoint_available": exists,
        "dependency_missing": dependency_missing,
        "missing_dependency": dependency,
    }


def assess_runtime_coverage(root: str | Path, observed_rule_ids: Iterable[str] = ()) -> dict:
    """Audit runtime surface and observed 2025 rule coverage without executing rules."""
    repo_root = Path(root)
    allowlist = _load_allowlist(repo_root)
    murphy = list(allowlist["verified_runtime"]["MURPHY"])
    nison = list(allowlist["verified_runtime"]["NISON"])
    allowed = set(murphy) | set(nison)

    observed = sorted({str(x) for x in observed_rule_ids if str(x)})
    rejected_observed = sorted(set(observed) - allowed)
    observed_allowed = sorted(set(observed) & allowed)

    murphy_surface = {rule_id: _murphy_entrypoint_surface(repo_root, rule_id) for rule_id in murphy}
    nison_surface = _nison_runtime_surface(repo_root)

    runtime_available = []
    runtime_blocked = []
    for rule_id, surface in murphy_surface.items():
        if surface["entrypoint_available"] and not surface["dependency_missing"]:
            runtime_available.append(rule_id)
        else:
            runtime_blocked.append(rule_id)

    if nison_surface["entrypoint_available"]:
        runtime_available.extend(nison)
    else:
        runtime_blocked.extend(nison)

    return {
        "status": "PASS",
        "scope": {"murphy": len(murphy), "nison": len(nison), "total": len(allowed)},
        "runtime_surface": {
            "entrypoint_available_count": len(runtime_available),
            "entrypoint_blocked_count": len(runtime_blocked),
            "blocked_rules": sorted(runtime_blocked),
            "nison_surface": nison_surface,
            "murphy_surface": murphy_surface,
        },
        "observed_2025": {
            "observed_count": len(observed_allowed),
            "observed_rule_ids": observed_allowed,
            "coverage_pct": (100.0 * len(observed_allowed) / len(allowed)) if allowed else 0.0,
            "rejected_observed_rule_ids": rejected_observed,
        },
        "governance": {
            "2025_oos": True,
            "execution": "read_only_preflight",
            "generates_decisions": False,
            "generates_sl_tp": False,
            "tiz_semantics_created": False,
            "risk_semantics_created": False,
        },
        "authorization": {
            "fresh_2025_decision_event_stream": False,
            "reason": "This preflight inventories existing runtime surfaces; it does not synthesize the missing central 2025 event producer.",
        },
    }
