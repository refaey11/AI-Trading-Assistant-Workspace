//+------------------------------------------------------------------+
//| D0 Read-Only CopyRates Range Diagnostic                          |
//| Test-only script. Demo accounts only. No trade operations.       |
//+------------------------------------------------------------------+
#property strict
#property version   "1.00"
#property script_show_inputs
#property description "Read-only D0 diagnostic: repeats one bounded CopyRates range and exports evidence."

input ENUM_TIMEFRAMES InpTimeframe = PERIOD_M5;
input datetime InpRangeFrom = D'2026.11.02 00:00';
input datetime InpRangeTo   = D'2026.11.03 00:00';
input bool InpArrayAsSeries = true;

bool SameBar(const MqlRates &a, const MqlRates &b)
{
   return (a.time == b.time &&
           a.open == b.open &&
           a.high == b.high &&
           a.low == b.low &&
           a.close == b.close &&
           a.tick_volume == b.tick_volume &&
           a.spread == b.spread &&
           a.real_volume == b.real_volume);
}

int PhysicalIndex(const int physical_pos, const int count, const bool as_series)
{
   if(as_series)
      return count - 1 - physical_pos;
   return physical_pos;
}

string SafeStamp()
{
   string s = TimeToString(TimeLocal(), TIME_DATE | TIME_SECONDS);
   StringReplace(s, ".", "");
   StringReplace(s, ":", "");
   StringReplace(s, " ", "_");
   return s + "_" + IntegerToString((int)GetTickCount());
}

