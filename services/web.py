import json

import requests

with open('config/api.json') as f:
    URL = json.load(f)['functions']


def get_data():
    data = requests.get(URL + 'getWeb').json()
    for key in data.keys():
        data[key] = json.loads(data[key])[:20]  # TODO: Remove later
    return data
