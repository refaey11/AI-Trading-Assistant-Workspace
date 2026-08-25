"""CI visibility helpers for compatibility diagnostics.

This hook does not alter test behavior or trading logic. It only re-emits
captured pytest warnings so long-running CircleCI diagnostics remain visible
when tests otherwise pass and pytest hides warning details behind capture.
"""


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    warnings = terminalreporter.stats.get("warnings", [])
    diagnostics = []
    for warning in warnings:
        message = str(getattr(warning, "message", ""))
        if "FINAL_2025_NO_TRADE_DIAGNOSTIC=" in message:
            diagnostics.append(message)
    if diagnostics:
        tw = terminalreporter.write_sep("=", "FINAL 2025 DIAGNOSTIC")
        for message in diagnostics:
            terminalreporter.write_line(message, yellow=False, bold=True)
