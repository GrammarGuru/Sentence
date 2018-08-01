import json

from services.utils import get
from .nlp import get_sentences

with open('config/api.json') as f:
    URL = json.load(f)['functions']


def get_data():
    return get(URL + 'news').json()


def get_article(article_id):
    return get('{}news/{}'.format(URL, article_id)).json()


def crawl(url):
    return get(URL + 'scrape', params={'url': url}).json()


def break_paragraphs(paragraphs):
    return [line for p in paragraphs for line in get_sentences(p)]
