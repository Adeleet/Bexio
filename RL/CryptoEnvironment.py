import numpy as np
from RL.actions import buy, sell, hold
from RL.observation import Observation
from RL.reward import Reward
import BitMEX

import time


class CryptoEnvironment:
    def __init__(self):
        self.client = BitMEX.BitMEX()
        self.Observation = Observation(self.client)
        self.Reward = Reward(self.client)
        self.current_ob = self.Observation.new()
        self.action_space = [buy, sell, hold]
        self.time = time.time()

    def reset(self):
        return self.current_ob

    def step(self, action=None):
        self.current_ob = self.Observation.new()
        self.time = time.time()
        self.save_data()
        # self.act(action)
        time.sleep(65)

        # reward = self.Reward.get()
        # return self.current_ob, pnl(self.client)

    def save_data(self):
        np.save(f"./Data/observations/{round(self.time)}.npy", self.current_ob)

    def act(action):
        pass


crypto_env = CryptoEnvironment()
while True:
    crypto_env.step()
