import requests


def post(url, body={}, json=None):
    if json is not None:
        r = requests.post(url, json=json)
    else:
        r = requests.post(url, body)
    r.raise_for_status()
    return r


def get(url, params={}):
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r
