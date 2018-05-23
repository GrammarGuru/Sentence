import sys
import random
from firebase_admin import firestore
from .link_label import LinkLabel
from PyQt5.QtWidgets import QWidget, \
    QPushButton, QHBoxLayout, \
    QVBoxLayout, QLabel, \
    QLineEdit, QMessageBox, QGridLayout, QApplication, QLayout
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


def create_label(name):
    label = QLabel(name)
    label.setStyleSheet(header_sheet)
    label.setFont(QFont('Times New Roman', 13))
    return label

def create_btn(on_click):
    btn = QPushButton('Add')
    btn.setStyleSheet(btn_sheet)
    btn.clicked.connect(on_click)
    return btn

def fill_layout(layout, *args):
    for item in args:
        if isinstance(item, QLayout):
            layout.addLayout(item)
        else:
            layout.addWidget(item)
    


class NewsController(QWidget):
    def __init__(self, link_func, lines_func):
        super().__init__()
        self.setStyleSheet(background_sheet)
        self.link_func = link_func
        self.lines_func = lines_func
        self.articles = get_articles()
        self.layout = QVBoxLayout(self)

        manual_label = create_label('Enter Link')
        manual_layout = QHBoxLayout()
        manual_line = QLineEdit()
        manual_btn = create_btn(lambda: self.send_link(None, manual_line.text()))
        fill_layout(manual_layout, manual_line, manual_btn)

        grid = QGridLayout()
        grid.setSpacing(10)
        top_stories_label = create_label('Top Stories')
        for index, article in enumerate(self.articles):
            label = LinkLabel(article['title'].strip(), article['link'], font_size=12)
            callback = lambda _, lines=article['lines']: self.send_lines(_, lines)
            btn = create_btn(callback)
            grid.addWidget(label, index + 1, 0)
            grid.addWidget(btn, index + 1, 1)

        fill_layout(self.layout, manual_label, manual_layout, top_stories_label, grid)

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
