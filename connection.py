from hashlib import sha256
import hmac
import time
import requests
from config import API_KEY, API_SECRET
BASE_URL = "https://www.bitmex.com"


def generate_nonce():
    return int(time.time())


def signature(verb, path, expires, data=""):
    msg = bytes(verb + path + expires + data, "utf8")
    signature = hmac.new(bytes(API_SECRET, "utf8"), msg, digestmod=sha256)
    return signature.hexdigest()


def headers(verb, path, data):
    nonce = str(generate_nonce())
    return {
        'api-expires': str(nonce),
        'api-key': API_KEY,
        'api-signature': signature(verb, path, nonce, data)
    }
