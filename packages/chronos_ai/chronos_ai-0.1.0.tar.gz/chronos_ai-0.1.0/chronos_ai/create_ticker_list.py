import pandas as pd


def create_ticker_list():
    return (
        pd.read_csv(f"./chronos_ai/data/nasdaq_screener_1711270178562.csv")
        .dropna()
        .reset_index()
        .loc[:, "Symbol"]
    )
