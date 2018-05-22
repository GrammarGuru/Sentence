import json
import feedparser as fp
import random
from newspaper import Article
from nltk import sent_tokenize


def is_good_article(link):
    print(link)
    try:
        article = Article(link)
        article.download()
        article.parse()
        return len(sent_tokenize(article.text)) > 10
    except:
        return False


def get_articles(size=20):
    links = []
    with open('../newspapers.json') as f:
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
