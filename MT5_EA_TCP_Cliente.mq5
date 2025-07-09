#property strict

input string ServerIP = "127.0.0.1";
input ushort ServerPort = 5555;

int sock = -1;
datetime ultimoCandle = 0;

// Envia o candle atual como JSON para o servidor
void EnviarSinal()
{
   MqlRates rates[];
   if (CopyRates(Symbol(), PERIOD_CURRENT, 0, 1, rates) <= 0)
   {
      Print("❌ Erro ao obter candle.");
      return;
   }

   string json = StringFormat(
      "{\"ativo\":\"%s\",\"open\":%.2f,\"high\":%.2f,\"low\":%.2f,\"close\":%.2f,\"volume\":%d}",
      Symbol(),
      rates[0].open,
      rates[0].high,
      rates[0].low,
      rates[0].close,
      (int)rates[0].tick_volume
   );

   uchar data[];
   StringToCharArray(json + "\n", data);
   int sent = SocketSend(sock, data, ArraySize(data) - 1);
   if (sent <= 0)
   {
      Print("⚠️ Erro ao enviar sinal. Recriando conexão...");
      SocketClose(sock);
      sock = -1;
      sock = SocketCreate();
      if (sock != INVALID_HANDLE && SocketConnect(sock, ServerIP, ServerPort, 0))
         Print("🔄 Reconectado ao servidor.");
   }
   else
   {
      Print("📤 Sinal enviado:", json);
   }
}

// Recebe e interpreta a resposta do servidor
void ReceberSinal()
{
   uchar data[1024];
   int received = SocketRead(sock, data, sizeof(data), 0);
   if (received > 0)
   {
      string msg = CharArrayToString(data, 0, received);
      Print("📥 Sinal recebido: ", msg);

      string ativo = "", sinal = "";

      int posAtivo = StringFind(msg, "\"ativo\":\"");
      if (posAtivo != -1)
      {
         int ini = posAtivo + 9;
         int fim = StringFind(msg, "\"", ini);
         ativo = StringSubstr(msg, ini, fim - ini);
      }

      int posSinal = StringFind(msg, "\"sinal\":\"");
      if (posSinal != -1)
      {
         int ini = posSinal + 9;
         int fim = StringFind(msg, "\"", ini);
         sinal = StringSubstr(msg, ini, fim - ini);
      }

      if (ativo == Symbol() && (sinal == "compra" || sinal == "venda"))
      {
         ExecutarOrdem(sinal);
      }
      else
      {
         Print("⚠️ Sinal não corresponde ao ativo atual. Sinal:", sinal, ", Ativo no sinal:", ativo);
      }
   }
   else
   {
      Print("❌ Erro ao receber dados. Reconectando...");
      SocketClose(sock);
      sock = -1;
      sock = SocketCreate();
      if (sock != INVALID_HANDLE && SocketConnect(sock, ServerIP, ServerPort, 0))
         Print("🔄 Reconectado ao servidor.");
   }
}

// Executa uma ordem com base no sinal
void ExecutarOrdem(string sinal)
{
   double preco;
   if (!SymbolInfoDouble(Symbol(), SYMBOL_ASK, preco))
   {
      Print("❌ Erro ao obter preço.");
      return;
   }

   MqlTradeRequest request = {};
   MqlTradeResult result = {};

   request.symbol = Symbol();
   request.volume = 0.1;
   request.price = preco;
   request.deviation = 2;
   request.type = (sinal == "compra") ? ORDER_TYPE_BUY : ORDER_TYPE_SELL;
   request.action = TRADE_ACTION_DEAL;
   request.comment = "Ordem automática";
   request.type_filling = ORDER_FILLING_IOC;

   if (!OrderSend(request, result))
   {
      Print("❌ Erro ao enviar ordem: ", GetLastError());
   }
   else
   {
      Print("✅ Ordem de ", sinal, " executada. Ticket: ", result.order);
   }
}

int OnInit()
{
   sock = SocketCreate();
   if (sock == INVALID_HANDLE)
   {
      Print("❌ Erro ao criar socket");
      return INIT_FAILED;
   }

   if (!SocketConnect(sock, ServerIP, ServerPort, 0))
   {
      int erro = GetLastError();
      PrintFormat("❌ Erro ao conectar ao servidor TCP em %s:%d (código %d)", ServerIP, ServerPort, erro);
      return INIT_FAILED;
   }

   PrintFormat("🔌 Conectado ao servidor TCP: %s:%d", ServerIP, ServerPort);
   ultimoCandle = iTime(Symbol(), PERIOD_CURRENT, 0);
   return INIT_SUCCEEDED;
}

void OnTick()
{
   datetime atual = iTime(Symbol(), PERIOD_CURRENT, 0);
   if (atual != ultimoCandle)
   {
      ultimoCandle = atual;
      EnviarSinal();
      ReceberSinal();
   }
}

void OnDeinit(const int reason)
{
   if (sock != -1)
      SocketClose(sock);
}
