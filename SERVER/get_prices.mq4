//+------------------------------------------------------------------+
//|                                                   get_prices.mq4 |
//|                        Copyright 2019, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2019, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property strict
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- create timer
   EventSetTimer(1);
   
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//--- destroy timer
   EventKillTimer();
   
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//---
   
  }
//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+
void OnTimer()
  {
//---
   write_in_file();
  }
//+------------------------------------------------------------------+


void write_in_file(){
   int i; 
   int file;
   
   i = 0;
   while (i < 1000)
      {
         file = FileOpen("symbol_prices.txt",FILE_TXT|FILE_WRITE,","); 
         i += 1;
         if (file != INVALID_HANDLE)
            {            
            // This is the part that you can need to change only 
              
              
               FileWrite(file,"EURUSD",iHigh("EURUSD",PERIOD_M1,0),iLow("EURUSD",PERIOD_M1,0),iClose("EURUSD",PERIOD_M1,0));
               FileWrite(file,"XAUUSD",iHigh("XAUUSD",PERIOD_M1,0),iLow("XAUUSD",PERIOD_M1,0),iClose("XAUUSD",PERIOD_M1,0));
            
            
            /////////////////////////////////////////////////////
               FileClose(file); 
               break;
            }
      }
   
}