import os
import time
from datetime import datetime
from glob import glob

import numpy as np
import pandas as pd
import requests

from BitMEX import BitMEX

columns = ['close', 'foreignNotional', 'high', 'homeNotional', 'lastSize',
           'low', 'open', 'symbol', 'timestamp', 'trades', 'turnover',
           'volume', 'vwap']


def get_bucketed_trades():
    client = BitMEX()
    trade_data = np.empty((0, len(columns)))
    total_elapsed = (datetime.now() - datetime(2017, 1, 1))
    total_minutes = int((total_elapsed.total_seconds() / 60))
    progress = 0
    for i in range(0, total_minutes, 750):
        time.sleep(0.8)
        if "x-ratelimit-remaining" in client.response_headers.keys():
            remaining = int(client.response_headers["x-ratelimit-remaining"])
            current_progress = round(i / total_minutes, 2)
            if current_progress > progress:
                print(f"{round(i/total_minutes,2)} - {remaining}/300")
                progress = current_progress
            if remaining > 10 and remaining < 50:
                time.sleep(30)
            elif remaining < 10:
                raise ValueError("exceeding rate limit")
        new_values = pd.DataFrame(client.trades_bucketed(params={
                                  "binSize": "1m",
                                  "start": i,
                                  "count": 750,
                                  "symbol": "XBTUSD"}))
        try:
            trade_data = np.vstack([trade_data, new_values])
        except ValueError:
            print(client.rate_remaining, new_values)

    return pd.DataFrame(trade_data, columns=columns)


def download_data(source):
    """
    Downloads all historical data, using either trades or quotes

    Arguments:
        source (str) : type of data, must be 'trade' or 'quote'
    """

    # Ensure that argument source is trade or quote
    if source not in ["trade", "quote"]:
        raise ValueError("source should be 'trade' or 'quote'")

    # Open and read specified source urls .txt file (trade or quote)
    with open(f"data/{source}_urls.txt") as file_object:
        file_lines = file_object.readlines()
        urls = [q.strip() for q in file_lines]

    # Create /data/trade or /data/quote if it does not exist
    if not os.path.exists(f"./data/{source}"):
        os.makedirs(f"./data/{source}")

    # Initialize session, fetch .csv files using urls read from .txt file
    sess = requests.Session()
    for url in urls:
        file_name = url[url.index(source) + 6:]
        req = sess.get(url)
        with open(f"./data/{source}/{file_name}", "wb") as file_object:
            file_object.write(req.content)


def create_dataframe(source):
    file_index, df_index = 1, 1
    if source not in ["trade", "quote"]:
        raise ValueError("source should be 'trade' or 'quote'")
    if len(glob("data\\quote\\*.csv.gz")) == 0:
        raise EnvironmentError(
            "No data found, please run download_data() first")
    df_list = []
    file_list = os.listdir(f"data/{source}")
    num_files = len(file_list)
    for f in file_list:
        df_list.append(pd.read_csv(f"data/{source}/{f}"))
        if file_index == 50 or f == file_list[-1]:
            df = pd.concat(df_list)
            df_list = []
            df.to_csv(f"data/{source}-{df_index}.csv.gz",
                      compression="gzip", index=False)
            print(f"{df_index*50} / {num_files}")
            df_index += 1
            file_index = 0
        file_index += 1


# data = get_bucketed_trades()
# data.to_csv("data/bucketed/trades.csv.gz", index=False, compression="gzip")
