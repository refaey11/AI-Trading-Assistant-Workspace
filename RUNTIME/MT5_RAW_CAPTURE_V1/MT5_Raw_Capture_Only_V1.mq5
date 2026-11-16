//+------------------------------------------------------------------+
//| MT5 Raw Capture Only V1                                          |
//| Data export only: NO trade requests, NO indicators, NO signals.  |
//+------------------------------------------------------------------+
#property strict
#property version   "1.10"
#property description "Exports last closed Market Watch bars only. Never trades."

input int    CaptureIntervalSeconds = 10;
input string OutputFileName = "mt5_raw_capture_v1.csv";

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

bool IsNewBarForKey(const string key, const datetime bar_time)
{
   int n = ArraySize(g_seen_keys);
   for(int i = 0; i < n; i++)
   {
      if(g_seen_keys[i] == key)
      {
         if(g_seen_bar_times[i] == bar_time)
            return false;
         g_seen_bar_times[i] = bar_time;
         return true;
      }
   }
   ArrayResize(g_seen_keys, n + 1);
   ArrayResize(g_seen_bar_times, n + 1);
   g_seen_keys[n] = key;
   g_seen_bar_times[n] = bar_time;
   return true;
}

void AppendClosedBar(const string symbol, const ENUM_TIMEFRAMES tf, const string tf_name)
{
   MqlRates rates[];
   ArraySetAsSeries(rates, true);
   // Shift 1 means the most recent fully closed bar, never the forming bar.
   if(CopyRates(symbol, tf, 1, 1, rates) != 1)
      return;

   string key = symbol + "|" + tf_name;
   if(!IsNewBarForKey(key, rates[0].time))
      return;

   datetime server_now = TimeTradeServer();
   datetime gmt_observed = TimeGMT();
   datetime local_now = TimeLocal();
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
      FileWrite(file, "symbol", "timeframe", "bar_time_server",
                "terminal_time_server", "terminal_gmt_observed_utc",
                "terminal_local_time_observed", "capture_time_utc",
                "broker_server_id", "source_id", "capture_version",
                "is_closed", "open", "high", "low", "close",
                "tick_volume", "real_volume", "spread_points", "volume_type",
                "observed_server_minus_gmt_seconds");
   }

   long observed_offset = (long)server_now - (long)gmt_observed;
   FileWrite(file,
      symbol, tf_name,
      TimeToString(rates[0].time, TIME_DATE|TIME_SECONDS),
      TimeToString(server_now, TIME_DATE|TIME_SECONDS),
      IsoUtc(gmt_observed),
      TimeToString(local_now, TIME_DATE|TIME_SECONDS),
      IsoUtc(gmt_observed),
      broker_server, source_id, "1.1.0",
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
}

void CaptureMarketWatch()
{
   int total = SymbolsTotal(true);
   for(int s = 0; s < total; s++)
   {
      string symbol = SymbolName(s, true);
      if(symbol == "")
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
   Print("MT5 Raw Capture Only V1 started. Data export only; trading is not implemented.");
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
