import sys
from newscrawler import get_articles
from firestore import FireStore
from newspaper import Article
sys.path.append("..")
from src.sentence import Sentence
import en_core_web_sm

nlp = en_core_web_sm.load()


def crawl(link):
    article = Article(link)
    article.download()
    article.parse()
    doc = nlp(article.text)
    lines = [sent.string.strip() for sent in doc.sents]
    return [line for line in lines if Sentence(line).is_valid()]


def get_article(article):
    return {
        'title': article.title,
        'lines': crawl(article.id)
    }


def load_articles(size=20):
    articles = get_articles(size=size)
    print(articles)
    db = FireStore()
    for article in articles:
        data = get_article(article)
        db.add(article.title, data)


if __name__ == '__main__':
    load_articles()