

import pandas as pd
import BitMEX
from RL import reward
from RL.observation import Observation


def buy(client, ob):
    last_vwap = ob.last_vwap
    client.createOrder()


def sell(client, ob):
    last_vwap = ob.last_vwap


def hold(client, ob):
    last_vwap = ob.last_vwap


client = BitMEX.BitMEX()
ob = Observation(client)
