//+------------------------------------------------------------------+
//| MT5 Forex-Only Raw Capture V1.1                                  |
//| Data export only: NO trade requests, indicators, or signals.     |
//+------------------------------------------------------------------+
#property strict
#property version   "1.20"
#property description "Exports latest closed FX bars only. Never trades."

input int    CaptureIntervalSeconds = 10;
input string OutputFileName = "mt5_raw_capture_fx_v1_1.csv";
input bool   CaptureForexOnly = true;

ENUM_TIMEFRAMES g_timeframes[] = {PERIOD_M5, PERIOD_M15, PERIOD_M30, PERIOD_H1, PERIOD_H4, PERIOD_D1};
string g_tf_names[] = {"M5", "M15", "M30", "H1", "H4", "D1"};
string g_seen_keys[];
datetime g_seen_bar_times[];

string IsoUtc(const datetime value)
{
   MqlDateTime t;
   TimeToStruct(value, t);
   return StringFormat("%04d-%02d-%02dT%02d:%02d:%02dZ",
                       t.year, t.mon, t.day, t.hour, t.min, t.sec);
}

bool IsForexSymbol(const string symbol)
{
   long calc_mode = -1;
   if(!SymbolInfoInteger(symbol, SYMBOL_TRADE_CALC_MODE, calc_mode))
      return false;
   return (calc_mode == SYMBOL_CALC_MODE_FOREX ||
           calc_mode == SYMBOL_CALC_MODE_FOREX_NO_LEVERAGE);
}

bool IsNewBarForKey(const string key, const datetime bar_time)
{
   int n = ArraySize(g_seen_keys);
   for(int i = 0; i < n; i++)
      if(g_seen_keys[i] == key)
         return (g_seen_bar_times[i] != bar_time);
   return true;
}

void MarkBarWritten(const string key, const datetime bar_time)
{
   int n = ArraySize(g_seen_keys);
   for(int i = 0; i < n; i++)
   {
      if(g_seen_keys[i] == key)
      {
         g_seen_bar_times[i] = bar_time;
         return;
      }
   }
   ArrayResize(g_seen_keys, n + 1);
   ArrayResize(g_seen_bar_times, n + 1);
   g_seen_keys[n] = key;
   g_seen_bar_times[n] = bar_time;
}

void AppendClosedBar(const string symbol, const ENUM_TIMEFRAMES tf, const string tf_name)
{
   MqlRates rates[];
   ArraySetAsSeries(rates, true);
   if(CopyRates(symbol, tf, 1, 1, rates) != 1)
      return;

   string key = symbol + "|" + tf_name;
   if(!IsNewBarForKey(key, rates[0].time))
      return;

   datetime server_estimate = TimeTradeServer();
   datetime server_last_quote = TimeCurrent();
   datetime host_gmt_estimate = TimeGMT();
   datetime host_local_observed = TimeLocal();
   if(server_estimate <= 0 || server_last_quote <= 0 || host_gmt_estimate <= 0)
   {
      Print("Raw capture: clock observation unavailable; retrying next timer.");
      return;
   }

   string broker_server = AccountInfoString(ACCOUNT_SERVER);
   string terminal_name = TerminalInfoString(TERMINAL_NAME);
   string source_id = terminal_name + "|" + TerminalInfoString(TERMINAL_PATH);

   string volume_type = "UNAVAILABLE";
   if(rates[0].tick_volume > 0 && rates[0].real_volume > 0)
      volume_type = "BOTH";
   else if(rates[0].tick_volume > 0)
      volume_type = "TICK";
   else if(rates[0].real_volume > 0)
      volume_type = "REAL";

   int file = FileOpen(OutputFileName,
                       FILE_READ|FILE_WRITE|FILE_CSV|FILE_SHARE_READ|FILE_COMMON|FILE_ANSI,
                       ',');
   if(file == INVALID_HANDLE)
   {
      Print("Raw capture: FileOpen failed. Error=", GetLastError());
      return;
   }

   bool write_header = (FileSize(file) == 0);
   FileSeek(file, 0, SEEK_END);
   if(write_header)
   {
      FileWrite(file, "symbol", "timeframe", "bar_time_mt5_utc",
                "terminal_time_server", "terminal_time_current_server",
                "host_gmt_estimate_utc", "host_local_time_observed",
                "broker_server_id", "source_id", "capture_version",
                "is_closed", "open", "high", "low", "close",
                "tick_volume", "real_volume", "spread_points", "volume_type",
                "observed_server_minus_host_gmt_seconds");
   }

   long observed_offset = (long)server_estimate - (long)host_gmt_estimate;
   uint bytes_written = FileWrite(file,
      symbol, tf_name,
      IsoUtc(rates[0].time),
      TimeToString(server_estimate, TIME_DATE|TIME_SECONDS),
      TimeToString(server_last_quote, TIME_DATE|TIME_SECONDS),
      IsoUtc(host_gmt_estimate),
      TimeToString(host_local_observed, TIME_DATE|TIME_SECONDS),
      broker_server, source_id, "1.2.0",
      "true",
      DoubleToString(rates[0].open, 10),
      DoubleToString(rates[0].high, 10),
      DoubleToString(rates[0].low, 10),
      DoubleToString(rates[0].close, 10),
      (long)rates[0].tick_volume,
      (long)rates[0].real_volume,
      (int)rates[0].spread,
      volume_type,
      observed_offset
   );
   FileFlush(file);
   FileClose(file);
   if(bytes_written == 0)
   {
      Print("Raw capture: row write failed; bar will be retried.");
      return;
   }
   MarkBarWritten(key, rates[0].time);
}

void CaptureMarketWatch()
{
   int total = SymbolsTotal(true);
   for(int s = 0; s < total; s++)
   {
      string symbol = SymbolName(s, true);
      if(symbol == "")
         continue;
      if(CaptureForexOnly && !IsForexSymbol(symbol))
         continue;
      for(int t = 0; t < ArraySize(g_timeframes); t++)
         AppendClosedBar(symbol, g_timeframes[t], g_tf_names[t]);
   }
}

int OnInit()
{
   if(CaptureIntervalSeconds < 2)
   {
      Print("Raw capture: interval must be at least 2 seconds.");
      return INIT_PARAMETERS_INCORRECT;
   }
   EventSetTimer(CaptureIntervalSeconds);
   Print("MT5 Forex-Only Raw Capture V1.1 started. ForexOnly=",
         CaptureForexOnly, ". Data export only; trading is not implemented.");
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   EventKillTimer();
}

void OnTimer()
{
   CaptureMarketWatch();
}
//+------------------------------------------------------------------+
