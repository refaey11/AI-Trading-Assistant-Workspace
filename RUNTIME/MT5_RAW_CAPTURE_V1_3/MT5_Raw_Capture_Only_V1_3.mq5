//+------------------------------------------------------------------+
//| MT5 Raw Capture Only V1.3                                        |
//| Data export only. No trade requests, indicators, or signals.     |
//+------------------------------------------------------------------+
#property strict
#property version   "1.30"
#property description "Exports closed MT5 bars with raw clock provenance only."
input int CaptureIntervalSeconds = 10;
input string OutputFileName = "mt5_raw_capture_v1_3.csv";
ENUM_TIMEFRAMES g_timeframes[] = {PERIOD_M5, PERIOD_M15, PERIOD_M30, PERIOD_H1, PERIOD_H4, PERIOD_D1};
string g_tf_names[] = {"M5", "M15", "M30", "H1", "H4", "D1"};
string g_seen_keys[];
datetime g_seen_bar_times[];

bool IsNewBarForKey(const string key, const datetime bar_time)
{
   for(int i = 0; i < ArraySize(g_seen_keys); i++)
      if(g_seen_keys[i] == key)
         return (g_seen_bar_times[i] != bar_time);
   return true;
}
void MarkBarWritten(const string key, const datetime bar_time)
{
   int n = ArraySize(g_seen_keys);
   for(int i = 0; i < n; i++)
      if(g_seen_keys[i] == key) { g_seen_bar_times[i] = bar_time; return; }
   ArrayResize(g_seen_keys, n + 1);
   ArrayResize(g_seen_bar_times, n + 1);
   g_seen_keys[n] = key;
   g_seen_bar_times[n] = bar_time;
}
void AppendClosedBar(const string symbol, const ENUM_TIMEFRAMES tf, const string tf_name)
{
   MqlRates rates[];
   ArraySetAsSeries(rates, true);
   if(CopyRates(symbol, tf, 1, 1, rates) != 1) return;
   string key = symbol + "|" + tf_name;
   if(!IsNewBarForKey(key, rates[0].time)) return;

   datetime server_estimate = TimeTradeServer();
   datetime server_last_quote = TimeCurrent();
   datetime host_gmt_estimate = TimeGMT();
   datetime host_local_observed = TimeLocal();
   if(server_estimate <= 0 || server_last_quote <= 0 || host_gmt_estimate <= 0)
   {
      Print("Raw capture V1.3: clock observation unavailable; retrying.");
      return;
   }
   string broker_server = AccountInfoString(ACCOUNT_SERVER);
   string source_id = TerminalInfoString(TERMINAL_NAME) + "|" + TerminalInfoString(TERMINAL_PATH);
   string volume_type = "UNAVAILABLE";
   if(rates[0].tick_volume > 0 && rates[0].real_volume > 0) volume_type = "BOTH";
   else if(rates[0].tick_volume > 0) volume_type = "TICK";
   else if(rates[0].real_volume > 0) volume_type = "REAL";

   int file = FileOpen(OutputFileName, FILE_READ|FILE_WRITE|FILE_CSV|FILE_SHARE_READ|FILE_COMMON|FILE_ANSI, ',');
   if(file == INVALID_HANDLE) { Print("Raw capture V1.3: FileOpen failed. Error=", GetLastError()); return; }
   bool write_header = (FileSize(file) == 0);
   FileSeek(file, 0, SEEK_END);
   if(write_header)
      FileWrite(file, "symbol", "timeframe", "bar_time_epoch_seconds_raw",
                "bar_time_source_clock", "bar_time_utc_status",
                "terminal_time_server_observed", "terminal_time_current_server_observed",
                "host_gmt_estimate_observed", "host_local_time_observed",
                "broker_server_id", "source_id", "capture_version", "is_closed",
                "open", "high", "low", "close", "tick_volume", "real_volume",
                "spread_points", "volume_type", "observed_server_minus_host_gmt_seconds");

   // Preserve MqlRates.time as raw epoch seconds. No UTC suffix or conversion.
   long observed_offset_diagnostic = (long)server_estimate - (long)host_gmt_estimate;
   uint bytes_written = FileWrite(file, symbol, tf_name, (long)rates[0].time,
      "MT5_MQLRATES_DATETIME_RAW", "UNVERIFIED",
      TimeToString(server_estimate, TIME_DATE|TIME_SECONDS),
      TimeToString(server_last_quote, TIME_DATE|TIME_SECONDS),
      TimeToString(host_gmt_estimate, TIME_DATE|TIME_SECONDS),
      TimeToString(host_local_observed, TIME_DATE|TIME_SECONDS),
      broker_server, source_id, "1.3.0", "true",
      DoubleToString(rates[0].open, 10), DoubleToString(rates[0].high, 10),
      DoubleToString(rates[0].low, 10), DoubleToString(rates[0].close, 10),
      (long)rates[0].tick_volume, (long)rates[0].real_volume,
      (int)rates[0].spread, volume_type, observed_offset_diagnostic);
   FileFlush(file);
   FileClose(file);
   if(bytes_written == 0) { Print("Raw capture V1.3: row write failed; bar will be retried."); return; }
   MarkBarWritten(key, rates[0].time);
}
void CaptureMarketWatch()
{
   int total = SymbolsTotal(true);
   for(int s = 0; s < total; s++)
   {
      string symbol = SymbolName(s, true);
      if(symbol == "") continue;
      for(int t = 0; t < ArraySize(g_timeframes); t++)
         AppendClosedBar(symbol, g_timeframes[t], g_tf_names[t]);
   }
}
int OnInit()
{
   if(CaptureIntervalSeconds < 2) return INIT_PARAMETERS_INCORRECT;
   EventSetTimer(CaptureIntervalSeconds);
   Print("MT5 Raw Capture Only V1.3 started. Raw capture only; no trading.");
   return INIT_SUCCEEDED;
}
void OnDeinit(const int reason) { EventKillTimer(); }
void OnTimer() { CaptureMarketWatch(); }
//+------------------------------------------------------------------+
