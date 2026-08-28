from __future__ import annotations
import ast
from pathlib import Path

TARGETS = [
    Path("BACKTEST/CANONICAL_E2E_ORCHESTRATOR_V2.py"),
    Path("BACKTEST/CIRCLECI_RUN_GOVERNED_BACKTEST.py"),
    Path("BACKTEST/CIRCLECI_RUN_GOVERNED_GATE.py"),
]
FORBIDDEN = {
    "similarity=None": "similarity_null_pass",
    'tiz_status\": \"UNRESOLVED_OPTIONAL\"': "tiz_placeholder_in_event_path",
    "equity=100000.0": "synthetic_equity",
    "peak_equity=100000.0": "synthetic_peak_equity",
}

def main() -> int:
    failures: list[str] = []
    for p in TARGETS:
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        for needle, reason in FORBIDDEN.items():
            if needle in text:
                failures.append(f"{p}: {reason}")
    # Brain and book source files must not be modified by this gate.
    protected = [
        Path("RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py"),
        Path("01_MURPHY"),
        Path("02_NISON"),
    ]
    for p in protected:
        if p.is_file() and p.name == "decision_brain.py":
            try:
                ast.parse(p.read_text(encoding="utf-8"))
            except SyntaxError as exc:
                failures.append(f"{p}: syntax_error:{exc}")
    if failures:
        print("GOVERNED_RUNNER_V3_STATIC_GATE: FAIL")
        for f in failures:
            print(f" - {f}")
        return 1
    print("GOVERNED_RUNNER_V3_STATIC_GATE: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
