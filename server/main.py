from newscrawler import get_articles, crawl
from firestore import FireStore
import en_core_web_sm

nlp = en_core_web_sm.load()


def get_article(article):
    return {
        'title': article.title,
        'link': article.id,
        'lines': crawl(article.id)
    }


def load_articles(size=20):
    articles = get_articles(size=size)
    db = FireStore()
    db.clear()
    for article in articles:
        data = get_article(article)
        db.add(article.title, data)


if __name__ == '__main__':
    load_articles()