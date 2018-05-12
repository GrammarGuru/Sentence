from newspaper import Article
from nltk import sent_tokenize

def crawl(link):
    article = Article(link)
    article.download()
    article.parse()
    return sent_tokenize(article.text)

if __name__ == '__main__':
    lines = crawl("https://abcnews.go.com/International/wireStory/monitor-42-killed-israeli-strikes-syria-week-55115848")
    for line in lines:
        print(line)