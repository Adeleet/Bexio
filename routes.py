from connection import make_request


def executions(params=None):
    return make_request("GET", "/execution/tradeHistory", params)


def instruments(params=None):
    return make_request("GET", "/instrument/active", params)


def liquidations(params=None):
    return make_request("GET", "/liquidation", params)


def get_orders(params=None):
    return make_request("GET", "/order", params)


def cancel_orders(params=None):
    return make_request("DELETE", "/order/all", params)


def create_order(params=None):
    return make_request("POST", "/order", params)


def orderbook(params=None):
    return make_request("GET", "/orderBook/L2", params)


def positions(params=None):
    return make_request("GET", "/position", params)


def quotes(params=None):
    return make_request("GET", "/quote", params)


def quotes_bucketed(params=None):
    return make_request("GET", "/quote/bucketed", params)


def settlements(params=None):
    return make_request("GET", "/settlement", params)


def stats(params=None):
    return make_request("GET", "/stats", params)


def stats_history(params=None):
    return make_request("GET", "/stats/historyUSD", params)


def trades(params=None):
    return make_request("GET", "/trade", params)


def trades_bucketed(params=None):
    return make_request("GET", "/trade/bucketed", params)


def user(params=None):
    return make_request("GET", "/user", params)


def user_execution_history(params=None):
    return make_request("GET", "/user/executionHistory", params)


def user_wallet(params=None):
    return make_request("GET", "/user/wallet", params)


def user_wallet_history(params=None):
    return make_request("GET", "/user/walletHistory", params)


def user_wallet_summary(params=None):
    return make_request("GET", "/user/walletsummary", params)
