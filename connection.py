from urllib.parse import urlencode
from requests import request
from hashlib import sha256
import hmac
import time
from config import API_KEY, API_SECRET
from urllib.parse import quote


def generate_nonce():
    return int(time.time())


def generate_signature(verb, endpoint, expires, data=""):
    data = quote(str(data))
    path = f"/api/v1/{endpoint}"
    msg = bytes(verb + path + expires + data, "utf8")
    signature = hmac.new(bytes(API_SECRET, "utf8"), msg, digestmod=sha256)
    return signature.hexdigest()


def generate_headers(method, endpoint, data=""):
    nonce = str(generate_nonce())
    return {
        'api-expires': str(nonce),
        'api-key': API_KEY,
        'api-signature': generate_signature(method, endpoint, nonce, data)
    }


BASE_URL = "https://www.bitmex.com/api/v1"


def make_request(method, endpoint, params={}):
    if params:
        headers = generate_headers(
            f"{method}", f"{endpoint}?{urlencode(params)}")
    else:
        headers = generate_headers(f"{method}", f"{endpoint}")
    r = request(method, f"{BASE_URL}/{endpoint}",
                params=params, headers=headers)
    return r.json()
