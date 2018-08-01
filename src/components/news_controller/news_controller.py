from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import \
    QVBoxLayout, QLabel, \
    QMessageBox, QGridLayout

from services.news import get_article
from src.components.link_label import LinkLabel
from src.components.window import Window
from src.widget_utils import fill_layout, create_btn

header_sheet = """
                color: rgb(66, 184, 221);
               """


def create_label(name):
    label = QLabel(name)
    label.setStyleSheet(header_sheet)
    label.setFont(QFont('Times New Roman', 13))
    return label


class NewsController(Window):
    def __init__(self, topic, articles, lines_func):
        super().__init__()
        self.lines_func = lines_func
        self.articles = articles
        self.layout = QVBoxLayout(self)

        grid = QGridLayout()
        grid.setSpacing(10)
        title = create_label('Category: {}'.format(topic))
        for index, article in enumerate(self.articles):
            label = LinkLabel(article['title'].strip(), article['url'], font_size=12)
            callback = lambda _, id=article['id'], link=article['url']: self.send_lines(id, link)
            btn = create_btn('Add', callback, style='secondary')
            grid.addWidget(label, index + 1, 0)
            grid.addWidget(btn, index + 1, 1)

        fill_layout(self.layout, title, grid)

    def send_lines(self, article_id, link):
        try:
            lines = get_article(article_id)
            self.lines_func(lines, link)
            self.close()
        except Exception as inst:
            print(inst)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText('Error: Try Again')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.show()
