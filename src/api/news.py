import requests
import json
from .nlp import get_sentences

with open('config/api.json') as f:
    URL = json.load(f)['functions']


def get_data():
    return requests.post(URL + 'getNews', {'file': 'data.json'}).json()


def crawl(url):
    return requests.post(URL + 'scrape', data={'url': url}).json()


def break_paragraphs(paragraphs):
    return [line for p in paragraphs for line in get_sentences(p)]