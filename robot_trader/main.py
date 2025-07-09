from robot_trader.mt5.socket_client import MT5SocketClient
from robot_trader.api.server import iniciar_api
from robot_trader.ai.lightgbm_model import prever_sinal
from robot_trader.db import salvar_candle, criar_tabelas
import threading
import time
import json
from datetime import datetime

ordens_executadas = []

class RoboTrader:
    def __init__(self):
        self.cliente_mt5 = MT5SocketClient()

    def iniciar(self):
        criar_tabelas()
        self.cliente_mt5.on_message(self.processar_tick)
        threading.Thread(target=self.cliente_mt5.start, daemon=True).start()
        iniciar_api(ordens_executadas)

    def processar_tick(self, tick):
        try:
            dados = json.loads(tick)
            print("📈 Tick recebido:", dados)

            candle = {
                "ativo": dados.get("ativo", "DESCONHECIDO"),
                "open": dados.get("open"),
                "high": dados.get("high"),
                "low": dados.get("low"),
                "close": dados.get("close"),
                "volume": dados.get("volume"),
                "timestamp": datetime.utcnow()
            }

            salvar_candle(candle)

            sinal = prever_sinal(dados)
            ordem = {
                "ativo": candle["ativo"],
                "tipo": sinal,
                "preco": candle["close"],
                "timestamp": candle["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
            }

            ordens_executadas.append(ordem)
            print("✅ Sinal gerado:", ordem)

            # Envia resposta ao MT5 com ativo e sinal
            self.enviar_resposta({
                "ativo": candle["ativo"],
                "sinal": sinal
            })

        except Exception as e:
            print("❌ Erro ao processar tick:", e)

    def enviar_resposta(self, resposta_dict):
        try:
            resposta = json.dumps(resposta_dict)
            for client in self.cliente_mt5.clientes_conectados:
                client.sendall(resposta.encode() + b"\n")
        except Exception as e:
            print("❌ Erro ao enviar resposta ao MT5:", e)

if __name__ == "__main__":
    print("🚀 Iniciando robô de trade com PostgreSQL e múltiplos ativos...")
    robo = RoboTrader()
    robo.iniciar()
    while True:
        time.sleep(1)
