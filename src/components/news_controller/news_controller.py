from src.components.link_label import LinkLabel
from src.components.widget_utils import fill_layout
from PyQt5.QtWidgets import QWidget, \
    QPushButton, \
    QVBoxLayout, QLabel, \
    QMessageBox, QGridLayout

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


class NewsController(QWidget):
    def __init__(self, topic, articles, lines_func):
        super().__init__()
        self.setStyleSheet(background_sheet)
        self.lines_func = lines_func
        self.articles = articles
        self.layout = QVBoxLayout(self)

        grid = QGridLayout()
        grid.setSpacing(10)
        title = create_label('Category: {}'.format(topic))
        for index, article in enumerate(self.articles):
            label = LinkLabel(article['title'].strip(), article['url'], font_size=12)
            callback = lambda _, lines=article['lines']: self.send_lines(lines)
            btn = create_btn(callback)
            grid.addWidget(label, index + 1, 0)
            grid.addWidget(btn, index + 1, 1)

        fill_layout(self.layout, title, grid)

    def send_lines(self, lines):
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
