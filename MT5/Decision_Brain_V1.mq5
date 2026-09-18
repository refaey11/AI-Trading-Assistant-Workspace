//+------------------------------------------------------------------+
//| Decision Brain V1 - MT5 Display Bridge                           |
//| Existing Python Brain V1; display/analysis only; no orders.      |
//+------------------------------------------------------------------+
#property strict
#property indicator_chart_window
#property indicator_plots 0

input string BridgeURL = "http://127.0.0.1:8765/assess";
input int RefreshSeconds = 5;
input int WebRequestTimeoutMs = 1500;

ENUM_TIMEFRAMES TFs[6] = {PERIOD_M5,PERIOD_M15,PERIOD_M30,PERIOD_H1,PERIOD_H4,PERIOD_D1};
string TFNames[6] = {"M5","M15","M30","H1","H4","D1"};

double ClampSigned(double x)
{
   if(x > 1.0) return 1.0;
   if(x < -1.0) return -1.0;
   return x;
}

double GetRegime(ENUM_TIMEFRAMES tf)
{
   int h50=iMA(_Symbol,tf,50,0,MODE_EMA,PRICE_CLOSE);
   int h200=iMA(_Symbol,tf,200,0,MODE_EMA,PRICE_CLOSE);
   if(h50==INVALID_HANDLE || h200==INVALID_HANDLE)
   {
      if(h50!=INVALID_HANDLE) IndicatorRelease(h50);
      if(h200!=INVALID_HANDLE) IndicatorRelease(h200);
      return 0.0;
   }

   double ema50[2],ema200[2],cls[2];
   ArraySetAsSeries(ema50,true);
   ArraySetAsSeries(ema200,true);
   ArraySetAsSeries(cls,true);

   int ok1=CopyBuffer(h50,0,0,2,ema50);
   int ok2=CopyBuffer(h200,0,0,2,ema200);
   int ok3=CopyClose(_Symbol,tf,0,2,cls);
   IndicatorRelease(h50);
   IndicatorRelease(h200);

   if(ok1<2 || ok2<2 || ok3<2) return 0.0;

   double slope=ema50[0]-ema50[1];
   if(ema50[0]>ema200[0] && slope>0.0 && cls[0]>ema50[0]) return 1.0;
   if(ema50[0]<ema200[0] && slope<0.0 && cls[0]<ema50[0]) return -1.0;
   if(ema50[0]>ema200[0]) return 0.25;
   if(ema50[0]<ema200[0]) return -0.25;
   return 0.0;
}

string BuildPayload()
{
   double r[6];
   double sum=0.0;
   for(int i=0;i<6;i++)
   {
      r[i]=GetRegime(TFs[i]);
      sum+=r[i];
   }

   string j="{";
   j += "\"mtf_trend_score\":"+DoubleToString(ClampSigned(sum/6.0),6);

   for(int i=0;i<6;i++)
      j += ",\""+TFNames[i]+"_trend_regime\":"+DoubleToString(r[i],6);

   // The current Brain only treats source-backed volume as governed evidence.
   j += ",\"volume_available\":false";
   j += "}";
   return j;
}

string JsonString(string body,string key)
{
   string needle="\""+key+"\":\"";
   int p=StringFind(body,needle);
   if(p<0) return "";
   p+=StringLen(needle);
   int e=StringFind(body,"\"",p);
   if(e<0) return "";
   return StringSubstr(body,p,e-p);
}

double JsonNumber(string body,string key)
{
   string needle="\""+key+"\":";
   int p=StringFind(body,needle);
   if(p<0) return 0.0;
   p+=StringLen(needle);
   int e=p;
   while(e<StringLen(body))
   {
      ushort c=StringGetCharacter(body,e);
      if((c>='0' && c<='9') || c=='-' || c=='+' || c=='.' || c=='e' || c=='E')
         e++;
      else
         break;
   }
   return StringToDouble(StringSubstr(body,p,e-p));
}

void Show(string s)
{
   Comment(s);
}

void RequestBrain()
{
   string payload=BuildPayload();
   char post[];
   char result[];
   string response_headers;
   string headers="Content-Type: application/json\r\n";

   int n=StringToCharArray(payload,post,0,WHOLE_ARRAY,CP_UTF8);
   if(n>0) ArrayResize(post,n-1);

   ResetLastError();
   int code=WebRequest("POST",BridgeURL,headers,WebRequestTimeoutMs,post,result,response_headers);

   if(code!=200)
   {
      int err=GetLastError();
      Show("DECISION BRAIN V1\n\nBridge not reachable.\nHTTP: "+
           IntegerToString(code)+"  Error: "+IntegerToString(err)+
           "\n\nStart the Python bridge and allow WebRequest.");
      return;
   }

   string body=CharArrayToString(result,0,-1,CP_UTF8);
   string state=JsonString(body,"market_state");
   string bias=JsonString(body,"directional_bias");
   double conf=JsonNumber(body,"confidence");

   Show("DECISION BRAIN V1\n"+
        "-------------------------\n"+
        "Symbol: "+_Symbol+"\n"+
        "Market: "+state+"\n"+
        "Bias: "+bias+"\n"+
        "Confidence: "+DoubleToString(conf*100.0,1)+"%\n"+
        "-------------------------\n"+
        "Source: existing Brain V1\n"+
        "Orders: DISABLED\n"+
        "Volume: unavailable\n"+
        "-------------------------\n"+
        "LIVE: "+TimeToString(TimeCurrent(),TIME_SECONDS));
}

int OnInit()
{
   EventSetTimer(MathMax(1,RefreshSeconds));
   RequestBrain();
   return(INIT_SUCCEEDED);
}

void OnDeinit(const int reason)
{
   EventKillTimer();
   Comment("");
}

void OnTimer()
{
   RequestBrain();
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
   return rates_total;
}
