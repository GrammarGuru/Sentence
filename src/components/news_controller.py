import sys
import random
from firebase_admin import firestore
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


def get_articles(size=10):
    db = firestore.Client()
    articles = [doc for doc in db.collection('News').get()]
    return [doc.to_dict() for doc in random.sample(articles, size)]


def format_label(label):
    label.setStyleSheet(header_sheet)
    label.setFont(QFont('Times New Roman', 13))


class NewsController(QWidget):
    def __init__(self, link_func, lines_func):
        super().__init__()
        self.setStyleSheet(background_sheet)
        self.link_func = link_func
        self.lines_func = lines_func
        self.articles = get_articles()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        manual_label = QLabel('Enter link')
        format_label(manual_label)
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
        format_label(top_stories_label)
        self.layout.addWidget(top_stories_label)
        for index, article in enumerate(self.articles):
            label = LinkLabel(article['title'].strip(), article['link'], font_size=12)
            grid.addWidget(label, index + 1, 0)
            btn = QPushButton('Add')
            btn.setStyleSheet(btn_sheet)
            callback = lambda x, lines=article['lines']: self.send_lines(x, lines)
            btn.clicked.connect(callback)
            grid.addWidget(btn, index + 1, 1)
        self.layout.addLayout(grid)

    def send_lines(self, _, lines):
        try:
            self.lines_func(lines)
            self.close()
        except Exception as inst:
            print(inst)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText('Error: Try Again')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.show()

    def send_link(self, _, link):
        try:
            self.link_func(link)
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
    ex = NewsController(func, func)
    ex.show()
    sys.exit(app.exec_())
