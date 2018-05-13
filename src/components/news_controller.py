import sys
import newspaper
import random

from PyQt5.QtWidgets import QWidget, \
    QPushButton, QHBoxLayout, \
    QVBoxLayout, QLabel, \
    QLineEdit, QMessageBox, QGridLayout, QApplication

SOURCES = ["http://www.bbc.com/news"]


def is_valid(article):
    return article.title is not None and len(article.title.strip()) > 7


class NewsController(QWidget):
    def __init__(self, news_func):
        super().__init__()
        self.news_func = news_func
        self.articles = self.get_articles()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        manual_label = QLabel('Enter link')
        self.layout.addWidget(manual_label)
        manual_layout = QHBoxLayout()
        manual_line = QLineEdit()
        manual_layout.addWidget(manual_line)
        manual_btn = QPushButton('Add')
        manual_btn.clicked.connect(lambda: self.send_link(None, manual_line.text()))
        manual_layout.addWidget(manual_btn)
        self.layout.addLayout(manual_layout)

        grid = QGridLayout()
        grid.setSpacing(10)
        top_stories_label = QLabel('Top Stories')
        self.layout.addWidget(top_stories_label)
        for index, article in enumerate(self.articles):
            label = QLabel(article.title.strip())
            label.mousePressEvent = lambda _: print("Click")
            grid.addWidget(label, index + 1, 0)
            btn = QPushButton('Add')
            callback = lambda x, link=article.url: self.send_link(x, link)
            btn.clicked.connect(callback)
            grid.addWidget(btn, index + 1, 1)
        self.layout.addLayout(grid)

    def send_link(self, temp, link):
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

    @staticmethod
    def get_articles(size=10):
        links = []
        for source in SOURCES:
            paper = newspaper.build(source, memoize_articles=False)
            links += [article for article in paper.articles if is_valid(article)]
        return random.sample(links, min(len(links), size))



if __name__ == '__main__':
    func = lambda x: print("sadf")
    app = QApplication(sys.argv)
    ex = NewsController(func)
    ex.show()
    sys.exit(app.exec_())