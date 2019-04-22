import pandas as pd


class Reward:
    def __init__(self, client):
        self.client = client

    def __last_o_book__(self, o_book, side=None):
        if side:
            o_book = o_book[o_book["side"] == side]
        return o_book[o_book["timestamp"] == o_book["timestamp"].max()]

    def get(self, prev_act, vwap):
        orders = self.client.get_orders(params={"symbol": "XBTUSD",
                                                "reverse": "true",
                                                "count": "10"})

        df_orders = pd.DataFrame(orders)[["cumQty",
                                          "price",
                                          "side",
                                          "timestamp"]]
        df_orders["timestamp"] = pd.to_datetime(df_orders["timestamp"])

        self.last_order = self.__last_o_book__(df_orders)
        self.last_buy = self.__last_o_book__(df_orders, "Buy").values[0]
        self.last_sell = self.__last_o_book__(df_orders, "Sell").values[0]

        if prev_act != self.last_order["side"].values[0] or prev_act == "Hold":
            return 0
        elif prev_act == "Buy":
            return vwap - self.last_buy
        elif prev_act == "Sell":
            return self.last_sell - self.last_buy
