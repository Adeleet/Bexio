import sys
import time

from actions import buy, hold, sell
from BitMEX import BitMEX
from observation import Observation
from reward import Reward

sys.path.append("..")


class CryptoEnvironment:
    def __init__(self):
        self.client = BitMEX()
        self.Observation = Observation(self.client)
        self.Reward = Reward(self.client)
        self.current_ob = self.observation.new()
        self.action_space = [buy, sell, hold]

    def reset(self):
        return self.current_ob

    def step(self, action):
        observation = self.observation.new()
        self.act(action)
        time.sleep(65)
        reward = self.Reward.get()
        return self.current_ob, pnl(self.client)

    def act(action):
        pass
