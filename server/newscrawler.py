import sys
import json
import feedparser as fp
import random
from newspaper import Article
from nltk import sent_tokenize
import en_core_web_sm
sys.path.append("..")
from src.sentence import Sentence

nlp = en_core_web_sm.load()


def crawl(link):
    article = Article(link)
    article.download()
    article.parse()
    doc = nlp(article.text)
    lines = [sent.string.strip() for sent in doc.sents]
    return [line for line in lines if Sentence(line).is_valid()]


def is_good_article(link):
    if "/video/" in link or '/videos/' in link:
        return False
    try:
        article = Article(link)
        article.download()
        article.parse()
        if ';' in article.title:
            return False
        return len(sent_tokenize(article.text)) > 10
    except:
        return False


def get_articles(size=20):
    links = []
    with open('../config/newspapers.json') as f:
        sources = json.load(f)
        for _, value in sources.items():
            paper = fp.parse(value['rss'])
            links += [article for article in paper.entries]
    result = []
    while len(result) < size:
        index = random.randint(0, len(links) - 1)
        article = links[index]
        if is_good_article(article.id):
            result.append(article)
            del links[index]
    return result
