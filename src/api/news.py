import requests
import json

with open('config/api.json') as f:
    URL = json.load(f)['functions']


def get_data():
    content = requests.get(URL + 'getNews').content
    return json.loads(content)