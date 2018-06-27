import requests
import json

with open('config/api.json') as f:
    URL = json.load(f)['functions']


def get_data():
    content = requests.get(URL + 'getNews').json()
    return content


def crawl(url):
    content = requests.post(URL + 'scrape', data={'url': url}).content
    return json.loads(content)