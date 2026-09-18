//+------------------------------------------------------------------+
//| Decision Brain V1 - MT5 Display Bridge                           |
//| Uses the existing Python Decision Brain; orders are disabled.    |
//+------------------------------------------------------------------+
#property strict
#property indicator_chart_window
#property indicator_plots 0

input string BridgeURL = "http://127.0.0.1:8765/assess";
input int RefreshSeconds = 5;
input int WebRequestTimeoutMs = 1500;

ENUM_TIMEFRAMES TFs[6] = {PERIOD_M5, PERIOD_M15, PERIOD_M30, PERIOD_H1, PERIOD_H4, PERIOD_D1};
string TFNames[6] = {"M5","M15","M30","H1","H4","D1"};

datetime last_refresh = 0;
string last_status = "Starting...";
string last_state = "";
string last_bias = "";
double last_conf = 0.0;
string last_reasons = "";

string JsonEscape(string s)
{
   StringReplace(s, "\\", "\\\\");
   StringReplace(s, """, "\\"");
   return s;
}

double Clamp01(double x)
{
   if(x < 0.0) return 0.0;
   if(x > 1.0) return 1.0;
   return x;
}

double Regime(ENUM_TIMEFRAMES tf)
{
   int h50 = iMA(_Symbol, tf, 50, 0, MODE_EMA, PRICE_CLOSE);
   int h200 = iMA(_Symbol, tf, 200, 0, MODE_EMA, PRICE_CLOSE);
   if(h50 == INVALID_HANDLE || h200 == INVALID_HANDLE)
      return 0.0;

   double a50[3], a200[3], cls[3];
   ArraySetAsSeries(a50, true);
   ArraySetAsSeries(a200, true);
   ArraySetAsSeries(cls, true);

   if(CopyBuffer(h50, 0, 0, 3, a50) < 3 ||
      CopyBuffer(h200, 0, 0, 3, a200) < 3 ||
      CopyClose(_Symbol, tf, 0, 3, cls) < 3)
   {
      IndicatorRelease(h50);
      IndicatorRelease(h200);
      return 0.0;
   }

   double slope = a50[0] - a50[1];
   double scale = MathMax(a50[0] * 0.0001, _Point * 10.0);
   double s = 0.0;
   if(a50[0] > a200[0] && slope > 0.0 && cls[0] > a50[0])
      s = 1.0;
   else if(a50[0] < a200[0] && slope < 0.0 && cls[0] < a50[0])
      s = -1.0;
   else
      s = (a50[0] > a200[0] ? 0.25 : (a50[0] < a200[0] ? -0.25 : 0.0));

   IndicatorRelease(h50);
   IndicatorRelease(h200);
   return Clamp01(MathAbs(s)) * (s >= 0.0 ? 1.0 : -1.0);
}

double MTFScore(double &regs[])
{
   double sum = 0.0;
   for(int i=0;i<ArraySize(regs);i++) sum += regs[i];
   return sum / ArraySize(regs);
}

string BuildJSON()
{
   double regs[6];
   string json = "{";
   json += ""mtf_trend_score":";
   for(int i=0;i<6;i++) regs[i] = Regime(TFs[i]);
   json += DoubleToString(MTFScore(regs), 6);

   for(int i=0;i<6;i++)
   {
      json += ","" + TFNames[i] + "_trend_regime":" + DoubleToString(regs[i], 6);
   }

   // Tick volume is intentionally not promoted to governed volume evidence.
   // The existing Brain therefore reports volume as unavailable.
   json += ","volume_available":false";
   json += ","symbol":"" + JsonEscape(_Symbol) + """;
   json += ","timeframe":"" + IntegerToString(PeriodSeconds(_Period)/60) + "m"";
   json += "}";
   return json;
}

string ExtractString(string json, string key)
{
   string needle = """ + key + "":"";
   int p = StringFind(json, needle);
   if(p < 0) return "";
   p += StringLen(needle);
   int e = StringFind(json, """, p);
   if(e < 0) return "";
   return StringSubstr(json, p, e-p);
}

double ExtractNumber(string json, string key)
{
   string needle = """ + key + "":";
   int p = StringFind(json, needle);
   if(p < 0) return 0.0;
   p += StringLen(needle);
   int e = p;
   while(e < StringLen(json))
   {
      ushort c = StringGetCharacter(json, e);
      if((c >= '0' && c <= '9') || c == '-' || c == '+' || c == '.' || c == 'e' || c == 'E')
         e++;
      else
         break;
   }
   return StringToDouble(StringSubstr(json, p, e-p));
}

void DrawPanel(string text)
{
   Comment(text);
}

void RequestAssessment()
{
   string payload = BuildJSON();
   char data[];
   char result[];
   string headers = "Content-Type: application/json\r\n";
   int n = StringToCharArray(payload, data, 0, WHOLE_ARRAY, CP_UTF8);
   if(n > 0) ArrayResize(data, n-1);

   string result_headers;
   ResetLastError();
   int code = WebRequest("POST", BridgeURL, headers, WebRequestTimeoutMs, data, result, result_headers);

   if(code != 200)
   {
      int err = GetLastError();
      last_status = "Bridge error HTTP=" + IntegerToString(code) + " err=" + IntegerToString(err);
      DrawPanel("DECISION BRAIN V1\n\n" + last_status +
                "\n\nStart the local Python bridge.\nOrders: DISABLED");
      return;
   }

   string body = CharArrayToString(result, 0, -1, CP_UTF8);
   if(StringFind(body, ""error"") >= 0)
   {
      last_status = "Bridge returned an error";
      DrawPanel("DECISION BRAIN V1\n\n" + body);
      return;
   }

   last_state = ExtractString(body, "market_state");
   last_bias = ExtractString(body, "directional_bias");
   last_conf = ExtractNumber(body, "confidence");

   string reasons = "";
   if(StringFind(body, "no_trade_reasons") >= 0)
      reasons = "See Brain response / volume gate.";
   last_reasons = reasons;
   last_status = "LIVE • " + TimeToString(TimeCurrent(), TIME_SECONDS);

   string panel =
      "DECISION BRAIN V1\n" +
      "-------------------------\n" +
      "Symbol: " + _Symbol + "\n" +
      "Market: " + last_state + "\n" +
      "Bias:   " + last_bias + "\n" +
      "Confidence: " + DoubleToString(last_conf*100.0, 1) + "%\n" +
      "-------------------------\n" +
      "Analysis source: existing Brain V1\n" +
      "Orders: DISABLED\n" +
      "Volume gate: unavailable\n" +
      "-------------------------\n" +
      last_status;

   DrawPanel(panel);
}

int OnInit()
{
   EventSetTimer(MathMax(1, RefreshSeconds));
   RequestAssessment();
   return(INIT_SUCCEEDED);
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   Comment("");
}

void OnTimer()
{
   RequestAssessment();
}

int OnCalculate(const int rates_total,
                const int prev_calculated,
                const datetime &time[],
                const double &open[],
                const double &high[],
                const double &low[],
                const double &close[],
                const long &tick_volume[],
                const long &volume[],
                const int &spread[])
{
   return(rates_total);
}
