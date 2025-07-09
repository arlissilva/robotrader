import lightgbm as lgb
import pandas as pd
import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "modelo_lightgbm.pkl")

def treinar_lightgbm(dados_csv: str):
    df = pd.read_csv(dados_csv)
    df["sinal"] = ((df["close"].shift(-1) - df["close"]) > 50).astype(int)
    df.dropna(inplace=True)
    if df["sinal"].nunique() < 2:
        raise ValueError("❌ Dados não balanceados.")
    X = df[["open", "high", "low", "close", "volume"]]
    y = df["sinal"]
    modelo = lgb.LGBMClassifier()
    modelo.fit(X, y)
    joblib.dump(modelo, MODEL_PATH)

def prever_sinal(tick):
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("❌ Modelo não treinado.")
    modelo = joblib.load(MODEL_PATH)
    df_tick = pd.DataFrame([tick])
    X = df_tick[["open", "high", "low", "close", "volume"]]
    pred = modelo.predict(X)[0]
    return "compra" if pred == 1 else "venda"