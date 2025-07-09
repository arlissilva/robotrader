from robot_trader.ai.lightgbm_model import prever_sinal
from robot_trader.db import obter_candles_periodo
import sys

def executar_backtest(dias=30):
    candles = obter_candles_periodo(dias)
    if not candles:
        print("⚠️ Nenhum dado encontrado no banco de dados.")
        return

    print(f"📊 Executando backtest com {len(candles)} candles dos últimos {dias} dias...")
    compras = 0
    vendas = 0

    for c in candles:
        tick = {
            "open": c.open,
            "high": c.high,
            "low": c.low,
            "close": c.close,
            "volume": c.volume
        }
        sinal = prever_sinal(tick)
        if sinal == "compra":
            compras += 1
        else:
            vendas += 1

    print(f"✅ Resultado do backtest: {compras} compras / {vendas} vendas")

if __name__ == "__main__":
    dias = 30
    if len(sys.argv) > 1:
        try:
            dias = int(sys.argv[1])
        except:
            print("⚠️ Número de dias inválido, usando 30.")
    executar_backtest(dias)