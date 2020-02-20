import gym
import numpy as np
import pandas as pd
from gym import spaces
from sklearn import preprocessing
import math
from ExchangeClient import ExchangeClient

SATOSHI_BTC = 0.00000001


class BitMEX(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, api_key, api_secret):
        self.action_space = spaces.Discrete(3)
        self.client = ExchangeClient(api_key=api_key, api_secret=api_secret)
        self.observation_space = spaces.Box(shape=(1000, 10), low=0, high=1)

    def step(self, action):
        reward = self._get_reward()
        self._take_action(action)
        (price, obs) = self._get_obs()
        return obs, reward, False, {}

    def reset(self):
        self.position = self._get_position()
        (price, obs) = self._get_obs()
        self.price = price
        return obs

    def render(self, mode='human'):
        current_position = self._get_position()
        self.log("update", f"position = {current_position} XBT")

    def close(self):
        pass

    def _get_obs(self):
        orderbook = self._get_orderbook_data()
        (price, trade_data) = self._get_trade_data()
        df_orderbook = pd.DataFrame(orderbook)
        df_trades = pd.DataFrame(trade_data)
        return (price, pd.concat([df_orderbook, df_trades],
                                 ignore_index=True).reset_index(drop=True).values)

    def _take_action(self, action_type):
        qty = math.floor(self._get_available_balance() * self.price)
        price, trade_data = self._get_trade_data()
        if action_type == 0:
            self.client.create_order(side="Buy",
                                     orderQty=qty,
                                     price=round(price))
            self.client.cancel_all_after()
            self.log("agent-action", f"buy {qty} at ${price}")
        elif action_type == 1:
            self.client.create_order(side="Sell",
                                     orderQty=qty,
                                     price=round(price))
            self.client.cancel_all_after()
            self.log("agent-action", f"sell {qty} at ${price}")
        else:
            self.log("agent", "holding")

    def log(self, category, message):
        now = pd.Timestamp.utcnow()
        print(f"{now} [{category}] : {message}")

    def _get_orderbook_data(self):
        orderbook = self.client.orderbookL2(symbol="XBTUSD", depth=250)
        df = pd.DataFrame(orderbook, columns=["side", "size", "price"])
        df = pd.get_dummies(df)
        # normalize trade_data
        for col in df.columns:
            if abs(df[col].skew()) > 2:
                df[col] = np.log1p(df[col])
        x = df.values  # returns a numpy array
        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(x)
        df = pd.DataFrame(x_scaled)
        return df.values

    def _get_trade_data(self):
        now = pd.Timestamp.utcnow()
        res = self.client.trades(
            symbol="XBTUSD",
            count=500,
            reverse=True)
        df = pd.DataFrame(
            res,
            columns=[
                'timestamp',
                'side',
                'size',
                'price',
                'tickDirection',
                'grossValue',
            ])

        df['timestamp'] = df['timestamp'].apply(pd.Timestamp)
        df['t_delta'] = (now - df['timestamp']) / pd.Timedelta(1, 's')
        df.drop('timestamp', axis=1, inplace=True)

        weights = df['size'] / df['t_delta']
        price = (df['price'] * weights).sum() / weights.sum()

        df = pd.get_dummies(df)
        # normalize trade_data
        for col in df.columns:
            if abs(df[col].skew()) > 2:
                df[col] = np.log1p(df[col])
        x = df.values  # returns a numpy array
        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(x)
        df = pd.DataFrame(x_scaled)
        return price, df.values

    def _get_available_balance(self):
        self.price
        available = self.client.user_margin_balance()['availableMargin']
        return available * SATOSHI_BTC

    def _get_position(self):
        position = self.client.user_margin_balance()["marginBalance"]
        return position * SATOSHI_BTC

    def _get_reward(self):
        new_position = self._get_position()
        return new_position - self.position
