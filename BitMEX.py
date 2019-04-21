from urllib.parse import urlencode

from requests import Session

from config import BASE_URL
from connection import generate_headers


class BitMEX:
    def __init__(self):
        self.session = Session()

    def make_request(self, method, endpoint, params={}):
        if params:
            headers = generate_headers(
                f"{method}", f"{endpoint}?{urlencode(params)}")
        else:
            headers = generate_headers(f"{method}", f"{endpoint}")
        r = self.session.request(method, f"{BASE_URL}/{endpoint}",
                                 params=params, headers=headers)
        return r.json()

    def executions(self, params=None):
        return self.make_request("GET", "/execution/tradeHistory", params)

    def instruments(self, params=None):
        return self.make_request("GET", "/instrument/active", params)

    def liquidations(self, params=None):
        return self.make_request("GET", "/liquidation", params)

    def get_orders(self, params=None):
        return self.make_request("GET", "/order", params)

    def cancel_orders(self, params=None):
        return self.make_request("DELETE", "/order/all", params)

    def create_order(self, params=None):
        return self.make_request("POST", "/order", params)

    def orderbook(self, params=None):
        return self.make_request("GET", "/orderBook/L2", params)

    def positions(self, params=None):
        return self.make_request("GET", "/position", params)

    def quotes(self, params=None):
        return self.make_request("GET", "/quote", params)

    def quotes_bucketed(self, params=None):
        return self.make_request("GET", "/quote/bucketed", params)

    def settlements(self, params=None):
        return self.make_request("GET", "/settlement", params)

    def stats(self, params=None):
        return self.make_request("GET", "/stats", params)

    def stats_history(self, params=None):
        return self.make_request("GET", "/stats/historyUSD", params)

    def trades(self, params=None):
        return self.make_request("GET", "/trade", params)

    def trades_bucketed(self, params=None):
        return self.make_request("GET", "/trade/bucketed", params)

    def user(self, params=None):
        return self.make_request("GET", "/user", params)

    def user_execution_history(self, params=None):
        return self.make_request("GET", "/user/executionHistory", params)

    def user_wallet(self, params=None):
        return self.make_request("GET", "/user/wallet", params)

    def user_wallet_history(self, params=None):
        return self.make_request("GET", "/user/walletHistory", params)

    def user_wallet_summary(self, params=None):
        return self.make_request("GET", "/user/walletsummary", params)
