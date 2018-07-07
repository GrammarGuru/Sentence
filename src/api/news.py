import requests
import json
from nltk import sent_tokenize

with open('config/api.json') as f:
    URL = json.load(f)['functions']


def get_data():
    content = requests.get(URL + 'getNews').json()
    return content


def crawl(url):
    content = requests.post(URL + 'scrape', data={'url': url}).content
    return json.loads(content)


def break_paragraphs(paragraphs):
    return [line for p in paragraphs for line in sent_tokenize(p)]