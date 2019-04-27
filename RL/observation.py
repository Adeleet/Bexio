import numpy as np
import pandas as pd

from RL.stats_columns import stats_columns


class Observation:
    def __init__(self, client):
        self.client = client

    def new(self):
        # stats = __ob_stats__(client)
        orderbook = self.__ob_orderbook__()
        trades = self.__ob_trades__()
        return np.concatenate([trades, orderbook])

    def __ob_orderbook__(self):
        raw_orderbook = self.client.orderbook(
            params={"symbol": "XBTUSD", "depth": "20"})
        df_orderbook = pd.DataFrame(raw_orderbook).drop(
            ["symbol", "id"], axis=1)
        df_orderbook = df_orderbook.sort_values(by="side", ascending=False)
        return df_orderbook[["price", "size"]].values.flatten()

    def __ob_stats__(self):
        return pd.DataFrame(self.client.instruments(
            params={"symbol": "XBTUSD",
                    "columns": ",".join(stats_columns())}))

    def __ob_trades__(self):
        df = pd.DataFrame(self.client.trades_bucketed(
            params={"binSize": "1m",
                    "symbol": "XBTUSD",
                    "count": "2",
                    "reverse": "true",
                    "partial": "true"}))
        df = df.select_dtypes(exclude=["object"])
        self.last_vwap = df["vwap"][0]
        return df.apply(lambda x: x * np.array([0.75, 0.25])).sum().values
