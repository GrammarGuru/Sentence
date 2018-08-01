import json

from services.utils import get

with open('config/api.json') as f:
    URL = json.load(f)['functions']


def get_data():
    data = get(URL + 'web').json()
    for key in data.keys():
        data[key] = json.loads(data[key])[:20]  # TODO: Remove later
    return data
