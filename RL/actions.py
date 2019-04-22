import sys

import pandas as pd

from BitMEX import BitMEX
from observation import Observation
from reward import pnl

sys.path.append("..")


def buy(client, ob):
    last_vwap = ob.last_vwap
    client.createOrder()


def sell(client, ob):
    last_vwap = ob.last_vwap


def hold(client, ob):
    last_vwap = ob.last_vwap


client = BitMEX()
ob = Observation(client)
