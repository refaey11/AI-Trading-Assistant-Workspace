//+------------------------------------------------------------------+
//| MT5 Forex Filter Diagnostic V1                                   |
//| Read-only symbol-property audit. No bars, indicators, or trades. |
//+------------------------------------------------------------------+
#property strict
#property version   "1.00"
#property script_show_inputs
#property description "Audits Market Watch symbol properties against the V1.2 forex filter. Read-only."

input string OutputFileName = "mt5_forex_filter_diagnostic_v1.csv";

string g_supported_currency_codes[] =
{
   "AED","AFN","ALL","AMD","ANG","AOA","ARS","AUD","AWG","AZN",
   "BAM","BBD","BDT","BGN","BHD","BIF","BMD","BND","BOB","BRL",
   "BSD","BTN","BWP","BYN","BZD","CAD","CDF","CHF","CLP","CNY",
   "CNH","COP","CRC","CUP","CVE","CZK","DJF","DKK","DOP","DZD",
   "EGP","ERN","ETB","EUR","FJD","FKP","GBP","GEL","GHS","GIP",
   "GMD","GNF","GTQ","GYD","HKD","HNL","HRK","HTG","HUF","IDR",
   "ILS","INR","IQD","IRR","ISK","JMD","JOD","JPY","KES","KGS",
   "KHR","KMF","KPW","KRW","KWD","KYD","KZT","LAK","LBP","LKR",
   "LRD","LSL","LYD","MAD","MDL","MGA","MKD","MMK","MNT","MOP",
   "MRU","MUR","MVR","MWK","MXN","MYR","MZN","NAD","NGN","NIO",
   "NOK","NPR","NZD","OMR","PAB","PEN","PGK","PHP","PKR","PLN",
   "PYG","QAR","RON","RSD","RUB","RUR","RWF","SAR","SBD","SCR",
   "SDG","SEK","SGD","SHP","SLE","SLL","SOS","SRD","SSP","STN",
   "SVC","SYP","SZL","THB","TJS","TMT","TND","TOP","TRY","TTD",
   "TWD","TZS","UAH","UGX","USD","UYU","UZS","VES","VND","VUV",
   "WST","XAF","XCD","XOF","XPF","YER","ZAR","ZMW","ZWG"
};

bool IsSupportedCurrencyCode(const string code)
{
   if(StringLen(code) != 3)
      return false;
   for(int i = 0; i < ArraySize(g_supported_currency_codes); i++)
      if(code == g_supported_currency_codes[i])
         return true;
   return false;
}

void OnStart()
{
   int file = FileOpen(OutputFileName,
                       FILE_WRITE|FILE_CSV|FILE_COMMON|FILE_ANSI,
                       ',');
   if(file == INVALID_HANDLE)
   {
      Print("FOREX DIAGNOSTIC ERROR: FileOpen failed. Error=", GetLastError());
      return;
   }

   FileWrite(file,
      "symbol",
      "calc_mode_numeric",
      "calc_mode_name",
      "base_currency",
      "profit_currency",
      "calc_mode_is_forex",
      "base_code_supported",
      "profit_code_supported",
      "filter_result",
      "filter_reason"
   );

   int total = SymbolsTotal(true);
   int accepted = 0;
   int rejected = 0;
   int property_errors = 0;

   for(int i = 0; i < total; i++)
   {
      string symbol = SymbolName(i, true);
      if(symbol == "")
         continue;

      long calc_mode = -1;
      string base_currency = "";
      string profit_currency = "";

      bool calc_ok = SymbolInfoInteger(symbol, SYMBOL_TRADE_CALC_MODE, calc_mode);
      bool base_ok = SymbolInfoString(symbol, SYMBOL_CURRENCY_BASE, base_currency);
      bool profit_ok = SymbolInfoString(symbol, SYMBOL_CURRENCY_PROFIT, profit_currency);

      bool calc_is_forex = (calc_ok &&
         (calc_mode == SYMBOL_CALC_MODE_FOREX ||
          calc_mode == SYMBOL_CALC_MODE_FOREX_NO_LEVERAGE));
      bool base_supported = (base_ok && IsSupportedCurrencyCode(base_currency));
      bool profit_supported = (profit_ok && IsSupportedCurrencyCode(profit_currency));

      string result = "REJECT";
      string reason = "";

      if(!calc_ok || !base_ok || !profit_ok)
      {
         reason = "SYMBOL_PROPERTY_UNAVAILABLE";
         property_errors++;
      }
      else if(!calc_is_forex)
         reason = "CALC_MODE_NOT_FOREX";
      else if(base_currency == profit_currency)
         reason = "BASE_EQUALS_PROFIT";
      else if(!base_supported)
         reason = "BASE_CURRENCY_NOT_ALLOWLISTED";
      else if(!profit_supported)
         reason = "PROFIT_CURRENCY_NOT_ALLOWLISTED";
      else
      {
         result = "ACCEPT";
         reason = "PASSES_V1_2_FILTER";
         accepted++;
      }

      if(result == "REJECT")
         rejected++;

      string calc_name = calc_ok ?
         EnumToString((ENUM_SYMBOL_CALC_MODE)calc_mode) : "UNAVAILABLE";

      FileWrite(file,
         symbol,
         calc_ok ? IntegerToString((int)calc_mode) : "UNAVAILABLE",
         calc_name,
         base_ok ? base_currency : "UNAVAILABLE",
         profit_ok ? profit_currency : "UNAVAILABLE",
         calc_is_forex ? "true" : "false",
         base_supported ? "true" : "false",
         profit_supported ? "true" : "false",
         result,
         reason
      );
   }

   FileFlush(file);
   FileClose(file);

   Print("FOREX FILTER DIAGNOSTIC V1 COMPLETE. Read-only audit; no market data captured and no trading functions called.");
   Print("Market Watch symbols=", total,
         "; accepted=", accepted,
         "; rejected=", rejected,
         "; property_errors=", property_errors,
         "; report=Common Files/", OutputFileName);
}
//+------------------------------------------------------------------+
