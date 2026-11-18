# MT5 Forex Filter Diagnostic V1

## Purpose
A separate, read-only MetaTrader 5 script to audit the symbol properties used by the V1.2 forex-only capture filter.

## Safety boundary
- Reads only symbols currently visible in Market Watch.
- Reads `SYMBOL_TRADE_CALC_MODE`, `SYMBOL_CURRENCY_BASE`, and `SYMBOL_CURRENCY_PROFIT`.
- Uses the same versioned currency-code allowlist as MT5 Forex-Only Raw Capture V1.2.
- Does not call `CopyRates`, collect candles, calculate indicators, create signals, size risk, submit orders, or modify positions.
- Writes a separate diagnostic CSV. It does not read, overwrite, or append to any V1/V1.1/V1.2 capture file.
- This is a diagnostic aid, not proof of broker-wide instrument classification. It audits only the currently visible Market Watch list.

## Output
`mt5_forex_filter_diagnostic_v1.csv` in the MT5 Common Files directory.

The report includes each symbol, calculation mode (numeric and enum name), base/profit currencies, each filter condition, ACCEPT/REJECT, and a reason.

The Experts log prints accepted/rejected totals and the report filename.

## How to run
1. Compile `MT5_Forex_Filter_Diagnostic_V1.mq5` in MetaEditor.
2. In MT5, open Navigator > Scripts and refresh if needed.
3. Drag **MT5_Forex_Filter_Diagnostic_V1** onto any chart once.
4. The script runs once and exits. It does not require the V1.2 capture EA to be stopped.
5. Read the Experts log for the totals. The CSV is in File > Open Data Folder > go up one level to `TerminalCommonFiles`.

Do not change the V1.2 capture EA or its existing CSV as part of this diagnostic.
