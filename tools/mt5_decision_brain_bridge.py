#!/usr/bin/env python3
"""
Decision Brain V1 <-> MetaTrader 5 local bridge.

This is an execution-neutral display bridge:
- MT5 supplies current multi-timeframe market features.
- The existing recovered Decision Brain V1 performs the assessment.
- No trading orders are placed.
- No project rules are modified.
"""

from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRAIN_PATH = ROOT / "RECOVERED_SOURCES" / "DECISION_BRAIN_V1" / "decision_brain.py"

import importlib.util

spec = importlib.util.spec_from_file_location("decision_brain_v1", BRAIN_PATH)
if not spec or not spec.loader:
    raise RuntimeError(f"Cannot load {BRAIN_PATH}")
brain = importlib.util.module_from_spec(spec)
spec.loader.exec_module(brain)


def assessment_payload(row: dict) -> dict:
    a = brain.assess(row, similarity=None)
    return {
        "version": "DECISION_BRAIN_MT5_BRIDGE_V1",
        "market_state": a.market_state,
        "directional_bias": a.directional_bias,
        "confidence": float(a.confidence),
        "evidence": a.evidence,
        "contradictions": a.contradictions,
        "no_trade_reasons": a.no_trade_reasons,
        "order_execution": "DISABLED",
        "official_profitability_claim_allowed": False,
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "DecisionBrainMT5Bridge/1.0"

    def _reply(self, code: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._reply(200, {"status": "ok", "brain": "DECISION_BRAIN_V1", "orders": "disabled"})
        else:
            self._reply(404, {"error": "not_found"})

    def do_POST(self):
        if self.path != "/assess":
            self._reply(404, {"error": "not_found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 1_000_000:
                raise ValueError("invalid request size")
            row = json.loads(self.rfile.read(length).decode("utf-8"))
            if not isinstance(row, dict):
                raise ValueError("JSON body must be an object")
            self._reply(200, assessment_payload(row))
        except Exception as exc:
            self._reply(400, {"error": str(exc), "order_execution": "DISABLED"})

    def log_message(self, fmt, *args):
        print("[MT5]", fmt % args, flush=True)


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8765
    print(f"Decision Brain MT5 bridge listening on http://{host}:{port}", flush=True)
    print(f"Loaded: {BRAIN_PATH}", flush=True)
    ThreadingHTTPServer((host, port), Handler).serve_forever()
