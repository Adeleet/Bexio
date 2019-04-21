import hmac
import time
from hashlib import sha256
from urllib.parse import quote

from config import API_KEY, API_SECRET


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