void OnStart()
{
   // Hard safety boundary: this diagnostic refuses non-Demo accounts.
   ENUM_ACCOUNT_TRADE_MODE mode =
      (ENUM_ACCOUNT_TRADE_MODE)AccountInfoInteger(ACCOUNT_TRADE_MODE);
   if(mode != ACCOUNT_TRADE_MODE_DEMO)
   {
      Print("D0 diagnostic refused: Demo account required. No data captured.");
      return;
   }

   if(InpRangeFrom <= 0 || InpRangeTo <= InpRangeFrom)
   {
      Print("D0 diagnostic refused: invalid bounded date range.");
      return;
   }

   if(!TerminalInfoInteger(TERMINAL_CONNECTED))
   {
      Print("D0 diagnostic refused: terminal is not connected.");
      return;
   }

   long synchronized = 0;
   bool sync_query_ok = SeriesInfoInteger(_Symbol, InpTimeframe,
                                           SERIES_SYNCHRONIZED, synchronized);
   int expected_count = Bars(_Symbol, InpTimeframe, InpRangeFrom, InpRangeTo);
   int period_seconds = PeriodSeconds(InpTimeframe);
   datetime server_now = TimeTradeServer();
   if(server_now <= 0)
      server_now = TimeCurrent();

   MqlRates rates_a[];
   MqlRates rates_b[];
   bool set_a = ArraySetAsSeries(rates_a, InpArrayAsSeries);
   bool set_b = ArraySetAsSeries(rates_b, InpArrayAsSeries);

   ResetLastError();
   int copied_a = CopyRates(_Symbol, InpTimeframe, InpRangeFrom, InpRangeTo, rates_a);
   int error_a = GetLastError();

   ResetLastError();
   int copied_b = CopyRates(_Symbol, InpTimeframe, InpRangeFrom, InpRangeTo, rates_b);
   int error_b = GetLastError();

   bool series_a = ArrayGetAsSeries(rates_a);
   bool series_b = ArrayGetAsSeries(rates_b);

   bool arrays_equal = (copied_a > 0 && copied_a == copied_b);
   bool strictly_increasing = true;
   bool all_closed = (period_seconds > 0 && server_now > 0);
   int mismatches = 0;
   int duplicate_or_order_errors = 0;
   int unclosed_bars = 0;

   if(copied_a > 0)
   {
      for(int p = 0; p < copied_a; p++)
      {
         int ia = PhysicalIndex(p, copied_a, series_a);
         if(rates_a[ia].time + period_seconds > server_now)
         {
            all_closed = false;
            unclosed_bars++;
         }
         if(p > 0)
         {
            int prev = PhysicalIndex(p - 1, copied_a, series_a);
            if(rates_a[ia].time <= rates_a[prev].time)
            {
               strictly_increasing = false;
               duplicate_or_order_errors++;
            }
         }
      }
   }

   if(arrays_equal)
   {
      for(int p = 0; p < copied_a; p++)
      {
         int ia = PhysicalIndex(p, copied_a, series_a);
         int ib = PhysicalIndex(p, copied_b, series_b);
         if(!SameBar(rates_a[ia], rates_b[ib]))
         {
            arrays_equal = false;
            mismatches++;
         }
      }
   }
   else
   {
      mismatches = -1; // Counts differ or no complete first response.
   }

   bool sync_ready = (sync_query_ok && synchronized != 0);
   bool full_counts = (expected_count > 0 &&
                       copied_a == expected_count &&
                       copied_b == expected_count);
   string result = "INCONCLUSIVE";
   if(full_counts && arrays_equal && strictly_increasing && all_closed && sync_ready)
      result = "PASS";
   else if(full_counts && (!arrays_equal || !strictly_increasing || !all_closed))
      result = "FAIL";

   string run_id = SafeStamp();
   string file_name = "D0_ReadOnly_" + run_id + ".csv";
   int handle = FileOpen(file_name, FILE_WRITE | FILE_CSV | FILE_ANSI, ',');
   if(handle == INVALID_HANDLE)
   {
      PrintFormat("D0 evidence file could not be opened. Error=%d", GetLastError());
      return;
   }

   FileWrite(handle, "record_type", "run_id", "symbol", "timeframe",
             "range_from_raw", "range_to_raw", "expected_count",
             "copied_a", "error_a", "copied_b", "error_b",
             "sync_query_ok", "series_synchronized",
             "array_set_a_ok", "array_set_b_ok", "array_as_series_a",
             "array_as_series_b", "server_time_observed",
             "period_seconds", "all_bars_closed", "unclosed_bars",
             "physical_time_strictly_increasing", "arrays_equal",
             "mismatches", "duplicate_or_order_errors", "result");
   FileWrite(handle, "META", run_id, _Symbol, EnumToString(InpTimeframe),
             (long)InpRangeFrom, (long)InpRangeTo, expected_count,
             copied_a, error_a, copied_b, error_b,
             (int)sync_query_ok, synchronized,
             (int)set_a, (int)set_b, (int)series_a, (int)series_b,
             (long)server_now, period_seconds, (int)all_closed, unclosed_bars,
             (int)strictly_increasing, (int)arrays_equal, mismatches,
             duplicate_or_order_errors, result);

   FileWrite(handle, "dataset", "physical_position", "bar_time_raw",
             "open", "high", "low", "close", "tick_volume", "spread", "real_volume");

   for(int p = 0; p < copied_a; p++)
   {
      int i = PhysicalIndex(p, copied_a, series_a);
      FileWrite(handle, "A", p, (long)rates_a[i].time,
                DoubleToString(rates_a[i].open, _Digits),
                DoubleToString(rates_a[i].high, _Digits),
                DoubleToString(rates_a[i].low, _Digits),
                DoubleToString(rates_a[i].close, _Digits),
                (long)rates_a[i].tick_volume, rates_a[i].spread,
                (long)rates_a[i].real_volume);
   }

   for(int p = 0; p < copied_b; p++)
   {
      int i = PhysicalIndex(p, copied_b, series_b);
      FileWrite(handle, "B", p, (long)rates_b[i].time,
                DoubleToString(rates_b[i].open, _Digits),
                DoubleToString(rates_b[i].high, _Digits),
                DoubleToString(rates_b[i].low, _Digits),
                DoubleToString(rates_b[i].close, _Digits),
                (long)rates_b[i].tick_volume, rates_b[i].spread,
                (long)rates_b[i].real_volume);
   }

   FileFlush(handle);
   FileClose(handle);

   PrintFormat("D0 diagnostic finished. Result=%s; evidence=%s; A=%d/%d; B=%d/%d; mismatch=%d",
               result, file_name, copied_a, expected_count,
               copied_b, expected_count, mismatches);
   Print("Evidence is in this terminal's MQL5/Files folder (not FILE_COMMON).");
   Print("This script does not place, modify, or close orders and does not modify the capture EA.");
}
