# Nison Official Scanner Research — 2026-08-24

## Research question
Can the official Steve Nison Candle Scanner be used to close the current Nison upstream-evidence gap for the Decision Brain?

## Verified official capabilities
- Nison Candle Scanner for TradingView scans/highlights/alerts candlestick patterns in real time.
- The official product describes 28 selected candlestick patterns, with Standard and Strict Criteria, plus NCS PRO modules including Intraday, FX, and Crypto.
- The official TradingView product page states the scanner can be configured for scans/alerts and that alert history can be exported from the alert log.
- TradingView officially supports webhook delivery for alerts to an external HTTP endpoint. Alert messages can be JSON; webhook requests are sent as HTTP POST. Webhook use requires 2FA.

## Important limitation for the current OOS problem
The official material reviewed does NOT establish a public API or a documented historical bulk-export interface that can reproduce 2025 Nison evidence for our exact frozen NISON_0001..NISON_0044 contracts.

TradingView alert logs are also operationally limited: older trigger records are automatically deleted, and TradingView recommends exporting the log as CSV before cleanup. Therefore, this is not sufficient by itself as a retroactive 2025 evidence source unless the required historical alerts were already retained/exported.

## Architectural decision
1. Do NOT replace the frozen Nison contracts with the external scanner output.
2. Do NOT use a third-party detector as if it were canonical Steve Nison evidence.
3. Treat official Nison Scanner output as a potential authoritative upstream candidate for FUTURE/live evidence, subject to field-level compatibility mapping and provenance capture.
4. For 2025 OOS, keep existing fail-closed behavior unless an authoritative historical evidence export can be obtained.
5. If the official scanner can emit webhook/alert payloads containing the required pattern identity and context, build a thin upstream adapter into the existing Nison source adapter; do not change Nison semantics.
6. Preserve Nison role as confirmation/contradiction only.

## Result
The web research found a viable FUTURE evidence-ingestion path (official Nison Scanner -> TradingView alert/webhook -> project evidence adapter), but did NOT prove a clean retroactive 2025 solution.

## Sources
- Candlecharts official Nison Candle Scanner for TradingView: https://specials.candlecharts.com/ncstva/
- Candlecharts TradingView product page: https://candlecharts.com/product-details/trading-view-landing/
- TradingView webhook documentation: https://www.tradingview.com/support/solutions/43000529348-how-to-configure-webhook-alerts/
- TradingView alert log/export documentation: https://www.tradingview.com/support/solutions/43000595311-manage-alerts/
- TradingView alert retention documentation: https://www.tradingview.com/support/solutions/43000766116-automatic-deletion-of-old-alert-triggers-from-the-log/
