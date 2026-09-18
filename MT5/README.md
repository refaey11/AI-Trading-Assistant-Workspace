# MetaTrader 5 — Decision Brain V1 Display Bridge

This integration does **not** rebuild the Decision Brain and does **not** place trades.

## Components

- `MT5/Decision_Brain_V1.mq5` — MT5 indicator/panel.
- `tools/mt5_decision_brain_bridge.py` — local HTTP bridge.
- Existing source used unchanged:
  `RECOVERED_SOURCES/DECISION_BRAIN_V1/decision_brain.py`.

## Run locally

From the repository root:

```bash
python tools/mt5_decision_brain_bridge.py
```

The bridge listens only on:

```
http://127.0.0.1:8765
```

Health check:

```
http://127.0.0.1:8765/health
```

## Install the MT5 indicator

Copy `MT5/Decision_Brain_V1.mq5` into:

```
MQL5/Indicators/
```

Compile it in MetaEditor and attach it to a chart.

In MT5, allow the indicator to call:

```
http://127.0.0.1:8765
```

under **Tools → Options → Expert Advisors → Allow WebRequest for listed URL**.

## What it does

Every few seconds the indicator sends current M5/M15/M30/H1/H4/D1 trend-regime features to the existing Brain V1 and displays:

- market state
- directional bias
- confidence
- Brain status
- explicit indication that order execution is disabled

The MT5-side regime calculation is a display/runtime adapter only. It does not modify the governed rule registry.

## Important boundary

This V1 is an **analysis indicator**, not an auto-trading Expert Advisor.

It deliberately keeps:
- order execution disabled
- official profitability claims disabled
- volume confirmation unavailable unless a source-backed volume field is supplied

The next integration step, after live observation is stable, is to connect the governed Murphy/Nison evidence stream rather than inventing new trading rules inside MQL5.
