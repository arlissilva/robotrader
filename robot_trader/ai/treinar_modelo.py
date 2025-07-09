from lightgbm_model import treinar_lightgbm
import os

CAMINHO_PADRAO = os.path.join(os.path.dirname(__file__), "dados", "exemplo_1000_candles.csv")

def main():
    print("📚 Treinando modelo LightGBM com:", CAMINHO_PADRAO)
    try:
        treinar_lightgbm(CAMINHO_PADRAO)
        print("✅ Modelo treinado com sucesso.")
    except Exception as e:
        print("❌ Erro no treinamento:", e)

if __name__ == "__main__":
    main()