from urllib.parse import urlencode

from requests import Session

import hmac
import time
from hashlib import sha256
from urllib.parse import quote

BASE_URL = "https://www.bitmex.com/api/v1"


class ExchangeClient:
    def __init__(self, api_key, api_secret):
        self.session = Session()
        self.response_headers = {}
        self.request_headers = {}
        self.API_KEY = api_key
        self.API_SECRET = api_secret
        self.rate_remaining = 0

    @staticmethod
    def _generate_nonce():
        """
        Generates nonce for signature

        Returns:
        nonce (int) : timestamp epoch
        """
        return int(time.time() + 100)

    def generate_signature(self, verb, endpoint, expires, data=""):
        data = quote(str(data))
        path = f"/api/v1/{endpoint}"
        msg = bytes(verb + path + expires + data, "utf8")
        signature = hmac.new(bytes(self.API_SECRET, "utf8"), msg, digestmod=sha256)
        return signature.hexdigest()

    def generate_headers(self, method, endpoint, data=""):
        nonce = str(ExchangeClient._generate_nonce())
        return {
            "api-expires": str(nonce),
            "api-key": self.API_KEY,
            "api-signature": self.generate_signature(method, endpoint, nonce, data),
        }

    def make_request(self, method, endpoint, params={}):
        if params:
            headers = self.generate_headers(
                f"{method}", f"{endpoint}?{urlencode(params)}"
            )
        else:
            headers = self.generate_headers(f"{method}", f"{endpoint}")
        r = self.session.request(
            method, f"{BASE_URL}/{endpoint}", params=params, headers=headers
        )
        self.response_headers = r.headers
        self.request_headers = headers
        self.rate_remaining = r.headers["X-RateLimit-Remaining"]
        return r.json()

    def executions(self, **kwargs):
        return self.make_request("GET", "/execution/tradeHistory", kwargs)

    def instruments(self, **kwargs):
        return self.make_request("GET", "/instrument/active", kwargs)

    def liquidations(self, **kwargs):
        return self.make_request("GET", "/liquidation", kwargs)

    def get_orders(self, count=1, reverse="true"):
        return self.make_request(
            "GET",
            "/order",
            params={
                "count": count,
                reverse: reverse})

    def cancel_orders(self, **kwargs):
        return self.make_request("DELETE", "/order/all", kwargs)

    def create_order(
            self,
            side,
            orderQty,
            price,
            execInst="ParticipateDoNotInitiate",
            symbol="XBTUSD"):
        return self.make_request("POST", "/order", params={
            "symbol": symbol,
            "side": side,
            "orderQty": orderQty,
            "price": price,
            "execInst": "ParticipateDoNotInitiate"
        })

    def cancel_all_after(self, timeout=50000):
        return self.make_request("POST", "/order/cancelAllAfter", {"timeout": timeout})

    def orderbookL2(self, symbol, depth=25):
        return self.make_request("GET", "/orderBook/L2",
                                 {"symbol": symbol, "depth": depth})

    def positions(self, **kwargs):
        return self.make_request("GET", "/position", kwargs)

    def quotes(self, **kwargs):
        return self.make_request("GET", "/quote", kwargs)

    def quotes_bucketed(self, **kwargs):
        return self.make_request("GET", "/quote/bucketed", kwargs)

    def settlements(self, **kwargs):
        return self.make_request("GET", "/settlement", kwargs)

    def stats(self, **kwargs):
        return self.make_request("GET", "/stats", kwargs)

    def stats_history(self, **kwargs):
        return self.make_request("GET", "/stats/historyUSD", kwargs)

    def trades(self, **kwargs):
        return self.make_request("GET", "/trade", kwargs)

    def trades_bucketed(self, **kwargs):
        return self.make_request("GET", "/trade/bucketed", kwargs)

    def user(self, **kwargs):
        return self.make_request("GET", "/user", kwargs)

    def user_execution_history(self, **kwargs):
        return self.make_request("GET", "/user/executionHistory", kwargs)

    def user_wallet(self, **kwargs):
        return self.make_request("GET", "/user/wallet", kwargs)

    def user_wallet_history(self, **kwargs):
        return self.make_request("GET", "/user/walletHistory", kwargs)

    def user_wallet_summary(self, **kwargs):
        return self.make_request("GET", "/user/walletsummary", kwargs)

    def user_margin_balance(self):
        return self.make_request("GET", "/user/margin?currency=XBt")
