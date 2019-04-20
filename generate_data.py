import os

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
