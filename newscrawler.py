from newspaper import Article
from nltk import sent_tokenize

def crawl(link):
    article = Article(link)
    article.download()
    article.parse()
    return sent_tokenize(article.text)

if __name__ == '__main__':
    lines = crawl("http://abcnews.go.com/US/wireStory/accused-serial-rapist-killer-undetected-working-cop-54741076")
    for line in lines:
        print(line)