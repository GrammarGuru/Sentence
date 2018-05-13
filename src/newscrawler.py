from newspaper import Article
import spacy
from .sentence import Sentence

nlp = spacy.load('en_core_web_sm')

def crawl(link):
    article = Article(link)
    article.download()
    article.parse()
    doc = nlp(article.text)
    lines = [sent.string.strip() for sent in doc.sents]
    return [line for line in lines if Sentence(line).is_valid()]


if __name__ == '__main__':
    lines = crawl("http://bleacherreport.com/articles/2775757-amanda-nunes-emerges-from-ronda-rouseys-shadow-ready-for-cyborg-fight?utm_source=cnn.com&utm_medium=referral&utm_campaign=editorial")
    for line in lines:
        print(line)