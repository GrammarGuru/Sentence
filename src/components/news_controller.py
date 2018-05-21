import sys
from nltk import sent_tokenize
from newspaper import Article
import random
import feedparser as fp
import json
from .link_label import LinkLabel
from PyQt5.QtWidgets import QWidget, \
    QPushButton, QHBoxLayout, \
    QVBoxLayout, QLabel, \
    QLineEdit, QMessageBox, QGridLayout, QApplication
from PyQt5.QtGui import QFont

background_sheet = """
                    background-color: rgb(250, 250, 250)
                   """
btn_sheet = """
        color: rgb(255, 255, 255);
        border-radius: 5px;
        border: 2px solid rgb(66, 184, 221);
        text-shadow 0 1px 1px rgba(0, 0, 0, 0.2);
        background-color: rgb(66, 184, 221);
        """

header_sheet = """
                color: rgb(66, 184, 221);
               """


def is_valid(article):
    return article.title is not None and len(article.title.strip()) > 7


def is_good_article(link):
    print(link)
    try:
        article = Article(link)
        article.download()
        article.parse()
        return len(sent_tokenize(article.text)) > 10
    except:
        return False


def get_articles(size=10):
    links = []
    with open('newspapers.json') as f:
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


class NewsController(QWidget):
    def __init__(self, news_func):
        super().__init__()
        self.setStyleSheet(background_sheet)
        self.news_func = news_func
        self.articles = get_articles()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        manual_label = QLabel('Enter link')
        self.format_label(manual_label)
        self.layout.addWidget(manual_label)
        manual_layout = QHBoxLayout()
        manual_line = QLineEdit()
        manual_layout.addWidget(manual_line)
        manual_btn = QPushButton('Add')
        manual_btn.setStyleSheet(btn_sheet)
        manual_btn.clicked.connect(lambda: self.send_link(None, manual_line.text()))
        manual_layout.addWidget(manual_btn)
        self.layout.addLayout(manual_layout)

        grid = QGridLayout()
        grid.setSpacing(10)
        top_stories_label = QLabel('Top Stories')
        self.format_label(top_stories_label)
        self.layout.addWidget(top_stories_label)
        for index, article in enumerate(self.articles):
            label = LinkLabel(article.title.strip(), article.id, font_size=12)
            grid.addWidget(label, index + 1, 0)
            btn = QPushButton('Add')
            btn.setStyleSheet(btn_sheet)
            callback = lambda x, link=article.id: self.send_link(x, link)
            btn.clicked.connect(callback)
            grid.addWidget(btn, index + 1, 1)
        self.layout.addLayout(grid)

    def format_label(self, label):
        label.setStyleSheet(header_sheet)
        label.setFont(QFont('Times New Roman', 13))

    def send_link(self, _, link):
        print('link', link)
        try:
            self.news_func(link)
            self.close()
        except Exception as inst:
            print(inst)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText('Error: Check Link and Try Again')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.show()



if __name__ == '__main__':
    func = lambda x: print("sadf")
    app = QApplication(sys.argv)
    ex = NewsController(func)
    ex.show()
    sys.exit(app.exec_())