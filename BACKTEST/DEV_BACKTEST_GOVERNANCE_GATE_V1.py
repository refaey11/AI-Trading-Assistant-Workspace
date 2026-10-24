from __future__ import annotations

"""Static governance gate for DEV_BACKTEST_RUNNER_V1.

This is a validation layer only. It does not create a second backtest engine,
change Murphy/Nison rules, or tune any strategy parameter. It prevents the
current diagnostic runner from being mistaken for the governed final run.
"""

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "BACKTEST/DEV_BACKTEST_RUNNER_V1.py"
ALLOWLIST = ROOT / "governance/DECISION_BRAIN_RULE_ALLOWLIST_V1.json"

REQUIRED_GOVERNANCE_MARKERS = {
    "official_claim_allowed": "official claim must be explicitly gated",
    "costs_applied": "frozen costs must be applied",
    "frozen_cost_slippage": "frozen cost/slippage state must be recorded",
}


def read_runner() -> str:
    return RUNNER.read_text(encoding="utf-8")


def check_python_syntax(source: str) -> None:
    ast.parse(source, filename=str(RUNNER))


def check_allowlist() -> list[str]:
    data = json.loads(ALLOWLIST.read_text(encoding="utf-8"))
    verified = data["verified_runtime"]
    murphy = set(verified["MURPHY"])
    nison = set(verified["NISON"])
    if len(murphy) != 34:
        raise AssertionError(f"expected 34 Murphy rules, found {len(murphy)}")
    if len(nison) != 44:
        raise AssertionError(f"expected 44 Nison rules, found {len(nison)}")
    if "MURPHY_0008" in murphy:
        raise AssertionError("MURPHY_0008 must remain blocked")
    return sorted(murphy | nison)


def main() -> int:
    source = read_runner()
    check_python_syntax(source)
    rule_ids = check_allowlist()

    failures: list[str] = []
    for marker, reason in REQUIRED_GOVERNANCE_MARKERS.items():
        if marker not in source:
            failures.append(f"missing runner governance marker {marker!r}: {reason}")

    # The current runner explicitly contains a diagnostic state. Keep the gate
    # honest: diagnostic output is not allowed to masquerade as final.
    if "DIAGNOSTIC_NOT_OFFICIAL" in source and "official_profitability_claim" in source:
        failures.append("runner is still explicitly diagnostic; do not publish profitability as official")

    # 2025 must never be mixed into the 2016-2024 development run.
    if "<= 2024" not in source or ">= 2016" not in source:
        failures.append("2016-2024 development window is not statically visible")

    print(f"verified runtime allowlist: {len(rule_ids)} rules")
    if failures:
        print("GOVERNANCE_GATE=FAIL")
        for item in failures:
            print(f"- {item}")
        return 1

    print("GOVERNANCE_GATE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
