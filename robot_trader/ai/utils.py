import pandas as pd

def carregar_dados_formatados(caminho_csv):
    df = pd.read_csv(caminho_csv)
    df = df[["open", "high", "low", "close", "volume"]]
    df.dropna(inplace=True)
    return df