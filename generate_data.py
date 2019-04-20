import os
from glob import glob

import pandas as pd
import requests


def download_data(source):
    if source not in ["trade", "quote"]:
        raise ValueError("source should be 'trade' or 'quote'")
    with open(f"data/{source}_urls.txt") as file_object:
        file_lines = file_object.readlines()
        urls = [q.strip() for q in file_lines]
    sess = requests.Session()
    if not os.path.exists(f"./data/{source}"):
        os.makedirs(f"./data/{source}")
    for url in urls:
        file_name = url[url.index(source) + 6:]
        req = sess.get(url)

        with open(f"./data/{source}/{file_name}", "wb") as file_object:
            file_object.write(req.content)


def create_dataframes():
    if min(
            len(glob("data\\quote\\*.csv.gz")),
            len(glob("data\\quote\\*.csv.gz"))) < 0:
        raise EnvironmentError(
            "No data found, please run download_data() first")

    quote_dfs = [pd.read_csv(f"data/quote/{f}")
                 for f in os.listdir("data/quote")[:10]]
    pd.concat(quote_dfs).to_csv("data/quote.csv.gz", compression="gzip")
    quote_dfs = None
    trade_dfs = [pd.read_csv(f"data/trade/{f}")
                 for f in os.listdir("data/trade")]

    pd.concat(trade_dfs).to_csv("data/trade.csv.gz", compression="gzip")


create_dataframes()
