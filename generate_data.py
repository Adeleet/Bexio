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
